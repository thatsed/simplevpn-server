.. _installation:

============
Installation
============

Deployment with Docker is straight-forward, but first you must check for a couple of requisites.

Prerequisites
=============

* Install Docker
* Make sure the host has WireGuard kernel modules ``wireguard-dkms`` installed and loaded.
* If you want to redirect traffic through the VPN, enable IPv4 forwarding by running ``sysctl -w net.ipv4.ip_forward=1`` then ``sysctl --system``.
* Choose a folder to be mounted for config data. In the following example, we'll be using ``/opt/simplevpn``
* Retrieve your machine's IP address or domain name to be used as ``SIMPLE_VPN_ENDPOINT``
* Open ports 8000/tcp and 1194/udp (default). You may change them in the docker command (change only the left one)

Docker deployment
=================
1. To start the server, simply run::

      docker run --rm -d \
                 --cap-add NET_ADMIN \
                 --env SIMPLE_VPN_ENDPOINT=<your-machine-ip-address-or-domain> \
                 -p 8000:8000 \
                 -p 1194:1194/udp \
                 -v /opt/simplevpn:/data \
                 --name simplevpn \
                 registry.gitlab.com/simplevpn/simplevpn-server:stable

2. Create an administration account::

      docker exec -it simplevpn python manage.py createsuperuser

   You will be asked for a username, email and password. The email is optional and can be left empty.


3. Navigate to your machine's IP address or domain on port 8000. Login with the credential created in the previous step.


.. tip:: Setup NGINX as reverse proxy with Cerbot to obtain a Let's Encrypt ssl certificate and enable https.
    `Here's an example <https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04>`_


Configuration Options
=====================

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

``SIMPLE_VPN_ENDPOINT``
-----------------------

Set this variable to your machine's IP address or domain name.
Settings this to an incorrect value will prevent you from connecting to the VPN,
but restarting the container with the correct one will fix it.

If left empty, your machine's public IP will be inferred by calling https://checkip.amazonaws.com


------

``SIMPLE_VPN_PORT``
-------------------
  Default: ``1194``

The port WireGuard will be listening on.

.. warning:: If you change this value, please change the port mapping of the ``docker run`` command accordingly.


------

``SIMPLE_VPN_SUBNET``
--------------------------------------
  Default: ``10.100.20.1/24``

Set this variable to an interface address to be assigned to the VPN.

You can specify multiple values by separating addresses with a comma.

.. warning:: If you update this value, the interface will update too, but not the peers. If you expand the subnet, keeping the addresses already assigned to peers, it will be fine.
    If you instead remove from the subnet(s) addresses already assigned, you will need to update (through the Django Admin Panel) or delete and recreate the faulty peers.

------

``SIMPLE_VPN_DNS``
------------------------------------
  Default: ``1.1.1.1,1.0.0.1``

Set this variable to the DNS server(s) you want to use when redirecting traffic through the VPN. Separate addresses with a comma.
Defaults to CloudFlare's DNS.

------

``ENABLE_DJANGO_ADMIN``
-----------------------------------
Enable Django Admin Site. Set this variable without any value (it's ignored).
