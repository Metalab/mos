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

STATIC_ROOT = PROJECT_DIR.parent.child("www", "static")
MEDIA_ROOT = PROJECT_DIR.parent.child("www", "media")

HOS_SEPA_CREDITOR_ID = 'AT29HXR00000037632'
