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

MEDIA_ROOT = BASE_DIR.child("media")

HOS_SEPA_CREDITOR_ID = 'AT29HXR00000037632'

HOS_WIKI_URL = "https://metalab.at/wiki/"
MEDIAWIKI_API = HOS_WIKI_URL + "api.php"
