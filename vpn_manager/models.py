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
    peer = models.OneToOneField('django_wireguard.WireguardPeer',
                                on_delete=models.CASCADE,
                                null=False,
                                related_name='show_config_token',
                                verbose_name=_("WireGuard Peer"))

    class Meta:
        verbose_name = _("Configuration Share Link")
        verbose_name_plural = _("Configuration Share Links")

    def get_link(self, request=None):
        url = reverse_lazy('vpn_manager:peer_config', args=[self.token])
        if request:
            return request.build_absolute_uri(url)
        return str(url)

    def __str__(self):
        return self.get_link()
