#!/usr/bin/env bash
#!inicalmente, eh preciso criar o arquivo .env
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py migrate --run-syncdb
sudo python3 manage.py collectstatic
sudo /opt/bitnami/ctlscript.sh restart apache