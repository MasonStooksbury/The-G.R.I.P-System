#! python3

# RDAP.py - Handles all of the RDAP stuff

####### VERSION HISTORY #######
# Version 1: Able to grab RDAP information, export to JSON, and print to console
# Version 2: Added 'getRDAPText' function to visit RDAP site and grab the JSON text
#            Added 'convertToHumanDatetime' function to change string time format to more readable string
#            Added 'convertToDatetime' function to change string time format to datetime object
#            Added 'returnMostRecentUpdateEntry' function to return most recent update entry based on registration
#                   or last_changed
#            Added 'returnOldestUpdateEntry' function to return most recent update entry based on registration
#                   or last_changed
#            Added 'printRdapIPInfo' function to print the main RDAP info
#            Added 'printEntryInfo' function to print info for a specific entry
#            Added 'printAllUpdateEntries' function to print info for all update entries
###############################

import urllib.request
import urllib.parse
import pprint
import json
import re
import requests
import dateutil.parser
import datetime

MONTHS = {'1': 'January',
          '2': 'February',
          '3': 'March',
          '4': 'April',
          '5': 'May',
          '6': 'June',
          '7': 'July',
          '8': 'August',
          '9': 'September',
          '10': 'October',
          '11': 'November',
          '12': 'December'
          }



# Free from: https://rdap.apnic.net    
RDAP_addr = 'https://rdap.apnic.net/ip/{}'

# Homemade function to act as a very specialized lambda-esque try/except (See 'printRdapIPInfo')
# Returns: String of element at arg2 position of arg1
# External Modifications: None
def tryExcept(text, thing):
    '''Homemade function to act as a very specialized lambda-esque try/except (See 'printRdapIPInfo')

        Arguments:
            text: String
            thing: String
        Returns: String of element at arg2 position of arg1
        External Modifications: None
    '''
    
    try:
        item = text[thing]
        return str(item)
    except:
        return ''


# Visits RDAP site to grab RDAP info about provided IP
# Returns: Text of RDAP info in JSON layout OR error message
# External Modifications: Visits website utilizing 'requests' module
def getRDAPText(IP):
    '''Visits RDAP site to grab RDAP info about provided IP

        Arguments:
            IP: String version of IP address
        Returns: Text of RDAP info in JSON layout
        External Modifications: Visits webstie utilizing 'requests' module
    '''

    # Concatenate URL with specified IP address
    RDAP_URL = RDAP_addr.format(IP)

    # Go to RDAP URL and bring up specific IP info
    response = requests.get(RDAP_URL)
    
    # Grab the text and load it here in JSON format
    rdap_text = json.loads(response.text)

    # If the rdap_text contains a 404 error code, return error string
    try:
        if rdap_text['errorCode'] == '404':
            rdap_text = (str(IP) + " was not a valid IP or is reserved by the IANA")
    except:
        return rdap_text
    
    return

# Converts provided date into something more readable (e.g. 2018-07-05   --->   July 5, 2018)
# Returns: list of MONTH, DAY, and YEAR for manipulation by later print function
# External Modifications: None
def convertToHumanDatetime(date):
    '''Converts provided date into something more readable (e.g. 2018-07-05 ---> July 5, 2018)

        Arguments:
            date: String version of date
        Returns: list of MONTH, DAY, and YEAR for manipulation by later print function
        External Modification: None
    '''

    # Take string 'date' and make it a datetime object
    new_date = dateutil.parser.parse(date)

    # Grab the relevant info from datetime object (namely: MONTH, DAY, and YEAR)
    date_string_list = [new_date.month, new_date.day, new_date.year]
    
    return date_string_list

# Converts string to a Datetime object
# Returns: Datetime object
# External Modifications: None
def convertToDatetime(date):
    '''Converts string to a Datetime object

        Arguments:
            date: String version of a date
        Returns: Datetime object
        External Modifications: None
    '''
    
    new_date = dateutil.parser.parse(date)

    return new_date

