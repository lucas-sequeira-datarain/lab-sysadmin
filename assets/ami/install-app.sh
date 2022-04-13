#!/bin/bash
echo "[ACTIVATE ENVIRONMENT]"
source lab-sysadmin-env/bin/activate

# Update repo
echo "[UPDATE REPOSITORY]"
cd /home/ubuntu/lab-sysadmin
git pull

# Install dependencies
echo "[UPDATE DEPENDENCIES]"
pip3 install -r application/requirements.txt

# .conf file
echo "[CONFIGURING APP .CONF]"
sudo rm -r /etc/nginx/sites-enabled
sudo mkdir /etc/nginx/sites-enabled
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/application /etc/nginx/sites-enabled/application
sudo service nginx restart
# sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/

# .service file
echo "[CONFIGURING APP .SERVICE]"
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl daemon-reload
sudo systemctl start application
sudo systemctl status application



# App
echo "[STARTING APP]"
# sudo systemctl daemon-reload
# sudo systemctl restart nginx
# sudo systemctl restart application
# sudo systemctl start application
# sudo systemctl enable application

# Configuration
echo "[INTIALIZING NGINX]"
sudo systemctl daemon-reload
# sudo rm -r /etc/nginx/sites-available/default
# sudo rm -r /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-available/default
# sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-enabled/default

