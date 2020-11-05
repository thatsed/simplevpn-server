"""
Module Configuration.

Register SimpleVPN Modules here.
The modules are shown in the order they are inserted in the ``MODULES`` list.
The first module of the list will be treated as the default. Set ``DEFAULT_MODULE`` to the module name of
another one to change it.

Module Struct: (module_name, {options})
Available options:
    title: the verbose name of the module
    slug: the url slug used as base url for the module views
    namespace: app_name of the app's urls module (defaults to module_name)
    index: path name of the module's index view (defaults to "index")
"""

from django.utils.translation import ugettext_lazy as _


MODULES = [
    ('vpn_manager', {}),
]
