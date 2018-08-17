# Django settings for hos

from unipath import FSPath as Path

BASE_DIR = Path(__file__).absolute().ancestor(3)

# Make this unique, and don't share it with anybody.
from .secret_key import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': 'meta',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mos',
        'PASSWORD': ''
    },
}

# Local timezone
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = (
    BASE_DIR.child("static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'members.middleware.DeactivateUserMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.SetStatFooter',  # remove this row to disable
                                      # footer stats
)

ROOT_URLCONF = 'mos.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    BASE_DIR.child('templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'core.context_processors.custom_settings_global',
)

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'web',
    'projects',
    'cal',
    'members',
    'sources',
    'announce',
    'core',
)


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/member/login/'

#---  Custom Options ----------------------------------------------------------
HOS_URL_PREFIX = '/'
HOS_NAME = 'Metalab OS'
HOS_HOME_EVENT_NUM = 5
HOS_WIKI_URL = '/wiki/'
HOS_ANNOUNCE_FROM = 'core@metalab.at'
HOS_SEPA_CREDITOR_ID = 'AT12ZZZ00000000001'

MOS_WIKI_CHANGE_URL = 'https://metalab.at/wiki/index.php?title=Spezial:Letzte_%C3%84nderungen&feed=atom'
MOS_WIKI_KEEP = 5

# ----------------- Style ---------------------
HOS_CUSTOM_STYLE = ''  # name of the custom style, blank for default
HOS_MEMBER_GALLERY = True
HOS_CALENDAR = True
HOS_OPENLAB = True
HOS_INTRODUCTION = True
HOS_PROJECTS = True
HOS_RECENT_CHANGES = True
