================
SimpleVPN Server
================

    SimpleVPN is a self-hosted VPN solution powered by WireGuard and Django.

Deployment
==========

Deployment with Docker is straight-forward, but first you must check for a couple of requisites.

Prerequisites
~~~~~~~~~~~~~
.. important:: Don't skip those steps!

* Make sure the host has WireGuard kernel modules `wireguard-dkms` installed and loaded.
* If you want to redirect traffic through the VPN, enable IPv4 forwarding by adding the line `net.ipv4.ip_forward = 1` to `/etc/sysctl.conf`.
* Create a folder to be mounted for config data. In the following example, we'll be using `/opt/simplevpn`
* Retrieve your machine's IP address or domain name and keep that in mind

Docker deployment
~~~~~~~~~~~~~~~~~
1. To start the server, simply run

   .. code-block:: bash

      docker run --rm -d \
                 --cap-add SYS_ADMIN \
                 --cap-add NET_ADMIN \
                 --env SIMPLE_VPN_ENDPOINT=<your-machine-ip-address-or-domain> \
                 -p 8000:8000 \
                 -p 1194:1194 \
                 -v /opt/simplevpn:/data \
                 registry.gitlab.com/simplevpn/simplevpn-server


2. Create a superuser account

   .. code-block:: bash

      docker exec -it simplevpn python manage.py createsuperuser

   You will be asked for a username, email and password. The email is optional and can be left empty.


3. Navigate to your machine's IP address or domain name on port 8000. Login with the credential created in the previous step.

4. (Optional) setup NGINX reverse proxy with Cerbot to obtain a Let's Encrypt ssl certificate.
