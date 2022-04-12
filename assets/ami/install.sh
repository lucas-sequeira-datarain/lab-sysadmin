#!/bin/bash
sudo su -
passwd ubuntu
000000
000000
sudo apt update
sudo apt install python3-pip -y
sudo apt install nginx -y
pip3 install virtualenv
virtualenv lab-sysadmin-env
source lab-sysadmin-env/bin/activate
