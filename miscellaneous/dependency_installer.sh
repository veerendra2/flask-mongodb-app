#!/usr/bin/env bash
sudo apt update
sudo apt install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common python-pip
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
echo "[*] Installing Docker"
sudo apt-get install docker-ce
echo "[*] Installing requests python module"
sudo pip install requests
#echo "[*] Downloading minikube binary"
#curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64 \
#  && chmod +x minikube
#sudo cp minikube /usr/local/bin && rm minikube
#echo "[*] Launching minikube cluster"
#minikube start