#!/bin/bash
echo "[ACTIVATE ENVIRONMENT]"
source lab-sysadmin-env/bin/activate > tmp.txt

# Update repo
echo "[UPDATE REPOSITORY]"
cd ~/lab-sysadmin
git pull > tmp.txt

# Install dependencies
echo "[UPDATE DEPENDENCIES]"
pip3 install -r application/requirements.txt > tmp.txt

# Create /var/www/application
echo "[CREATE /VAR/WWW/APPLICATION]"
sudo cp -r application /var/www/application
cd /var/www/application
sudo chown -R www-data:www-data /var/www/application/ > tmp.txt
cd ~/lab-sysadmin

# Configure Nginx

# Configuration
echo "[INTIALIZING NGINX]"
sudo systemctl start nginx > tmp.txt
sudo systemctl enable nginx > tmp.txt

# .conf file
echo "[CONFIGURING NGINX .CONF]"
sudo rm -r /etc/nginx/sites-available/application.conf
sudo cp assets/ami/application.conf /etc/nginx/sites-available/application.conf
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/ > tmp.txt
sudo systemctl restart nginx > tmp.txt

# .service file
echo "[CONFIGURING NGINX .SERVICE]"
sudo rm -r /etc/systemd/system/application.service
sudo cp assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl restart application.service > tmp.txt
sudo systemctl daemon-reload > tmp.txt
