#! python3

# GEOIP.py - A script that handles GeoIP stuff

####### VERSION HISTORY #######
# Version 1: Added 'getIPData' to find relevant GEOIP data about provided IP
#            Added 'printGEO' to print found data about IP
# Version 2: Edited 'printGEO' to print only desired info. If all are false, it will print everything
#            
###############################

import urllib.request
import urllib.parse
import pprint
import json
import re

# Free from: https://rdap.apnic.net    
RDAP_addr = 'https://rdap.apnic.net/ip/{}'

# Free from:     http://geoiplookup.net/xml-api/
GEOIP_addr = 'http://api.geoiplookup.net/?query={}'

# Free with API Key from:     https://ipstack.com/quickstart
GEOIP_more = 'http://api.ipstack.com/{0}?access_key=d81366ea95d6cef38e7bc524c8a88a09'#&output={1}'




# Visits the GEOIP site to grab the GEOIP data
# Returns: respData for parsing
# External Modifications: None
def getIPData(ip):
    '''Visits the GEOIP site to grab the GEOIP data

        Arguments:
            ip: String version of the IP address
        Returns: respData for parsing
        External Modifications: None
    '''

    # Will fail if IP is not valid
    try:
        GEO_URL = GEOIP_addr.format(ip)
        resp = urllib.request.urlopen(GEO_URL)
        respData = resp.read()
    except:
        respData = (str(ip) + " was not a valid IP (Error 404)")
        
    return respData

# Prints all of the GEOIP data for a given IP with filter parameters
# Returns: Nothing
# External Modifications: None
def printGEO(respData, ip=False, host=False, isp=False, city=False, c_code=False, c_name=False, lat=False, long=False):
    '''Prints all of the GEOIP data for a given IP with filter parameters

        Arguments:
            respData: Response data from GEOIP request
            ip: Displays IP address
            host: Displays Host IP address
            isp: Displays Internet Service Provided
            city: Displays IP city
            c_code: Displays the country code (e.g. United States = US)
            c_name: Displays the country name (e.g. United States)
            lat: Displays the latitude for the given IP address
            long: Displays the longitude for the given IP address
        Returns: Nothing
        External Modifications: None
    '''

    
    # Used for validating IP address
    valid_ip = True
    not_valid_ip = respData

    # See if the IP is valid.
    # This will enter except only when respData is byte data, indicating its been returned from the URL
    #           in a JSON format
    # Clunky, but it works well.
    
    try:
        if '(Error 404)' in respData:
            valid_ip = False

    except:
        not_valid_ip = respData


    # If the IP has been proven valid, continue
    if valid_ip:

        # A list of all of the passed in and default values
        bool_list = [ip, host, isp, city, c_code, c_name, lat, long]

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

        #IP
        ip_tag = re.findall(r'<ip>(\d.*?)</ip>', str(respData))
        
        #HOST
        host_tag = re.findall(r'<host>(.*?)</host>', str(respData))
        
        #ISP
        isp_tag = re.findall(r'<isp>(.*?)</isp>', str(respData))
        
        #CITY
        city_tag = re.findall(r'<city>(.*?)</city>', str(respData))
        
        #COUNTRYCODE
        c_code_tag = re.findall(r'<countrycode>(.*?)</countrycode>', str(respData))
        
        #COUNTRYNAME
        c_name_tag = re.findall(r'<countryname>(.*?)</countryname>', str(respData))
        
        #LATITUDE
        lat_tag = re.findall(r'<latitude>(.*?)</latitude>', str(respData))
        
        #LONGITUDE
        long_tag = re.findall(r'<longitude>(.*?)</longitude>', str(respData))

        # Store everything in a dictionary for "Pretty Printing" later
        GEO_Data = {'IP': ip_tag,
                    'HOST': host_tag,
                    'ISP': isp_tag,
                    'CITY': city_tag,
                    'COUNTRY CODE': c_code_tag,
                    'COUNTRY NAME': c_name_tag,
                    'LATITUDE': lat_tag,
                    'LONGITUDE': long_tag
                    }

        print('\n\n')
        
        # bool_list index from above
        list_count = 0

        # Print only those the user asked for.
        # If none were specified, print everything
        for key, val in GEO_Data.items():
            if bool_list[list_count]:
                pprint.pprint(key.ljust(20, '.') + str(val).rjust(30, ' '))
            list_count += 1
        print('\n\n')

    # IP was not valid, print so to the screen
    else:
        print(not_valid_ip)

    return
    


##### MAIN #####
if __name__ == '__main__':
    print("Hello, World!")

    

    

