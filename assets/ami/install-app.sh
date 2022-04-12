#!/bin/bash
echo "[ACTIVATE ENVIRONMENT]"
source lab-sysadmin-env/bin/activate

# Update repo
echo "[UPDATE REPOSITORY]"
cd ~/lab-sysadmin
git pull

# Install dependencies
echo "[UPDATE DEPENDENCIES]"
pip3 install -r application/requirements.txt

# Create /var/www/application
echo "[CREATE /VAR/WWW/APPLICATION]"
sudo rm -r /var/www/application
sudo cp -r ~/lab-sysadmin/application /var/www/
cd /var/www/application
sudo chown -R www-data:www-data /var/www/application/
cd ~/lab-sysadmin

# Configure Nginx
cd /var/www/application/

# .service file
echo "[CONFIGURING APP .SERVICE]"
sudo rm -r /etc/systemd/system/application.service
sudo cp ~/lab-sysadmin/assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl start application
sudo systemctl enable application

# .conf file
echo "[CONFIGURING APP .CONF]"
sudo rm -r /etc/nginx/sites-available/application.conf
sudo cp ~/lab-sysadmin/assets/ami/application.conf /etc/nginx/sites-available/application.conf
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/

# App
echo "[STARTING APP]"
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl restart application
sudo systemctl start application
sudo systemctl enable application

# Configuration
echo "[INTIALIZING NGINX]"
sudo rm -r /etc/nginx/sites-available/default
sudo systemctl start nginx
sudo systemctl enable nginx

# sudo cp /home/ubuntu/lab-sysadmin/assets/ami/nginx.default.conf /etc/nginx/sites-available/default

