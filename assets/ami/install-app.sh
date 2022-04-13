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

# .service file
echo "[CONFIGURING APP .SERVICE]"
sudo rm -r /etc/systemd/system/application.service
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl start application
sudo systemctl enable application

# .conf file
echo "[CONFIGURING APP .CONF]"
sudo rm -r /etc/nginx/sites-available/application.conf
sudo rm -r /etc/nginx/sites-enabled/application.conf
sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-available/default
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/

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
sudo systemctl start nginx
sudo systemctl enable nginx

# sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-available/default
# sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-enabled/default

