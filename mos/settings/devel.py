# Django settings for a local development instance of MOS
from .common import *


# Make this unique, and don't share it with anybody. 
# ATTENTION - It may trigger an error or overwrite the SECRET_KEY if you develope in a docker environment with DEVEL settings
from .secret_key import *

DEBUG = True
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

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

MEDIA_ROOT = BASE_DIR.child("media")

HOS_SEPA_CREDITOR_ID = 'AT29HXR00000037632'
HOS_SEPA_CREDITOR_BIC = 'GIBAATWWXXX'