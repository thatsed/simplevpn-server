"""
Django base settings for SimpleVPN project.
"""

import os

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy

from SimpleVPN import modules

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Application definition
# Plug-In Modules setup

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_wireguard',
    'crispy_forms',
    'bootstrap_pagination',
] + list(map(lambda module: module[0], modules.MODULES))

PLUGIN_MODULES = []

for module_name, module_conf in modules.MODULES:
    conf = {
        'title': module_name.replace('_', ' ').capitalize(),
        'slug': module_name,
        'namespace': module_name,
        'module_name': module_name,
    }
    conf.update(module_conf)

    conf['index'] = reverse_lazy(f"{conf['namespace']}:{conf.get('index', 'index')}")
    PLUGIN_MODULES.append(conf)

if not PLUGIN_MODULES:
    raise ImproperlyConfigured("No module loaded.")

DEFAULT_MODULE = str(getattr(modules, 'DEFAULT_MODULE', PLUGIN_MODULES[0]['module_name']))
if DEFAULT_MODULE not in map(lambda module: module['module_name'], PLUGIN_MODULES):
    raise ImproperlyConfigured("DEFAULT_MODULE is not in MODULES")

DEFAULT_MODULE_REDIRECT = next(filter(lambda module: module['module_name'] == DEFAULT_MODULE, PLUGIN_MODULES))['index']


# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SimpleVPN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'SimpleVPN.context_processors.modules',
            ],
        },
    },
]

WSGI_APPLICATION = 'SimpleVPN.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')


CRISPY_TEMPLATE_PACK = 'bootstrap4'


# SimpleVPN config

WIREGUARD_ENDPOINT = os.environ.get('SIMPLE_VPN_ENDPOINT', 'localhost')

SIMPLE_VPN_DNS = os.environ.get('SIMPLE_VPN_DNS', '1.1.1.1,1.0.0.1')

SIMPLE_VPN_INTERFACE = os.environ.get('SIMPLE_VPN_INTERFACE', 'simplevpn')

SIMPLE_VPN_DISABLE_SHARE_LINK = os.environ.get('SIMPLE_VPN_DISABLE_SHARE_LINK') == 'true'
