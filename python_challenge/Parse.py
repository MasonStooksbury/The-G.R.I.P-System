#! python3

####### VERSION HISTORY #######
# Version 1: Added 'getIPs' function to allow for return of a list of valid IPs upon receiving valid text file
###############################

import re
import pprint

# Parses through a provided file and strips all of the IPs out
# Returns: A list of IPv4 addresses
# External Modifications: None
def getIPs(file_path):
    ''' Parses through file and loads them all into a list that is returned. Be sure you
            have a list to catch them all.

        Arguments:
            file_path: This is the complete path from main drive to file (e.g. C:\...\file.txt)
        Returns: list of IP addresses
        External Modifications: None
    '''
    
    # Regex for IPv4 address
    #valid_IPV4_regex = re.compile(r'\b(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\b')
    all_IPV4_format_regex = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    
    #'valid' will only display valid IPs, where as 'all' will display any set of numbers with a dot format
    #       similar to that of IPv4. I went with 'all' because there were several 'non-valid' addresses
    #       in 'valid' and vice versa. Better to just keep them all and let the URL decide which ones
    #       are legit


    # List to hold all of the extracted IPs for returning
    return_list = []

    # Essentially will only break if 'file_path' doesn't exist or code is messed with
    try:
        with open(file_path, 'r') as myfile:
            data = myfile.read().replace('\n', '')
            disjoint_ip_list = all_IPV4_format_regex.findall(data)
            
            for ip in disjoint_ip_list:
                #new_ip_format = ".".join(ip)
                return_list.append(ip)#new_ip_format)
            

    except:
        print("File not found or error in 'getIPs' function")

    # Return our list of IP addresses
    return return_list





##### MAIN #####
if __name__ == '__main__':

    # Archived for later so I know what I'm doing

    '''
    FULL_PATH = "C:\\Users\\MasonStooksbury\\Documents\\PythonScripts\\Scripts\\Swimlane_Homework\\"

    file = 'list_of_ips.txt'
    
    IPs = getIPs(file)

    pprint.pprint(IPs)
    '''
    print("Hello, World")











    
