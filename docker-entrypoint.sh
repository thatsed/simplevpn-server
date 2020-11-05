#!/bin/bash

python manage.py migrate

if [ -z $SIMPLE_VPN_SUBNET ]; then
  export SIMPLE_VPN_SUBNET=10.100.20.1/24
fi
if [ -z $SIMPLE_VPN_PORT ]; then
  export $SIMPLE_VPN_PORT=1194
fi
export SIMPLE_VPN_INTERFACE=simplevpn

# split subnets and pass them as arguments
python -c "print(' '.join('$SIMPLE_VPN_SUBNET'.split(',')))" | xargs python manage.py setup_interface $SIMPLE_VPN_INTERFACE --listen-port $SIMPLE_VPN_PORT --address

if [ -f /data/.config ]; then
  echo "Loading configuration"
  source /data/.config
else
  echo "First startup configuration"
  if [ -z $DJANGO_SECRET_KEY ]; then
    export DJANGO_SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
  fi

  # echo $SIMPLE_VPN_SUBNET | xargs python manage.py create_peer simplevpn default --allowed-ips
  # if [ -z $DJANGO_SUPERUSER_PASSWORD ]; then
  #   export DJANGO_SUPERUSER_PASSWORD=$(tr -dc 'a-zA-Z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c16)
  # fi
  # python manage.py createsuperuser --username simplevpn --email "mail@example.com" --noinput
  # echo User Created: simplevpn $DJANGO_SUPERUSER_PASSWORD
  # unset DJANGO_SUPERUSER_PASSWORD

  # if configuration is successful, save config file
  touch /data/.config
  echo "DJANGO_SECRET_KEY=\"$DJANGO_SECRET_KEY\"" >> /data/.config
  echo "SIMPLE_VPN_INTERFACE=$SIMPLE_VPN_INTERFACE" >> /data/.config
  echo "Configuration saved"
fi

iptables -A FORWARD -i $SIMPLE_VPN_INTERFACE -j ACCEPT; iptables -A FORWARD -o $SIMPLE_VPN_INTERFACE -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
exec gunicorn SimpleVPN.wsgi:application --bind 0.0.0.0:8000 --workers 3
