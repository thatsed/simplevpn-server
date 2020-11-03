from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_wireguard.models import WireguardPeer, WireguardInterface


class WireguardPeerForm(forms.ModelForm):
    redirect_traffic = forms.BooleanField(required=False,
                                          initial=True,
                                          help_text=_("Redirect peer traffic through the VPN"))
    killswitch = forms.BooleanField(required=False,
                                    initial=True,
                                    help_text=_("Block all traffic not directed to VPN"))

    class Meta:
        model = WireguardPeer
        fields = ('name', 'public_key', 'redirect_traffic', 'killswitch')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['redirect_traffic'].initial = bool(self.instance.dns)
            self.fields['killswitch'].initial = self.instance.allowed_ips == '0.0.0.0/0'

    def save(self, commit=True):
        self.instance.interface = WireguardInterface.objects.get(name=settings.SIMPLE_VPN_INTERFACE)
        if self.cleaned_data['redirect_traffic']:
            self.instance.dns = settings.SIMPLE_VPN_DNS
            self.instance.allowed_ips = '0.0.0.0/0' if self.cleaned_data['killswitch'] else '0.0.0.0/1,128.0.0.0/1'
        else:
            self.instance.dns = ''
            self.instance.allowed_ips = self.instance.interface.address
        return super().save(commit)
