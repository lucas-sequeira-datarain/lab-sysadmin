#!/bin/bash
source lab-sysadmin-env/bin/activate
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git
cd lab-sysadmin
pip3 install -r application/requirements.txt
sudo cp assets/ami/lab-sysadmin-appserver.service /etc/systemd/system/lab-sysadmin-appserver.service
systemctl start lab-sysadmin-appserver
000000
systemctl daemon-reload
000000
sudo cp assets/ami/lab-sysadmin-appserver /etc/nginx/sites-available/lab-sysadmin-appserver
sudo ln -s /etc/nginx/sites-available/lab-sysadmin-appserver /etc/nginx/sites-enabled
systemctl restart nginx
000000