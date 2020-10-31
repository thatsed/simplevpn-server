"""
Django development settings for SimpleVPN project.
"""

from .base import *


SECRET_KEY = '&e1tf5lh6(le8s2l2r_rlmp24n@hki=+^8+6+^=_521&n2n66q'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}