# Django settings for a local development instance of MOS
from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

LOGGING['loggers']['django']['handlers'] = ['file', 'console']
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['django.request']['handlers'] = ['file', 'console']
LOGGING['loggers']['django.request']['level'] = 'DEBUG'
