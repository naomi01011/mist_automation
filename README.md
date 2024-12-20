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
  
## Execute script
### Prerequisites
You need to install Python: https://phoenixnap.com/kb/how-to-install-python-3-windows

You need an SSH connection to the device your organization ID from your Mist Org and a token or your login data to log in to Mist.

Create a “config.py” to store your credentials there.
## Execution

```shell
py .\<name_of_your_script>.py
