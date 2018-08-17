# Django settings for a local development instance of MOS
from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mos.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',)
    
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

MEDIA_ROOT = BASE_DIR.child("media")

HOS_SEPA_CREDITOR_ID = 'AT29HXR00000037632'
