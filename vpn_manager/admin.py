from django.contrib import admin

from vpn_manager.models import ShowConfigLink


@admin.register(ShowConfigLink)
class ShowConfigLinkAdmin(admin.ModelAdmin):
    model = ShowConfigLink
