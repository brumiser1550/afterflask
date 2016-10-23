'''
Production Configurations

- Use Amazon's S3 for storing static files and uploaded media
'''

from boto.s3.connection import OrdinaryCallingFormat
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
ALLOWED_HOSTS = ['.DOMAIN', 'SERVER_IP']
# END SITE CONFIGURATION

# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += (
    'storages',
)

AWS_ACCESS_KEY_ID = secret.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = secret.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = 'project'
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

#  See:http://stackoverflow.com/questions/10390244/
from storages.backends.s3boto import S3BotoStorage
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage = lambda: S3BotoStorage(location='media')
DEFAULT_FILE_STORAGE = 'theyburiedus.config.production.MediaRootS3BotoStorage'

MEDIA_URL = 'https://s3.amazonaws.com/{}/media/'.format(AWS_STORAGE_BUCKET_NAME)

# Static Assets
# ------------------------
STATIC_URL = 'https://s3.amazonaws.com/{}/static/'.format(AWS_STORAGE_BUCKET_NAME)
STATICFILES_STORAGE = 'theyburiedus.config.production.StaticRootS3BotoStorage'

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = 'XYZ <noreply@DOMAIN>'
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
DATABASES['default'] = {'ENGINE': 'django.contrib.gis.db.backends.postgis',
                        'HOST': secret.DB_HOST,
                        'NAME': 'tbudb',
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