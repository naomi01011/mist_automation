# mist_automation on Windows

## Benutzte Tools
* https://api.eu.mist.com/api/v1/docs/Home
* PyCharm or VisualStudioCode
* Postman
  * Mist Runner Collection
  * Mist Cloud API
* Mist Browser Extension
* Python
 * Libaries
   * junos-eznc
   * requests
   * pandas

## About Scripts
### assign_template_to_site.py
It will assign a template of your choice to a given site within your Mist organisation

### assign_IP_to_device.py
It will assign a static ( reserved ) IP-address to a device.
For that you will have to use a datasheet.

### create_gateway_template.py
It will create a Wan Edge template, based on the configration of an SRX device

## Execute script
### Prerequisites
You need to install Python: https://phoenixnap.com/kb/how-to-install-python-3-windows

You need an SSH connection to the device your organization ID from your Mist Org and a token or your login data to log in to Mist.

Create a “config.py” to store your credentials there.

### Execution

```shell
py .\<name_of_your_script>.py
