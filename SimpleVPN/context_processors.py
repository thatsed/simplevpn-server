from django.conf import settings
from django.http import HttpRequest


def modules(request: HttpRequest):
    kwargs = {
        'modules': settings.PLUGIN_MODULES,
        'current_module': next(filter(lambda module: module['module_name'] == request.resolver_match.app_name,
                                      settings.PLUGIN_MODULES), None),
    }
    return kwargs
