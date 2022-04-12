#!/bin/bash

# Clone repo
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git
cd lab-sysadmin

# Install dependencies
source lab-sysadmin-env/bin/activate
pip3 install -r application/requirements.txt

# Create /var/www/application
sudo cp -r application /var/www/application
cd /var/www/application
sudo chown -R www-data:www-data /var/www/application/
cd ~/lab-sysadmin

# Configure Nginx

# .conf file
sudo cp assets/ami/application.conf /etc/nginx/sites-available/application.conf
sudo ln -s /etc/nginx/sites-available/application.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
000000

# .service file
sudo cp assets/ami/lab-sysadmin-appserver.service /etc/systemd/system/application.service
sudo systemctl restart application.service
000000
sudo systemctl daemon-reload
000000
