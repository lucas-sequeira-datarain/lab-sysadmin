#!/bin/bash -xe
sudo rm -r lab-sysadmin
git clone https://github.com/lucas-sequeira-datarain/lab-sysadmin.git
bash lab-sysadmin/assets/ami/install-app.sh
