#!/bin/bash

# Clone repo
sudo rm -r lab-sysadmin
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git

# Run install-app.sh
bash lab-sysadmin/assets/ami/install-app.sh
