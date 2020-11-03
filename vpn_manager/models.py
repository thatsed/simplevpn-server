import secrets

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django_wireguard.models import WireguardPeer

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

    def get_link(self):
        return f"http://{settings.WIREGUARD_ENDPOINT}{reverse_lazy('vpn_manager:peer_config', args=[self.token])}"

    def __str__(self):
        return self.get_link()


@receiver(post_save, sender=WireguardPeer)
def generate_share_config_link(sender, **kwargs):
    peer = kwargs['instance']
    ShowConfigLink.objects.get_or_create(peer=peer)

