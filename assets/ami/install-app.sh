#!/bin/bash
echo "[ACTIVATE ENVIRONMENT]"
source lab-sysadmin-env/bin/activate
echo "[CREATE FOLDERS]"
mkdir -p /home/ubuntu/lab-sysadmin-data
cd /home/ubuntu
chmod 755 lab-sysadmin-data/
echo "[UPDATE REPOSITORY]"
cd /home/ubuntu/lab-sysadmin
git pull
echo "[UPDATE DEPENDENCIES]"
pip3 install -r application/requirements.txt
echo "[CONFIGURING APP .CONF]"
sudo rm -r /etc/nginx/sites-enabled
sudo mkdir /etc/nginx/sites-enabled
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/application /etc/nginx/sites-enabled/application
sudo service nginx restart
echo "[CONFIGURING APP .SERVICE]"
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl daemon-reload
sudo systemctl start application
echo "[STARTING APP]"
sudo systemctl restart application
echo "[STARTING CRAWLER]"
cd /home/ubuntu
source lab-sysadmin-env/bin/activate
cd /home/ubuntu/lab-sysadmin/application
kill -9 `pgrep -f "python metrics_crawler.py"`
nohup python metrics_crawler.py &