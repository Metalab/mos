# Django settings for a deployed instance of MOS
from common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('MOS Admin', 'mos@metalab.at'),
)

MANAGERS = ADMINS

USE_X_FORWARDED_HOST = True
ALLOWED_HOSTS = ['metalab.at']
SESSION_COOKIE_DOMAIN = 'metalab.at'

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
        'NAME': 'mos',
        'USER': 'mos',
        'PASSWORD': '********',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_ROOT = BASE_DIR.parent.child("www", "static")
MEDIA_ROOT = BASE_DIR.parent.child("www", "media")

HOS_SEPA_CREDITOR_ID = 'AT29HXR00000037632'
