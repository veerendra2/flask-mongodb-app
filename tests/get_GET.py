#!/usr/bin/env python

import json
import time
try:
    import requests
except ImportError:
    print "Install requests python module. pip install requests"
    exit(1)

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def check_file(value):
    try:
        f = open(value)
        return f.read().strip()
    except IOError:
        print "[-] The file '{}' not found in current directory.".format(value)
        exit(1)


URL = "http://{}:{}/configs/".format(check_file("ip"), check_file("nodePort"))

try:
    f = open("sample_data.json")
except IOError:
    print "[-] sample_data.json file is missing"
    exit(0)
json_data = json.load(f)
print "[+] JSON Data Loaded"


with open("deleted_list.txt") as f:
    stored_list = f.readlines()

print GREEN+"[+] Trying fetch deleted items which should FAIL!"+ENDC
for config in stored_list:
    res = requests.get(url=URL+config.strip())
    print "[*] [GET] HTTP Status code for the config {0} is {1}".format(config.strip(), res.status_code)
    print "    [-] Response Text ->", res.text
    time.sleep(1)


with open("available_list.txt") as f:
    stored_list = f.readlines()

print GREEN+"[+] Trying fetch available items which should SUCCESS!"+ENDC
for config in stored_list:
    res = requests.get(url=URL+config.strip())
    print "[*] [GET] HTTP Status code for the config {0} is {1}".format(config.strip(), res.status_code)
    print "    [-] Response Text ->", res.text
    time.sleep(1)
