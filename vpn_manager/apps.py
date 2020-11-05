from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VpnManagerConfig(AppConfig):
    name = 'vpn_manager'
    verbose_name = "VPN Manager Module"
    module_config = {
        "title": _("Manage VPN"),
        "slug": "vpn",
    }
