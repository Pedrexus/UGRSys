#!/usr/bin/env bash

sudo rm -r DeGRSys/
sudo git clone -b v1.0 --single-branch https://github.com/Pedrexus/UGRSys.git
sudo mv UGRSys/ DeGRSys/
sudo cp .env DeGRSys/.env

cd DeGRSys/

sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py migrate --run-syncdb

#!don't forget:
    #!opt/bitnami/apache2/conf/bitnami/bitnami-apps-prefix.conf
    #!Include "/opt/bitnami/apps/django/django_projects/PROJECT/conf/httpd-prefix.conf"
#!ALLOWED_HOSTS += ['SERVER-IP'] (settings.py)
#!POSTGRES_PASSWORD=... (.env)

#! TODO: Deploy allowing permission to edit media/ folder
sudo /opt/bitnami/ctlscript.sh restart apache