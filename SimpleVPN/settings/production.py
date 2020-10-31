"""
Django production settings for SimpleVPN project.
"""

from .base import *
import random

DATA_DIR = os.environ.get('DJANGO_DATA_DIR', BASE_DIR)

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'DANGER-THIS-IS-ONLY-FOR-COMMANDS')

DEBUG = False

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
    }
}
