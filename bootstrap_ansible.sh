#! /bin/bash

PYTHONUNBUFFERED=1 ansible-playbook -i /home/vagrant/hosts /vagrant/provision_vagrant.yml 
