from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from simple_vpn.forms import WireguardPeerForm
from simple_vpn.models import WireguardPeer
from vpn_manager.models import ShowConfigLink


class IndexView(PermissionRequiredMixin, TemplateView):
    permission_required = 'simple_vpn.view_wireguardpeer'
    template_name = 'vpn_manager/index.html'


class ListPeerView(PermissionRequiredMixin, ListView):
    permission_required = 'simple_vpn.view_wireguardpeer'
    model = WireguardPeer
    template_name = 'vpn_manager/wireguardpeer_list.html'
    context_object_name = 'peers'
    ordering = 'name'
    paginate_by = 5


class CreatePeerView(PermissionRequiredMixin, CreateView):
    permission_required = 'simple_vpn.add_wireguardpeer'
    model = WireguardPeer
    template_name = 'vpn_manager/wireguardpeer_create.html'
    form_class = WireguardPeerForm
    success_url = reverse_lazy('vpn_manager:list_peers')


class UpdatePeerView(PermissionRequiredMixin, UpdateView):
    permission_required = 'simple_vpn.change_wireguardpeer'
    model = WireguardPeer
    template_name = 'vpn_manager/wireguardpeer_update.html'
    form_class = WireguardPeerForm
    success_url = reverse_lazy('vpn_manager:list_peers')


class DeletePeerView(PermissionRequiredMixin, DeleteView):
    permission_required = 'simple_vpn.delete_wireguardpeer'
    model = WireguardPeer
    template_name = 'vpn_manager/wireguardpeer_confirm_delete.html'
    context_object_name = 'peer'
    success_url = reverse_lazy('vpn_manager:list_peers')


class PeerDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'simple_vpn.show_wireguardpeer'
    model = WireguardPeer
    template_name = 'vpn_manager/wireguardpeer_detail.html'
    context_object_name = 'peer'


class QRCodeGeneratorToolTemplateView(TemplateView):
    template_name = 'vpn_manager/generate_qrcode_tool.html'


class PeerConfigurationView(DetailView):
    model = ShowConfigLink
    template_name = 'vpn_manager/wireguardpeer_detail.html'
    slug_field = 'token'
    slug_url_kwarg = 'token'

    def get_context_data(self, **kwargs):
        context = super(PeerConfigurationView, self).get_context_data(**kwargs)
        context.update({
            'peer': self.object.peer,
        })
        return context
