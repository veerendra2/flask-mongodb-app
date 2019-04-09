#!/usr/bin/env python
import json
import time
import random
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
    f = open("sample_data.json")
except IOError:
    print "[-] sample_data.json file is missing"
    exit(0)
json_data = json.load(f)
print "[+] JSON Data Loaded"


store_items = list()
for count, items in enumerate(json_data):
    res = requests.post(url=URL, headers=headers, data=json.dumps(items))
    print "[*] [POST] HTTP Status code for the config {0} is {1}".format(items["name"], res.status_code)
    if count <= 10:  # 10 Good items that are stored in DB which are useful other tests
        store_items.append(items["name"])
    if res.status_code != 200:
       print "    [-] Error ->", res.text
    time.sleep(1)
