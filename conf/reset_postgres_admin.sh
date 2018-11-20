#!/usr/bin/env bash
#!in case of error: "Insert or update on table “django_admin_log” violates ..."

sudo python3 DeGRSys/manage.py migrate admin 0001
echo "DROP TABLE django_admin_log;" | sudo python3 DeGRSys/manage.py dbshell
sudo python3 DeGRSys/manage.py sqlmigrate admin 0001 | python3 manage.py dbshell
sudo python3 DeGRSys/manage.py migrate admin