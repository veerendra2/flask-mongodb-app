#!/usr/bin/env python
import json
import random
import time
try:
    import requests
except ImportError:
    print "Install requests python module. pip install requests"
    exit(1)


def check_file(value):
    try:
        f = open(value)
        return f.read().strip()
    except IOError:
        print "[-] The file '{}' not found in current directory.".format(value)
        exit(1)


URL = "http://{}:{}/configs/".format(check_file("ip"), check_file("nodePort"))
headers = {'Content-Type': 'application/json'}
try:
    with open("deleted_list.txt") as f:
        deleted_list = f.readlines()
except IOError:
    print "[-] sample_data.json file is missing"
    exit(0)


for items in deleted_list:
    res = requests.delete(url=URL + items.strip(), headers=headers)
    print "[*] [DELETE] HTTP Status code for the config {0} is {1}".format(items.strip(), res.status_code)
    print "    [-] Response Text ->", res.text
    time.sleep(1)


