#!/usr/bin/env python
import requests
import json
import random
import time

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
for i in range(10):
    random_item1 = random.choice(json_data)
    random_item2 = random.choice(json_data)
    print "[+] Updating {} config's data with {} config's data".format(random_item1["name"], random_item2["name"])
    data = {"data": random_item2["data"]}
    res = requests.put(url=URL+random_item2["name"].strip(), headers=headers, data=json.dumps(data))
    print "    [*] [PUT] HTTP Status code for the config {0} is {1}".format(random_item1["name"], res.status_code)
    print "    [*]Response Text ->", res.text
    time.sleep(1)