# Calculates the most recent entry from the RDAP response based on its datetime
# Returns: String version of the JSON entry from RDAP response OR error message
# External Modifications: None
def returnMostRecentUpdateEntry(IP, option):
    '''Calculates the most recent entry from the RDAP response based on its datetime

        Arguments:
            IP: String version of IP address
            option: 0 for "last_changed"
                    1 for "registration"
        Returns: String version of the JSON entry from RDAP response OR error message
        External Modifications: None
    '''

    # Grab all of the RDAP text from the site in JSON layout
    full_RDAP_text = getRDAPText(IP)

    # Used for validating IP address
    valid_ip = True
    result = full_RDAP_text

    # See if the IP is valid.
    # This will enter except only when respData is byte data, indicating its been returned from the URL
    #           in a JSON format
    # Clunky, but it works well.
    
    try:
        if 'IANA' in full_RDAP_text:
            valid_ip = False

    except:
        result = full_RDAP_text
        return result

  
    # If the IP has been proven valid, continue
    if valid_ip:

        # Number of update event registries
        num_entries = len(full_RDAP_text["entities"][0]["entities"])

        count = 0
        times = []
        
        # Create a list of all the times in relation to today for each entry
        for time in range(num_entries):
            date = convertToDatetime(str(full_RDAP_text["entities"][0]["entities"][count]["events"][option]["eventDate"]))
            times.append((NOW - date).days)
            count += 1

        # This is the index of the most recent entry from the RDAP stuff
        most_recent = times.index(min(times))

        # Delete the list. If this scales to be super huge, we don't need this potentially massive list sitting around
        times = []

        result = full_RDAP_text["entities"][0]["entities"][most_recent]

        return result

    else:
        print(result)
        
    return

# Calculates the oldest entry from the RDAP response based on its datetime
# Returns: String version of the JSON entry from RDAP response
# External Modifications: None
def returnOldestUpdateEntry(IP, option):
    '''Calculates the oldest entry from the RDAP response based on its datetime

        Arguments:
            IP: String version of IP address
            option: 0 for "last_changed"
                    1 for "registration"
        Returns: String version of the JSON entry from RDAP response
        External Modifications: None
    '''

    # Grab full RDAP text from the site in JSON layout
    full_RDAP_text = getRDAPText(IP)

    # Used for validating IP address
    valid_ip = True
    result = full_RDAP_text

    # See if the IP is valid.
    # This will enter except only when respData is byte data, indicating its been returned from the URL
    #           in a JSON format
    # Clunky, but it works well.
    
    try:
        if 'IANA' in full_RDAP_text:
            valid_ip = False

    except:
        result = full_RDAP_text
        return result



    # If the IP has been proven valid, continue
    if valid_ip:

        # Number of update event registries
        num_entries = len(full_RDAP_text["entities"][0]["entities"])

        count = 0
        times = []
        
        # Create a list of all the times in relation to today for each entry
        for time in range(num_entries):
            date = convertToDatetime(str(full_RDAP_text["entities"][0]["entities"][count]["events"][option]["eventDate"]))
            times.append((NOW - date).days)
            count += 1

        # This is the index of the most recent entry from the RDAP stuff
        oldest = times.index(max(times))

        # Delete the list. If this scales to be super huge, we don't need this potentially massive list sitting around
        times = []

        result = full_RDAP_text["entities"][0]["entities"][oldest]

        return result

    else:
        print(result)

    return 

