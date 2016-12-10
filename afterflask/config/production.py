'''
Production Configurations

- Use Amazon's S3 for storing static files and uploaded media
'''

from django.utils import six
from afterflask.generate_key import generate_key

from .common import *  # noqa

import afterflask.secret as secret

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = '{}'.format(generate_key(40, 128))


# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.naturalcarecleaningservice', '45.32.67.180']
# END SITE CONFIGURATION

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
)

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = 'No Reply <noreply@naturalcarecleaningservice>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'EMAIL@DOMAIN'
EMAIL_HOST_PASSWORD = secret.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[DOMAIN] '


# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = {'ENGINE': 'django.db.backends.postgresql',
                        'HOST': secret.DB_HOST,
                        'NAME': 'clean',
                        'USER': secret.DB_USER,
                        'PASSWORD': secret.DB_PASSWORD,
                        'PORT': '5432'}

ADMIN_URL = '/admin/'

# suppress admin emails from disallowed hosts
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}


# Your production stuff: Below this line define 3rd party library settings

DEBUG = False
REGISTRATION_OPEN = False
ACCOUNT_ACTIVATION_DAYS = 7