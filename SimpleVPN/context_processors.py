from django.conf import settings
from django.http import HttpRequest


def modules(request: HttpRequest):
    return {
        'modules': settings.PLUGIN_MODULES,
        'current_module': next(filter(lambda module: module['module_name'] == request.resolver_match.app_name,
                                      settings.PLUGIN_MODULES), None),
        'header_links': [{
            'title': link[0],
            'url': link[1],
        } for link in settings.HEADER_LINKS],
        'app_title': settings.APP_TITLE,
    }
