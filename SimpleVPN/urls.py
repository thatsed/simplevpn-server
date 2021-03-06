"""SimpleVPN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url=settings.DEFAULT_MODULE_REDIRECT)),
]

if settings.ENABLE_DJANGO_ADMIN:
    urlpatterns.append(path('admin/', admin.site.urls))

for module in settings.PLUGIN_MODULES:
    urlpatterns.append(path(module['slug'] + '/',
                            include(f"{module['module_name']}.urls",
                                    namespace=module['namespace'])))
