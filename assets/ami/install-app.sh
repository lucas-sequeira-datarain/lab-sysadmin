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
sudo cp -r application /var/www/application
cd /var/www/application
sudo chown -R www-data:www-data /var/www/application/
cd ~/lab-sysadmin

# Configure Nginx

# Configuration
echo "[INTIALIZING NGINX]"
sudo systemctl start nginx
sudo systemctl enable nginx

# .conf file
echo "[CONFIGURING NGINX .CONF]"
sudo rm -r /etc/nginx/sites-available/application.conf
sudo cp assets/ami/application.conf /etc/nginx/sites-available/application.conf
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# .service file
echo "[CONFIGURING NGINX .SERVICE]"
sudo rm -r /etc/systemd/system/application.service
sudo cp assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl restart application.service
sudo systemctl daemon-reload
