# python_challenge: The G.R.I.P. System
A script that allows lots of manipulation for GeoIP and RDAP data for a given IP address (or file with IP addresses in it)


The [G]eoIP [R]DAP [I]nternet [P]rotocol System or "G.R.I.P. System" is a platform designed to fetch data about a particular IP address and return it to the user in a variety of ways. All data is derived from GeoIP and RDAP.

---

# Python Version:
  3.6.4
  
---


# Dependencies:
To make this easy, here are all of the imports I have across all files. A lot of them come with Python, but just in case you're curious:
  import urllib.request
  import urllib.parse
  import pprint
  import json
  import re
  import requests
  import dateutil.parser
  import datetime
  import os.path
  
---
  
# How do I use this thing?:
Clone the repository wherever you want it, and run it by either:
  1. Clicking the 'CLI_Driver.py' file. 
  2. Opening 'CLI_Driver.py' in IDLE and running with 'F5'.
  3. Creating your own batch file to run it (bear in mind that if you run it this way or run it from the CLI, if you use the 'file' functionality, you will need to use the absolute path for the file).
    
    1 and 2 are preferred because:
        You can just put text files next to the script and only use the file name and extension (e.g. "file.txt")
    Otherwise:
        You have to use the absolute path (gross! Who programmed this?) (e.g. "C:\Users\MasonStooksbury\......\file.txt"
        
        
 ---
 
        
 # Anything Else?:
 I don't think so. I tried to make this as simple as possible. If you have any further questions or curiosities, play around with it!
 
 Or you can check out the demo video coming up soon!
