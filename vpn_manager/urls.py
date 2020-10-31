from django.urls import path
from django.views.generic import TemplateView

from vpn_manager import views

app_name = 'vpn_manager'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('peers', views.ListPeerView.as_view(), name='list_peers'),
    path('peers/add', views.CreatePeerView.as_view(), name='add_peer'),
    path('peers/<int:pk>/delete', views.DeletePeerView.as_view(), name='delete_peer'),
    path('peers/<int:pk>/edit', views.UpdatePeerView.as_view(), name='edit_peer'),
    path('peers/<int:pk>', views.PeerDetailView.as_view(), name='show_peer'),
    path('tools/qrcode', views.QRCodeGeneratorToolTemplateView.as_view(), name='tool_qrcode'),
    path('<slug:token>', views.PeerConfigurationView.as_view(), name='peer_config'),
]
