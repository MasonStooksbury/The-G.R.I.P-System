#! python3

# CLI_Driver.py - A script that handles the driving for the CLI version of the G.R.I.P. System

####### VERSION HISTORY #######
# Version 1: I did everything at once. It can display all GeoIP and RDAP data for a single IP
#               or file of IPs
###############################

import Parse as par
import GEOIP as geo
import RDAP as rdap
import Filter as filt
import pprint
import os.path

# Global variables corresponding to all of the many 'while' loops that exist
MAIN_LOOP = True
SINGLE_LOOP = True
FILE_LOOP = True
GEO_LOOP = True
RDAP_LOOP = True





##### MAIN #####


# Here is the structure (It'll make more sense as you go, I promise):
#       #############
#           ---------
#           ---------
#           ---------
#       #############
#       #############



print("Welcome to The G.R.I.P. System!")

while (MAIN_LOOP != False):
    SINGLE_LOOP = True
    FILE_LOOP = True
    GEO_LOOP = True
    RDAP_LOOP = True

    print('''\n\nPlease select an option:
    [1] Single IP
    [2] File with IPs
    [3] Quit
    [4] About''')

    ip_choice = input()


    # Single IP   ##################################################
    if ip_choice == '1':
        while (SINGLE_LOOP != False):
            print("\n\nWhat is your IP address?")
            IP = input()
            valid_IP = filt.validateIP(IP)

            print('''\n\nWhat type of data would you like to see?:
    [1] GeoIP
    [2] RDAP
    [3] <--''')
            
            data_choice = input()

       # GeoIP ---------------------
            if data_choice == '1':
                while (GEO_LOOP != False):
                    print('''\n\nWhat would you like to see?:
    ~ ip                         You should know this one
    ~ host                       IP address of Host
    ~ isp                        Provider of Internet Services
    ~ city                       City location of IP
    ~ c_code                     Country code of IP (e.g. United States = US)
    ~ c_name                     Country name of IP (e.g. United States)
    ~ lat                        Latitudinal coordinate for IP
    ~ long                       Longitudinal coordinate for IP

    Let's say you wanna see the IP address, isp, and c_code. You would type
        only what is in the parenthesis:    (ip isp c_code)
        
    If you want to see everything, just hit "space" and then "enter".
    
    Get the pattern?    Just type whatever you want to see with a space in
    between. I'll handle the rest. And if you screw it up, I'll let you know :)\n''')

                    # A string of filters
                    filter_choice = input()

                    # A list of separated filters
                    bool_list = filt.getBoolList(filter_choice)

                    # Blank dictionary to hold filter-arguments
                    arg_dictionary = {}

                    # Assign all the filters as True
                    for item in bool_list:
                        arg_dictionary[str(item)] = True

                    # Catch just in case filter-arguments are garbage
                    try:
                        geo.printGEO(geo.getIPData(IP), **arg_dictionary)
                    except:
                        print("\nIncorrect format or filters. Please try again\n\n")
                        break

                    print('''\n\nNow what?:
    [1] Do another filtering!
    [2] Quit''')
                    choice = input()
                    if choice == '2':
                        GEO_LOOP = False
                        SINGLE_LOOP = False
                        break
                    

       # RDAP ---------------
            elif data_choice == '2':
                while (RDAP_LOOP != False):
                    print('''\n\nWhat would you like to see?:
    [1] Most Recent Update Entry (by "registration")
    [2] Most Recent Update Entry (by "last_changed")
    [3] Oldest Update Entry (by "registration")
    [4] Oldest Update Entry (by "last_changed")
    [5] All Update Entries
    [6] Main RDAP Info (This is really the only one worth viewing)
    [7] Quit''')
                    rdap_option = input()
                    print('\n\n')

                    # MR by registration
                    if rdap_option == '1':
                        rdap.printEntryInfo(rdap.returnMostRecentUpdateEntry(IP, 1))

                    # MR by last changed
                    elif rdap_option == '2':
                        rdap.printEntryInfo(rdap.returnMostRecentUpdateEntry(IP, 0))

                    # Oldest by registration
                    elif rdap_option == '3':
                        rdap.printEntryInfo(rdap.returnOldestUpdateEntry(IP, 1))

                    # Oldest by last changed
                    elif rdap_option == '4':
                        rdap.printEntryInfo(rdap.returnOldestUpdateEntry(IP, 0))

                    # All
                    elif rdap_option == '5':
                        input()

                    # Main
                    elif rdap_option == '6':
                        print('''\n\nWhat would you like to see?:
    ~ registration                        When the entry was created
    ~ handle                              DNR/RIR registry-unique identifier
    ~ ipVersion                           v4 or v6
    ~ name                                Unique identifier of network registration by registration holder
    ~ objectClassName                     Specifies object class (e.g. "ip network", "Domain", etc)
    ~ parentHandle                        RIR-unique identifier of parent network for this network registration
    ~ port43                              WHOIS port (Website host shown)
    ~ rdapConformance                     Specifies conformance level
    ~ startAddress                        IP with last octet not specified (starting address of network)

    Let's say you wanna see the IP address, isp, and c_code. You would type
        only what is in the parenthesis:    (ip isp c_code)
        
    If you want to see everything, just hit "space" and then "enter".
    
    Get the pattern?    Just type whatever you want to see with a space in
    between. I'll handle the rest. And if you screw it up, I'll let you know :)\n''')

                        # A string of filters
                        filter_choice = input()

                        # A list of separated filters
                        bool_list = filt.getBoolList(filter_choice)

                        # Blank dictionary to hold filter-arguments
                        arg_dictionary = {}

                        # Assign all the filters as True
                        for item in bool_list:
                            arg_dictionary[str(item)] = True

                        # Catch just in case filter-arguments are garbage or IP fails
                        try:
                            rdap.printRdapIPInfo(IP, **arg_dictionary)
                            if not valid_IP:
                                print("\nInvalid or reserved IP. Please try again")
                                break
                        except:
                            print("\nIncorrect format or filters. Please try again.\n\n")
                            break

                        print('''\n\nNow what?:
        [1] Do another filtering!
        [2] Quit to Main''')

                        choice = input()
                        if choice == '2':
                            RDAP_LOOP = False
                            SINGLE_LOOP = False
                            break

                    # Quit
                    elif rdap_option == '7':
                        RDAP_LOOP = False
                        SINGLE_LOOP = False
                        break
                    
                
       # <--   ------------------------------
            elif data_choice == '3':
                break
        
        


    # File IP ##################################################################
    elif ip_choice == '2':
        while (FILE_LOOP != False):
            valid_file = False
            while (valid_file != True):
                print('\n\nGimme a file path! I loooove files (Either absolute path or make sure file is in the same directory)')
                file_path = input()
                valid_file = os.path.isfile(str(file_path))
                if not valid_file:
                    print("\n\nNot a valid file. Please try again.")
                    break
                
            if valid_file:
                print('''\n\nWould data would you like to see for all of the IPs?:
        [1] GeoIP     Will display which IPs were invalid/reserved
        [2] RDAP      Will not print invalid/reserved IPs
        [3] <--''')

                data_choice = input()
        
                IPs = par.getIPs(file_path)

                # GeoIP
                if data_choice == '1':
                    for ip in IPs:
                        #print(ip)
                        geo.printGEO(geo.getIPData(ip))
                   
                # RDAP
                elif data_choice == '2':
                    for ip in IPs:
                        #print(ip)
                        result = rdap.printRdapIPInfo(ip)

                # <--
                elif data_choice == '3':
                    break

    # Quit  ######################################################
    elif ip_choice == '3':
        break

    # About #########################################################
    elif ip_choice == '4':
        print('''\n\nThe [G]eoIP [R]DAP [I]nternet [P]rotocol System or "G.R.I.P. System" is a platform
designed to fetch data about a particular IP address and return it to the user in a variety of ways.
All data is derived from GeoIP and RDAP.\n\n''')

        about = {'Code-Weaver': 'Mason Stooksbury',
                 'Date': 'August 9-12, 2018',
                 'OS': 'Windows 8.1 (Old, right?)',
                 'Python Version': '3.6.4 (Also old, I know)',
                 'Workstation': "Good ol' IDLE",
                 'Email': 'masonstooksbury@gmail.com',
                 'Location': 'Cookeville, TN',
                 'Hours Logged': 'Easily over 30. Easy...'
                 }

        for key, val in about.items():
            pprint.pprint(key.ljust(20, '.') + val.rjust(30, ' '))














                  
