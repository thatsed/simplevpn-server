import secrets

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

TOKEN_LENGTH = 32


def gen_token():
    return secrets.token_urlsafe(TOKEN_LENGTH)


class ShowConfigLink(models.Model):
    token = models.CharField(max_length=TOKEN_LENGTH,
                             default=gen_token,
                             verbose_name=_("Token"))
    peer = models.OneToOneField('simple_vpn.WireguardPeer',
                                on_delete=models.CASCADE,
                                null=False,
                                related_name='show_config_token',
                                verbose_name=_("WireGuard Peer"))

    def get_link(self):
        return reverse_lazy('vpn_manager:peer_config', args=[self.token])
