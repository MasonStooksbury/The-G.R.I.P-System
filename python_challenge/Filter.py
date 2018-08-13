#! python3

# Filter.py - A script that handles anything related to filtering

####### VERSION HISTORY #######
# Version 1: Added 'getBoolList' function to return a list of items in string
#            Added 'validateIP' function to validate IPs for the driver
###############################

import requests
import json



# Splits a list of items to their individual components
# Returns: List of items found in provided string
# External Modifications: None
def getBoolList(string):
    '''Splits a list of items to their individual components

        Arguments:
            string: Provided string with space-delimited things in it
        Returns: List of items found in provided string
        External Modifications: None
    '''
    
    return string.split()

# Validates provided IP address
# Returns: Boolean
# External Modifications: None
def validateIP(IP):
    '''Validates provided IP address

        Arguments:
            IP: String IP address
        Returns: Boolean
        External Modifications: None
    '''

    # Free site to lookup RDAP 
    RDAP_addr = 'https://rdap.apnic.net/ip/{}'

    # Jam out IP into the curly braces of 'RDAP_addr'
    RDAP_URL = RDAP_addr.format(IP)

    # Go to RDAP URL and bring up specific IP info
    response = requests.get(RDAP_URL)
    
    # Grab the text and load it here in JSON format
    rdap_text = json.loads(response.text)

    # Validate by checking if there is an 'errorCode' section with '404' in it
    try:
        if rdap_text['errorCode'] == '404':
            return False
    except:
        return True
    
    return




##### MAIN #####
if __name__ == '__main__':
    #getBoolList('ip isp c_code')
    print("Hello, World!")











    
