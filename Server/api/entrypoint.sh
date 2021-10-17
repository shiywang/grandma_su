#!/bin/sh
export SKIP_ZEROMQ=True
python care_api/manage.py makemigrations --noinput
python care_api/manage.py migrate
DJANGO_SUPERUSER_PASSWORD=uched4123 python care_api/manage.py createsuperuser --username admin --email test@gamil.com --noinput
unset SKIP_ZEROMQ
python care_api/manage.py runserver 0.0.0.0:8000
