#! /bin/bash


sudo apt-get update
# install requirements for ansible and python
sudo apt-get install -y curl apt-transport-https python-setuptools libmariadb-dev
sudo apt-get install ansible -y --no-install-recommends
# run ansible provisioning tasks
PYTHONUNBUFFERED=1 ansible-playbook -i "localhost," -c local /vagrant/provision_vagrant.yml
