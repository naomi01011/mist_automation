import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import json
import config

#Environment variable
site_id = 'your_site_id'
file_path = 'path_to_your_ip_address_datasheet'
df = pd.read_excel(file_path)
base_url = f'https://api.eu.mist.com/api/v1/sites/{site_id}/devices'
headers = {
    'Content-Type': 'application/json'
}


# Function to get device ID by device name
def get_device_information(device_name):
    response = requests.get(base_url, auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD), headers=headers)
    if response.status_code == 200:
        devices = response.json()
        for device in devices:
            if device['name'] == device_name:
                return device['id']
        return None
    else:
        print(f"Failed to fetch devices: {response.status_code}")
        return None

# Iterate over the rows in the excel sheet and get device IDs
def get_device_id_by_name():
    for index, row in df.iterrows():
        device_name = row['Device Name']
        device_id = get_device_information(device_name)
        if device_id:
            print(f'Device ID for {device_name} is {device_id}')
            return device_id
        else:
            print(f'Device ID for {device_name} not found')

# Iterate over the rows in the excel sheet and get network details
def get_network_information(device_id):
    url = f"{base_url}/{device_id}"

    for index, row in df.iterrows():
        device_name = row['Device Name']
        mac_address = row['MAC Address']
        ip_address = row['IP Address']
        netmask = row['Netmask']
        gateway = row['Gateway']
        dns = row['DNS'].split(',')

        data = {
            'ip_config': {
                'type': "static",
                'ip': ip_address,
                'netmask': netmask,
                'gateway': gateway,
                'dns': dns
            }
        }
        response = requests.put(url,auth=HTTPBasicAuth(config.USERNAME, config.PASSWORD),  headers=headers, json=data)
        response_json = response.json()   

        if response.status_code == 200:
            print(f'Successfully assigned IP {ip_address} to device {device_name} ({mac_address})')
        else:
            print(f'Failed to assign IP {ip_address} to device {device_name} ({mac_address}): {response_json}')
    print("All devices got assigned to a IP address!")


if __name__ == '__main__':
    print("###### Device ID ######")
    get_device_id_by_name()
    print("###### Assign fix IP to device ######")
    get_network_information(get_device_id_by_name())
