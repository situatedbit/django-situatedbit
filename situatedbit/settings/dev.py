from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$0))g4a&c_miv)v9oxtqn4#g!6u6!6v69a!5zcuj)i15s$@%ai'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'situatedbit_dev',
        'USER': 'situatedbit',
        'PASSWORD': 'garbage',
    }
}

try:
    from .local import *
except ImportError:
    pass
