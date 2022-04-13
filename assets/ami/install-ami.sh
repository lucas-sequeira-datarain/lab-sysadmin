#!/bin/bash
sudo apt update
sudo apt install python3-pip -y
sudo apt install nginx -y
sudo apt install python3-virtualenv
pip uninstall -y virtualenv
pip3 uninstall -y virtualenv
pip install virtualenv
virtualenv lab-sysadmin-env
