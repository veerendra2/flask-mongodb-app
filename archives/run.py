#!/usr/bin/env python
'''
Author: Veerendra Kakumanu
Description: Automated script to build, push docker images and launches pod in K8s
'''
import os
import ConfigParser
import subprocess
import base64

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'

DOCKER_BUILD_CMD = "docker build -t {}:{} ."
DOCKER_TAG_CMD = "docker tag {}:{} {}/{}/{}:{}"
DOCKER_PUSH_CMD = "docker push {}/{}/{}:{}"
DOCKER_LOGIN = "echo -n {} | sudo docker login {} --username={} --password-stdin"
CMDS = ["kubectl get pods", "docker ps"]
IMAGE_PULL_SECRETS = "kubectl create secret docker-registry regcred --docker-server={} --docker-username={} --docker-password={} --docker-email={}"

# Reading configuration file
try:
    if not os.path.exists("run.cfg"):
        print RED+"[-] run.cfg not found in current directory"+ENDC
        exit(1)
    config = ConfigParser.ConfigParser()
    status = config.read("run.cfg")
    if len(status) == 0:
        print "[-] Please check the configuration file run.cfg"
    REGISTRY = config.get("docker_registry", "registry")
    USERNAME = config.get("docker_registry", "username")
    PASWORD = config.get("docker_registry", "password")
    EMAIL = config.get("docker_registry", "email")
    TAG = config.get("docker_registry", "tag")
    BUILD_LOCATIONS = {
        "app": config.get("docker_registry", "frontend_image_name"),
        "db": config.get("docker_registry", "backend_image_name")
    }
    MONGO_USERNAME = config.get("db", "mongo_username")
    MONGO_PASSWORD = config.get("db", "mongo_password")
except ConfigParser.NoSectionError as e:
    print RED+"[-] Configuration error", str(e)+ENDC
    exit(1)

print BOLD+"*** Welcome to 'simple-flask-mongodb' app deployment process ****"+ENDC
print "The deployment process consists of below steps"
print "1. Docker image building for fronend and endend apps"
print "2. Docker image push to registry"
print "3. Configuration changes in K8s manifests files"
print "4. imagePullSecrets creation in K8s"
print "5. Application deployment in K8s"
print "\nPlease make sure you configure/install docker and K8s(minikube) or press control+c to abort"
res = raw_input("Are you ready to deploy the app?[y/N]> ")
if res.strip().capitalize() != "Y":
    exit(0)

# shell execute https://github.com/veerendra2/useless-scripts/blob/master/MyToolKit/executecmd.py
def execute(cmd, verbose=True):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = []
    while True:
        line = p.stdout.readline()
        out.append(line)
        if verbose:
            print line,
        if not line and p.poll() is not None:
            break
    if p.returncode != 0:
        print p.stderr.read().strip()
        return 1
    else:
        return ''.join(out).strip()


# Pre fight checks. Are we able to run these shell commands?
for pkg in CMDS:
    if execute("{} > /dev/null".format(pkg)) == 1:
        print RED+"[-] Not able run {}. Please install/configure packages".format(pkg)+ENDC
        exit(1)

# Docker login into registry. Required to push docker images
print GREEN+"[+] Attempting to login into {}".format(REGISTRY)+ENDC
if execute(DOCKER_LOGIN.format(PASWORD, REGISTRY, USERNAME)) == 1:
    exit(1)

# Build Docker Images and pushing to registry
for location, image in BUILD_LOCATIONS.items():
    os.chdir(location)
    print GREEN+"[+] Building docker image {}".format(image)+ENDC
    if execute(DOCKER_BUILD_CMD.format(image, TAG)) == 1:
        exit(1)
    print GREEN+"[+] Tagging :: {}:{} -> {}/{}/{}:{}".format(image, TAG, REGISTRY, USERNAME, image, TAG)+ENDC
    if execute(DOCKER_TAG_CMD.format(image, TAG, REGISTRY, USERNAME, image, TAG))  == 1:
        exit(1)
    print GREEN+"[+] Pushing docker image {} to {}".format(image, REGISTRY)+ENDC
    if execute(DOCKER_PUSH_CMD.format(REGISTRY, USERNAME, image, TAG)) == 1:
        exit(1)
    os.chdir("..")

# Writing credentials to mongodb_secrets.yml
print GREEN+" [+] Writing mongodb credentials to mongodb_secrets.yml"+ENDC
with open("k8s/templates/temp_mongodb_secrets.yml") as f:
    modfied_conent = f.read().replace("username: b64content", "username: {}".format(base64.b64encode(MONGO_USERNAME)))
    modfied_conent = modfied_conent.replace("password: b64content", "password: {}".format(base64.b64encode(MONGO_PASSWORD)))
with open("k8s/mongodb_secrets.yml", "w") as f:
    f.writelines(modfied_conent)

# imagePullSecrets required to pull private images
print GREEN+" [+] Creating 'imagePullSecrets' secrets in K8s"+ENDC
if execute(IMAGE_PULL_SECRETS.format(REGISTRY, USERNAME, PASWORD, EMAIL)) == 1:
    print RED+"[-] 'imagePullSecrets' creation failed. Please create it manually or delete it if already exits"+ENDC
    exit(1)

# Verification
print GREEN+"[+] Verifying imagePullSecrets' secrets in K8s"+ENDC
if execute("kubectl get secrets regcred") == 1:
    print RED+"[-] imagePullSecrets' creation failed. Please create it manually"+ENDC
    exit(1)

# Launching pods in K8s cluster
print GREEN+"[+] Launching application in K8s"+ENDC
execute("kubectl create -f k8s/mongodb_secrets.yml")
execute("kubectl create -f k8s/mongoDB.yml")
execute("kubectl create -f k8s/http_service.yml")

print BOLD+GREEN+"Done!"+ENDC
print BOLD+"\nPlease run 'minikube ip > tests/ip'"
print BOLD+"\nTIP: Once pods are up, run 'minikube service http-service' and goto /configs/ endpoint to check the status"+ENDC