# Prints all of the relevant information regarding the initial RDAP entry (doesnt include subsequent update entry log)
# Returns: Nothing
# External Modifications: None
def printRdapIPInfo(IP, registration=False, handle=False, ipVersion=False, name=False, objectClassName=False, parentHandle=False, port43=False, rdapConformance=False, startAddress=False):
    '''Prints all of the relevant information regarding the initial RDAP entry (doesn't include subsequent update entry log)

        Arguments:
            IP: String version of IP address
        Returns: Nothing
        External Modifications: None
    '''

    # Get full RDAP text from site in JSON layout
    rdap_text = getRDAPText(IP)

    # Used for validating IP address
    valid_ip = True
    result = rdap_text

    # See if the IP is valid.
    # This will enter except only when respData is byte data, indicating its been returned from the URL
    #           in a JSON format
    # Clunky, but it works well.
    
    try:
        if 'IANA' in rdap_text:
            valid_ip = False

    except:
        result = rdap_text
        return result

    # If the IP has been proven valid, continue
    if valid_ip:

        # A list of all of the passed in and default values
        bool_list = [registration, handle, ipVersion, name, objectClassName, parentHandle, port43, rdapConformance, startAddress]

        # The number of values that are true
        true_num = 0

        # Discover how many values are true
        for item in bool_list:
            if item:
                true_num += 1

        # If all values are false, set all of them to true so we print everything later (see below)
        if true_num == 0:
            count = len(bool_list)
            for item in range(count):
                bool_list[item] = True

        # Get the date it was created and make it more readable
        date_list = convertToHumanDatetime(rdap_text["events"][0]["eventDate"])
        RDAPCreated = MONTHS[str(date_list[0])] + " " + str(date_list[1]) + ", " + str(date_list[2])

        # Archived (Old way I did it)
        '''
        handle = rdap_text['handle']
        ipVersion = rdap_text['ipVersion']
        name = rdap_text['name']
        objectClassName = rdap_text['objectClassName']
        parentHandle = rdap_text['parentHandle']
        port43 = rdap_text['port43']
        rdapConformance = rdap_text['rdapConformance']
        startAddress = rdap_text['startAddress']
        '''

        # Grabs all the stuff we want via a homemade try/except function
        handle = tryExcept(rdap_text, 'handle')
        ipVersion = tryExcept(rdap_text, 'ipVersion')
        name = tryExcept(rdap_text, 'name')
        objectClassName = tryExcept(rdap_text, 'objectClassName')
        parentHandle = tryExcept(rdap_text, 'parentHandle')
        port43 = tryExcept(rdap_text, 'port43')
        rdapConformance = tryExcept(rdap_text, 'rdapConformance')
        startAddress = tryExcept(rdap_text, 'startAddress')
        
        # Store everything in a dictionary to "Pretty Print" later
        RDAP_INFO = {'registration': RDAPCreated,
                     'handle': handle,
                     'ipVersion': ipVersion,
                     'name': name,
                     'objectClassName': objectClassName,
                     'parentHandle': parentHandle,
                     'port43': port43,
                     'rdapConformance': rdapConformance,
                     'startAddress': startAddress
                     }
        
        print('\n\n')

        list_count = 0

        # Print only those the user asked for
        # If none were specified, print everything
        for key, val in RDAP_INFO.items():
            if bool_list[list_count]:
                pprint.pprint(key.ljust(20, '.') + str(val).rjust(30, ' '))
            list_count += 1

    else:
        print(result)
        
    return

# Prints relevant data for a specified entry
# Returns: Nothing
# External Modifications: None
def printEntryInfo(rdap_text):
    '''Prints relevant data for a specified entry

        Arguments:
            rdap_text: This is the text for only one entry (e.g. if you ran printMostRecentUpdateEntry and piped that here)
        Returns: Nothing
        External Modifications: None
    '''

    # Get dates and make them more readable
    date_list = convertToHumanDatetime(rdap_text["events"][1]["eventDate"])
    RDAPCreated = MONTHS[str(date_list[0])] + " " + str(date_list[1]) + ", " + str(date_list[2])
    date_list = convertToHumanDatetime(rdap_text["events"][0]["eventDate"])
    RDAPUpdated = MONTHS[str(date_list[0])] + " " + str(date_list[1]) + ", " + str(date_list[2])

    # Grab relevant data from RDAP text
    handle = rdap_text['handle']
    objectClassName = rdap_text['objectClassName']
    port43 = rdap_text['port43']
    roles = rdap_text['roles']
    status = rdap_text['status']

    # Store in a dictionary for "Pretty Printing" later
    RDAP_INFO = {'registration': RDAPCreated,
                 'last changed': RDAPUpdated,
                 'handle': handle,
                 'objectClassName': objectClassName,
                 'port43': port43,
                 'roles': roles,
                 'status': status
                 }

    # How many items are in the 'vcardArray' entry block
    new_range = len(rdap_text['vcardArray'][1])

    # List of indices of desired data
    list_of_indices = []

    # Deleted in the process
    # We really only care about the helpful email, and helpful tel number
    want_list = ['email', 'tel']

    # Find the indices in 'vcardArray' of everything in our want_list
    for i in range(new_range):
        want_item = rdap_text['vcardArray'][1][i][0]
        
        if want_item in want_list:
            list_of_indices.append(i)
            want_list.remove(want_item)

    
    email = rdap_text['vcardArray'][1][int(list_of_indices[0])][3]
    tel = rdap_text['vcardArray'][1][int(list_of_indices[1])][3]
        

    VCARD_INFO = {
                  'email': email,
                  'telephone': tel
                  }
    

    # Print it all!
    for key, val in RDAP_INFO.items():
        pprint.pprint(key.ljust(20, '.') + str(val).rjust(30, ' '))

    for key, val in VCARD_INFO.items():
        pprint.pprint(key.ljust(20, '.') + str(val).rjust(30, ' '))
        
    return 

