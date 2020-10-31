#!/bin/bash

# Generate random secret key if none is provided.
# This will break old sessions.
if [ -z $DJANGO_SECRET_KEY ]; then
  export DJANGO_SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
fi

python manage.py migrate
wg-quick up simplevpn
python manage.py sync_wg_peers
exec gunicorn SimpleVPN.wsgi:application --bind 0.0.0.0:8000 --workers 3