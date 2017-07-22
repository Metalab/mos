#! /bin/bash


sudo apt-get update
# install requirements for ansible APT repo
sudo apt-get install gnupg-curl apt-transport-https
sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
# add ansible APT repo and install ansible
echo 'deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main' | sudo tee /etc/apt/sources.list.d/ansible.list
sudo apt-get update
sudo apt-get install ansible -y --no-install-recommends
# run ansible provisioning tasks
PYTHONUNBUFFERED=1 ansible-playbook -i "localhost," -c local /vagrant/provision_vagrant.yml