# Prints some info about all of the update entries for a given IP
# Returns: Nothing
# External Modifications: None
def printAllUpdateEntries(IP, option, reverse=False):
    '''Prints some info about all of the update entries for a given IP

        Arguments:
            IP: String version of an IP address
            option: 0 for "last_changed"
                    1 for "registration"
            reverse: Defaults to ascending if not specified
                     True for "descending"
                     False for "ascending"
        Returns: Nothing
        External Modifications: None
    '''

    # Returned RDAP data as text in JSON format
    full_RDAP_text = getRDAPText(IP)

    # Number of update event registries
    num_entries = len(full_RDAP_text["entities"][0]["entities"])

    # Counter to indicate which entry we are on
    count = 0

    # List to keep track of times
    times = []

    # Find out how far away (in days) each entry is from right now and store those numbers
    for time in range(num_entries):
        date = convertToDatetime(str(full_RDAP_text["entities"][0]["entities"][count]["events"][option]["eventDate"]))
        times.append((NOW - date).days)
        count += 1

    # If reverse has not been set above, we want to print in 'ascending' order
    if reverse != True:
        for time in sorted(times):
            printEntryInfo(full_RDAP_text["entities"][0]["entities"][times.index(int(time))])
            print('\n\n')
    # Otherwise, we want 'descending'
    else:
        for time in sorted(times, reverse=True):
            printEntryInfo(full_RDAP_text["entities"][0]["entities"][times.index(int(time))])
            print('\n\n')


# Datetime of right now in ISO-8601 format
# DO NOT MOVE -- uses function above
NOW = convertToDatetime(datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat())





##### MAIN #####
if __name__ == '__main__':
    print("Hello, World!")

    # Below is an ugly cheat sheet that I'm gonna save in case I ever come back to this and have
    #   NO idea what's going on.
    #V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V V



    
    #IP = '244.36.171.60'
    #IP = '107.73.246.73'
    #IP = '127.0.0.0' #Test IP that fails
    

    #pprint.pprint(getRDAPText(IP)) #<-- Print everything

    #num_entries = len(rdap_text["entities"][0]["entities"]) #<-- Number of update entries

    
    #pprint.pprint(rdap_text["entities"][0]["events"][0]) #<-- Grabs the entry at the bottom of the first entities block
    
    #pprint.pprint(rdap_text["entities"][0]["entities"][1]) #<-- Grabs each "entry" event

    #                                                  V   <-- Edit this index to flip through event registries
    #pprint.pprint(rdap_text["entities"][0]["entities"][0]["events"][0]["eventDate"]) #<-- Grabs the event datetime string from an entry



    # Ascending by last_changed
    
    #printAllUpdateEntries(IP, 0, reverse=True)
    #print('\n\n\n')

    

    # Ascending by registration
    
    #printAllUpdateEntries(IP, 1, reverse=True)
    #print('\n\n\n')



    # Descending by last_changed
    
    #printAllUpdateEntries(IP, 0)
    #print('\n\n')



    # Descending by registration
    #printAllUpdateEntries(IP, 1)

    

    







    
    
