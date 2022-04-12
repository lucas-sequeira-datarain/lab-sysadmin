#!/bin/bash
sudo apt update
sudo apt install python3-pip -y
sudo apt install nginx -y
pip3 install virtualenv
virtualenv app-env