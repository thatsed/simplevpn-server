"""
Initialize Modules Configuration
"""
import logging
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

from SimpleVPN import modules

__all__ = ('PLUGIN_MODULES', 'DEFAULT_MODULE', 'DEFAULT_MODULE_REDIRECT', 'MODULE_APPS')

logger = logging.getLogger(__name__)

PLUGIN_MODULES = []

for module_name, module_conf in modules.MODULES:
    conf = {
        'title': module_name.replace('_', ' ').capitalize(),
        'slug': module_name,
        'namespace': module_name,
        'module_name': module_name,
    }
    conf.update(module_conf)

    # HUGE confusing try block, we don't care if any of this fails. It is by design.
    try:
        # import the module
        module = import_module(module_name)
        # get the module's default_app_config defined in __init__.py
        app_config_path = getattr(module, 'default_app_config')
        # get the AppConfig class and apps module
        *app_module, app_config = app_config_path.split('.')
        # import the apps module
        app_module = import_module('.'.join(app_module))
        # get the AppConfig class
        app_config = getattr(app_module, app_config)
        # get the `module_config` attribute and update the config with it
        conf.update(getattr(app_config, 'module_config', {}))
    except (ModuleNotFoundError, ValueError, AttributeError) as e:
        logger.debug(f"Could not import AppConfig.module_config from module '{module_name}': {e}")

    conf['index'] = reverse_lazy(f"{conf['namespace']}:{conf.get('index', 'index')}")

    PLUGIN_MODULES.append(conf)

if not PLUGIN_MODULES:
    raise ImproperlyConfigured("No module loaded.")

DEFAULT_MODULE = str(getattr(modules, 'DEFAULT_MODULE', PLUGIN_MODULES[0]['module_name']))

if DEFAULT_MODULE not in map(lambda module: module['module_name'], PLUGIN_MODULES):
    raise ImproperlyConfigured("DEFAULT_MODULE is not in MODULES")

DEFAULT_MODULE_REDIRECT = next(filter(lambda module: module['module_name'] == DEFAULT_MODULE, PLUGIN_MODULES))['index']

MODULE_APPS = list(map(lambda x: x[0], modules.MODULES))
