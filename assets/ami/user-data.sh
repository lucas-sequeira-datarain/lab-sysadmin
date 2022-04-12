#!/bin/bash
source lab-sysadmin-env/bin/activate
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git
cd lab-sysadmin
pip3 install -r application/requirements.txt
sudo cp assets/ami/lab-sysadmin-appserver.service /etc/systemd/system/lab-sysadmin-appserver.service
systemctl start lab-sysadmin-appserver
000000