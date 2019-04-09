#!/usr/bin/env python
try:
    import requests
except ImportError:
    print "Install requests python module. pip install requests"
    exit(1)


try:
    f = open("ip")
    IP = f.read().strip()
except IOError:
    print "[-] The file 'ip' not found in current directory. Please run 'minikube ip > ip'"
    exit(1)
NODE_PORT = 32242

URL = "http://{}:{}/configs/".format(IP, NODE_PORT)

res = requests.get(url=URL)
print res.text
print "\n", res.status_code
