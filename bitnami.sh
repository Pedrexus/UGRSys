#!/usr/bin/env bash

#!1. sudo git clone -b v1.0 --single-branch https://github.com/Pedrexus/UGRSys.git
#!2. sudo mv UGRSys/ DeGRSys/
#!3. sudo touch DeGRSys/.env
#!4. sudo nano DeGRSys/.env -> copiar parâmetros

sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py migrate --run-syncdb
sudo python3 manage.py collectstatic
sudo /opt/bitnami/ctlscript.sh restart apache