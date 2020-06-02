# Author: Veerendra K
# Description: Spawns VMs for testing

### BOXES LIST ###
#
# ubuntu/bionic64
# centos/7
# minimal/trusty64
# alpine/alpine64
# Example: https://www.thisprogrammingthing.com/2015/multiple-vagrant-vms-in-one-vagrantfile/


### MODIFY SCRIPT BELOW ACCORDING TO DISTRO ###

$web_script = <<-SCRIPT
apt-get update && apt-get upgrade -y
apt-get install python-pip apache2 apache2-dev -y
pip install flask pymongo
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.5.tar.gz 4.6.5.tar.gz
tar -xf 4.6.5.tar.gz \
    && cd mod_wsgi-4.6.5 \
	&& ./configure \
	&& make install
rm -rf /mod_wsgi-4.6.5
rm 4.6.5.tar.gz
apt-get autoremove -y
SCRIPT


$db_script = <<-SCRIPT
apt-get update && apt-get upgrade -y
apt-get install python-pip apache2 apache2-dev -y
sudo apt-get install mongodb -y
apt-get autoremove -y
SCRIPT


NODES_COUNT = 1
RAM_MB = 1024
CORE_COUNT = 2
BOX = "ubuntu/bionic64"


Vagrant.configure("2") do |config|

  (1..NODES_COUNT).each do |i|
    config.vm.define "web#{i}", primary: true do do |server|
      server.vm.box = BOX
      server.vm.hostname = "box#{i}"

      server.vm.provider "virtualbox" do |v|
        v.name = "web#{i}"
        v.memory = RAM_MB
        v.cpus = CORE_COUNT
      end
      server.vm.network "private_network", ip: "192.168.99.#{i+10}"

      # server.vm.network :forwarded_port, guest: 22, host: 10122
      # server.vm.synced_folder "../data", "/vagrant_data"
      # server.vm.provision "shell", path: "script_on_host.sh"

      server.vm.provision "shell", inline: $web_script
    end
  end

    config.vm.define "db" do |db|
    db.vm.box = "precise64"
    db.vm.hostname = 'db'
    db.vm.box_url = "ubuntu/precise64"

    db.vm.network :private_network, ip: "192.168.56.102"
    db.vm.network :forwarded_port, guest: 22, host: 10222, id: "ssh"

    db.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--memory", 512]
      v.customize ["modifyvm", :id, "--name", "db"]
    end

    server.vm.provision "shell", inline: $web_script
  end

end



