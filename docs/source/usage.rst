=====
Usage
=====

Quick Start
===========

Configuring Peers
~~~~~~~~~~~~~~~~~

To access your VPN, you will need to create yourself a WireGuard peer.

.. hint:: You will need a peer for each device you want to connect to the VPN

To create a peer:
   #. Access the admin panel by navigating to your newly deployed installation
   #. In the *VPN* section, create a new peer by clicking on *NEW* on the top right of the empty table
   #. Fill in the form with a name for this peer (for example, "My Smartphone")
   #. (Optional) `Providing your own Public Keys`_: for an extra layer of security, provide your own public key. Leave it empty for auto-generation.
   #. Select "Redirect traffic" to forward all traffic through the VPN (standard usage)
   #. Select "Killswitch" if you want any traffic not going through the VPN to be dropped. Uncheck this option to continue accessing your local network (eg. printers, smart devices and such) even when connected to the VPN
   #. Click on Save peer

Now that your peer is created, from the *Options* menu select *Show Configuration* to retrieve the configuration needed to connect with it.

.. warning:: Changing the "Redirect traffic" and "Killswitch" options require you to update the configuration on your device.


Connecting to the VPN
~~~~~~~~~~~~~~~~~~~~~

First, `Download WireGuard <https://www.wireguard.com/install/>`_ for your device.
Once installed, download and import your configuration or scan the QR code.

The configuration of a peer can be viewed from the peer list by selecting *Show Configuration* from the options menu.


Sharing Configurations
~~~~~~~~~~~~~~~~~~~~~~

You can create a share link for a peer by selecting *Share* from the options menu, then click on the *Create Link* button.

Copy and share the provided link.

.. danger:: It's strongly advised to delete the link once it's not needed anymore. You can do so from the same modal by clicking on the *Disable Link* button.
    Peers with active share links will have a *Shared* badge on the corresponding row.


Changing Login Password
~~~~~~~~~~~~~~~~~~~~~~~

Execute this command (while the container is running) to change a user's password::

    docker exec -it simplevpn python manage.py changepassword <username>

You can also manage users from the Django Admin Site. Be sure to enable it first by setting


Advanced Topics
===============

Providing your own Public Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of letting SimpleVPN generate and store Private Keys, you may want to provide your own Public Key.

Generate a Private Key
----------------------
With WireGuard installed, you can generate a Private Key by executing::

    wg genkey

This is the one that you need in your peer configuration. We'll refer to it as ``<YOUR-PRIVATE-KEY>``.

Calculate the Public Key
------------------------
The one needed in the form is the Public Key, and you gave to calculate it. This can be done with WireGuard too::

    echo <YOUR-PRIVATE-KEY> | wg pubkey

Copy the output and paste it in the form.

Complete peer configuration
---------------------------
You will notice that the configuration download page for a peer created this way is incomplete.

A warning is displayed, and the QR Code will not work.

Download the configuration, and replace the ``<INSERT-PRIVATE-KEY-FOR:{public-key}>`` with the corresponding private key.

.. hint:: You can copy this configuration in the *QRCode Tool* to substitute it manually and generate a valid QR Code.


Clearing Private Keys Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Execute the following command (while the container is running) to remove all Private Keys from database::

    docker exec -it simplevpn python manage.py clear_private_keys

.. warning:: After purging Private Keys, all peer configurations will show the "Missing private key" warning, and their configurations will have to be completed manually (`Complete peer configuration`_)
