# Django settings for a deployed instance of MOS
import os
from .common import *

DEBUG = False

ADMINS = (
    # ('MOS Admin', 'mos@metalab.at'),
)

MANAGERS = ADMINS

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = [ os.environ.get('DJANGO_DOMAIN', 'localhost') ]
SESSION_COOKIE_DOMAIN = os.environ.get('DJANGO_DOMAIN', 'localhost')

# Enable this if you are running behind a reverse proxy.
# You MUST configure the proxy to strip X-Forwarded-Proto to avoid security
# issues! This is how you do it in Apache (enable mod_headers):
#
# RequestHeader unset X-Forwarded-Proto
# RequestHeader set X-Forwarded-Proto https env=HTTPS
#
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'mos'),
        'USER': os.environ.get('MYSQL_USER', 'mos'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'mos'),
        'HOST': os.environ.get('MYSQL_HOST', 'db'),
    }
}

SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY')

STATIC_ROOT = os.environ.get('DJANGO_STATIC_ROOT', 'static')
MEDIA_ROOT = os.environ.get('DJANGO_MEDIA_ROOT', 'media')

EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', 25)
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'False').lower() in ('true', 'yes', '1')
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_SUBJECT_PREFIX = os.environ.get('DJANGO_EMAIL_SUBJECT_PREFIX', '[MOS] ')

HOS_SEPA_CREDITOR_ID = os.environ.get('HOS_SEPA_CREDITOR_ID', 'AT29HXR00000037632')
