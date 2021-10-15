#!/bin/bash

# Collect static files
echo "Collect static files"
python care_api/manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python care_api/manage.py migrate --noinput || exit 1
