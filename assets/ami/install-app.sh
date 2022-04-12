#!/bin/bash
source lab-sysadmin-env/bin/activate

# Update repo
cd ~/lab-sysadmin
git pull

# Install dependencies
pip3 install -r application/requirements.txt

# Create /var/www/application
sudo cp -r application /var/www/application
cd /var/www/application
sudo chown -R www-data:www-data /var/www/application/
cd ~/lab-sysadmin

# Configure Nginx

# Configuration
sudo systemctl start nginx
sudo systemctl enable nginx

# .conf file
sudo rm -r /etc/nginx/sites-available/application.conf
sudo cp assets/ami/application.conf /etc/nginx/sites-available/application.conf
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# .service file
sudo rm -r /etc/systemd/system/application.service
sudo cp assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl restart application.service
sudo systemctl daemon-reload
