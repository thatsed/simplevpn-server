from unittest import mock

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django_wireguard.models import WireguardPeer, WireguardInterface

from vpn_manager.forms import WireguardPeerForm


class TestPeerConfigOptions(TestCase):
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__ipr',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__wg',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    @mock.patch('django_wireguard.wireguard.WireGuard._WireGuard__connect_backend',
                mock.MagicMock(return_value=mock.MagicMock(return_value=False)))
    def setUp(self):
        self.interface = WireguardInterface.objects.create(
            name=settings.SIMPLE_VPN_INTERFACE,
            listen_port=4444,
            address='10.100.100.1/24'
        )

    def test_form_redirect_allowed_ips(self):
        """
        Test that PeerForm translates the ``redirect_traffic`` boolean value to correct AllowedIPs,
        and that it sets the DNS values.
        """
        form = WireguardPeerForm(data={
            'name': 'test',
            'killswitch': True,
            'redirect_traffic': True
        })

        # form.is_valid() call is required to init form cleaned data
        self.assertTrue(form.is_valid())
        instance: WireguardPeer = form.save(commit=False)
        self.assertIn('0.0.0.0/0', instance.allowed_ips)
        self.assertEqual(settings.SIMPLE_VPN_DNS, instance.dns)

    def test_form_killswitch_disabled_allowed_ips(self):
        """
        Test that PeerForm provides  correct AllowedIPs if ``killswitch`` is disabled.
        """
        form = WireguardPeerForm(data={
            'name': 'test',
            'killswitch': False,
            'redirect_traffic': True
        })

        # form.is_valid() call is required to init form cleaned data
        self.assertTrue(form.is_valid())
        instance: WireguardPeer = form.save(commit=False)
        self.assertIn('0.0.0.0/1', instance.allowed_ips)
        self.assertIn('128.0.0.0/1', instance.allowed_ips)
        self.assertEqual(settings.SIMPLE_VPN_DNS, instance.dns)

    def test_form_no_dns_if_no_redirect(self):
        """
        Test that PeerForm provides  correct AllowedIPs if ``killswitch`` is disabled.
        """
        form = WireguardPeerForm(data={
            'name': 'test',
            'killswitch': False,
            'redirect_traffic': False
        })

        # form.is_valid() call is required to init form cleaned data
        self.assertTrue(form.is_valid())
        instance: WireguardPeer = form.save(commit=False)
        self.assertEqual('', instance.dns)


class TestVPNModule(TestCase):
    login_username = 'admin'
    login_password = 'password'

    def setUp(self):
        user = User.objects.create(
            username=self.login_username,
            is_superuser=True,
            is_active=True
        )
        user.set_password(self.login_password)
        user.save()

        self.client = Client()
        
    def test_login_required(self):
        response = self.client.get('/vpn/')
        self.assertRedirects(response, settings.LOGIN_URL + '?next=/vpn/')

    def test_namespace_slug_index_view(self):
        self.client.login(username=self.login_username,
                          password=self.login_password)
        response = self.client.get('/vpn/')
        self.assertContains(response, 'Simple VPN')
