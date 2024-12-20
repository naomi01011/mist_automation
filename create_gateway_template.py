import requests
from requests.auth import HTTPBasicAuth
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import json
import config

#Environment variable
template_name = 'your_template_name'
site_name = 'your_site_name'
ORG_ID = 'your_org_id'
url = f'https://api.eu.mist.com/api/v1/orgs/{ORG_ID}/sites'
device_ip = 'IP_address_of_your_device'
template_api_url = f'https://api.eu.mist.com/api/v1/orgs/{ORG_ID}/gatewaytemplates'
#ssh
ssh_username = 'ssh_user'
ssh_password = 'ssh_password'

headers = {
    'Content-Type': 'application/json'
}

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

def get_site_id():
    try:
        response = requests.get(url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
        response.raise_for_status()  # Raise an error for bad status codes
        site_informations = response.json()

        # Print the retrieved templates in JSON format
        print(json.dumps(site_informations, indent=4))

        # Find the template ID by name
        for site in site_informations:
            if site["name"] == site_name:
                site_id = site["id"]
                print(f"This is the site ID for {site_name}: {site_id}")
                return site_id

        print(f"No site found with the name {site_name}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_template_id():
    # Authenticate and get the token

    response = requests.get(template_api_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), headers=headers)
    response.raise_for_status()
    templates = response.json()
    # Find the template ID by name
    for template in templates:
        if template["name"] == template_name:
            template_id = template["id"]
            print("Template ID" + template_id)
            return template_id
    return None


def assign_template_to_site(site_id, template_id):
    site_url = f'https://api.eu.mist.com/api/v1/sites/{site_id}'
    response = requests.get(site_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD))
    if response.status_code != 200:
        print(f"Failed to retrieve template: {response.status_code} - {response.text}")
        exit()

    template_data = response.json()
    template_data['gatewaytemplate_id'] = template_id

    response = requests.put(site_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), json=template_data)
    print("The URL:" + site_url)
    print(response.json)
    if response.status_code == 200 and response.status_code == 201:
        print("Template assigned successfully!")
    else:
        print(f"Failed to assign template: {response.status_code} - {response.text}")


if __name__ == '__main__':
    #get_site_id()
    assign_template_to_site(get_site_id(),get_template_id())
