#!/usr/bin/env python
import json
import random
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


try:
    f = open("sample_data.json")
except IOError:
    print "[-] sample_data.json file is missing"
    exit(0)
json_data = json.load(f)
print "[+] JSON Data Loaded"

with open("available_list.txt") as f:
    stored_list = f.readlines()

with open("deleted_list.txt") as f:
    deleted_list = f.readlines()


def search_item(value):
    for item in json_data:
        if item["name"].strip() == value.strip():
            return item["data"]


def run_query(stored_list):
    for item in stored_list:
        data_values = search_item(item.strip())
        try:  # Because in sample_data.json, we made one wrong format like for "data" key -> {"id": "value"} instead of list
            ran_dict = random.choice(data_values)  # Each 'data' key has array of dicts. select one randomly
        except KeyError:
            pass
        for key, value in ran_dict.items():
            PARAMS = [{"name": item.strip(), "data.{}".format(key): value}, {"data.{}".format(key): value} ]
            for param in PARAMS:
                URL = "http://{}:{}/search".format(check_file("ip"), check_file("nodePort"))
                res1 = requests.get(URL, params=param)
                print "[*] [GET] {}  HTTP response code: {}".format(res1.url, res1.status_code)
                print "   [+] Query Result -> {}".format(res1.text)
            print "\n"
            time.sleep(1)


print GREEN+"[*] Starting query on available_list which should success/return results"+ENDC
time.sleep(2)
run_query(stored_list)
print GREEN+"[*] Starting query on deleted_list which should fail/no results"+ENDC
time.sleep(2)
run_query(deleted_list)

