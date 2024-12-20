import requests
from requests.auth import HTTPBasicAuth
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import json
import config

#Environment variable
ORG_ID = 'your_org_id'
url = f'https://api.eu.mist.com/api/v1/orgs/{ORG_ID}/gatewaytemplates'
device_ip = 'IP_of_your_device'
#ssh
ssh_username = 'ssh_user'
ssh_password = 'ssh_password'

#Workaround function
def get_nested(data, keys, default=None):
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        elif isinstance(data, list) and isinstance(key, int):
            try:
                data = data[key]
            except IndexError:
                return default
        else:
            return default
        if data is default:
            break
    return data

#Workaround function
def extract_names(data):
    if isinstance(data, list):
        return [item['name'] for item in data if 'name' in item]
    return data

#############################################################
def get_wan_edge_template():
    try:
        response = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
        response.raise_for_status()  # Raise an error for bad status codes
        templates = response.json()

        # Print the retrieved templates in JSON format
        print(json.dumps(templates, indent=2))

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_device_config():
    try:
        # Connect to the device
        dev = Device(host=device_ip, user=ssh_username, passwd=ssh_password)
        dev.open()

        # Retrieve the configuration in JSON format
        config = dev.rpc.get_config(options={'format': 'json'})
        # Convert to JSON string
        config_json = json.dumps(config, indent=2)

        # Print the configuration
        print(config_json)
        # Close the connection
        dev.close()
        return config_json

    except ConnectError as err:
        print(f"Cannot connect to device: {err}")


def create_wan_edge_template(config_json):

    config_dict = json.loads(config_json)

    # To split Network and Subnet_mask
    lan = str(get_nested(config_dict,['configuration', 'access', 'address-assignment', 'pool', 0, 'family', 'inet', 'network']))
    lan_parts = lan.split('/', 1)
    ip_address = str(get_nested(config_dict,['configuration', 'access', 'address-assignment', 'pool', 0, 'family', 'inet', 'dhcp-attributes', 'router', 0, 'name']))
    subnet_mask = lan_parts[1] if len(lan_parts) > 1 else ''

    template_data = {
        "name": "test",
        "type": "standalone",
        "description": "Template for WAN Edge configuration",
        "additional_config_cmds": [
            "set protocols lldp interface all",
            "set protocols lldp port-id-subtype interface-name",
            "set protocols lldp port-description-type interface-alias",
            "set protocols lldp-med interface all",
        ],
        "ip_configs": {
            "lan": {
                "type": "local",
                "ip": ip_address,
                "netmask": subnet_mask
            }
        },
        "dhcpd_config": {
            "enabled": "true",
            "lan": {
                "type": "local",
                "ip_start": get_nested(config_dict,['configuration', 'access', 'address-assignment', 'pool', 0, 'family', 'inet','range', 0, 'low'],'default_value'),
                "ip_end": get_nested(config_dict,['configuration', 'access', 'address-assignment', 'pool', 0, 'family', 'inet', 'range', 0, 'high'],'default_value'),
                "gateway": extract_names(get_nested(config_dict,['configuration', 'access', 'address-assignment', 'pool', 0, 'family', 'inet', 'dhcp-attributes', 'router'], 'default_value')),
                "dns_servers": extract_names(get_nested(config_dict, ['configuration', 'system', 'name-server'], [])),
                "options": {},
                "lease_time": get_nested(config_dict, ['configuration', 'dhcpd_config', 'lan', 'lease_time'],'default_value'),
                "fixed_bindings": {}
            }
        },
        "ospf_areas": {},
        "port_config":  {
            "ge-0/0/1": {
                "name": "wan_default",
                "usage": "wan",
                "aggregated": "false",
                "redundant": "false",
                "critical": "false",
                "disabled": "false",
                "wan_type": "broadband",
                "ip_config": {
                    "type": "dhcp"
                }
        },
        "disable_autoneg": "false",
        "wan_source_nat": {
          "disabled": "false"
        },
        "vpn_paths": {}
      },
        "bgp_config": {},
        "routing_policies": {},
        "extra_routes": {},
        "path_preferences": {},
        "service_policies": [],
        "vrf_instances": {},
        "tunnel_configs": {},
        "oob_ip_config": {
            "type": "dhcp",
            "node1": {
                "type": "dhcp"
            }
        },
        "tunnel_provider_options": {
            "jse": {},
            "zscaler": {}
        },
        "ospf_config": {
            "enabled": get_nested(config_dict, ['configuration', 'ospf_config'], []),
            "areas": {}
        },
        "ntp_servers": get_nested(config_dict, ['configuration', 'system', 'ntp'], []),
        "dns_servers": extract_names(get_nested(config_dict, ['configuration', 'system', 'name-server']))
    }

    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), headers=headers,data=json.dumps(template_data))
        response.raise_for_status()  # Raise an error for bad status codes
        print("WAN Edge template created successfully!")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    print("###### Create WAN Edge Template ######")
    create_wan_edge_template(get_device_config())
