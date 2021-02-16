#!/bin/bash

if [ -z $SIMPLE_VPN_SUBNET ]; then
  export SIMPLE_VPN_SUBNET=10.100.20.1/24
fi
if [ -z $SIMPLE_VPN_PORT ]; then
  export SIMPLE_VPN_PORT=1194
fi
export SIMPLE_VPN_INTERFACE=simplevpn

if [ -f /data/.config ]; then
  echo "Loading configuration"
  source /data/.config
else
  echo "Creating configuration"
  touch /data/.config
fi

echo "Startup Configuration"
# generate secret key if none is given
if [ -z $DJANGO_SECRET_KEY ]; then
  export DJANGO_SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
  echo "export DJANGO_SECRET_KEY=\"$DJANGO_SECRET_KEY\"" >> /data/.config
fi

# get endpoint from https://checkip.amazonaws.com if none is given
if [ -z $SIMPLE_VPN_ENDPOINT ]; then
  export SIMPLE_VPN_ENDPOINT=$(python -c "import requests;print(requests.get('https://checkip.amazonaws.com/').text.strip())")
  echo "export SIMPLE_VPN_ENDPOINT=\"$SIMPLE_VPN_ENDPOINT\"" >> /data/.config
fi

# Run migrations
python manage.py migrate

# update interface configuration
# split subnets and pass them as arguments
python -c "print(' '.join('$SIMPLE_VPN_SUBNET'.split(',')))" | xargs python manage.py setup_interface $SIMPLE_VPN_INTERFACE --listen-port $SIMPLE_VPN_PORT --address

# route traffic from VPN to the internet through eth0 interface
iptables -A FORWARD -i $SIMPLE_VPN_INTERFACE -j ACCEPT
iptables -A FORWARD -o $SIMPLE_VPN_INTERFACE -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# launch service
exec gunicorn SimpleVPN.wsgi:application --bind 0.0.0.0:8000 --workers 3
