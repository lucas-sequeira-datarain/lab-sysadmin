#!/bin/bash
source lab-sysadmin-env/bin/activate

# Clone repo
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git
cd lab-sysadmin

# Install dependencies
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

# .service file
sudo cp assets/ami/application.service /etc/systemd/system/application.service
sudo systemctl restart application.service
000000
sudo systemctl daemon-reload
000000
