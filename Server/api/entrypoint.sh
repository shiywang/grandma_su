#!/bin/sh
export ZEROMQ_SERVER=0.0.0.0
# export ZEROMQ_PORT=5888
# python care_api/manage.py makemigrations --noinput
# export ZEROMQ_PORT=5889
# python care_api/manage.py migrate
# export ZEROMQ_PORT=5887
# DJANGO_SUPERUSER_PASSWORD=uched4123 python care_api/manage.py createsuperuser --username admin --email test@gamil.com --noinput
export ZEROMQ_PORT=5456
python care_api/manage.py runserver 0.0.0.0:8000
