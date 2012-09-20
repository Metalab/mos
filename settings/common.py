# Django settings for hos

from unipath import FSPath as Path
 
PROJECT_DIR = Path(__file__).absolute().ancestor(2)

# Make this unique, and don't share it with anybody.
try:
    from secret_key import *
except ImportError:
    from django_extensions.management.commands import generate_secret_key
    cmd = generate_secret_key.Command()
    SECRET_KEY = cmd.handle_noargs()

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql' # 'postgresql_psycopg2', 'postgresql', 'mysql',
                          # 'sqlite3' or 'oracle'.
DATABASE_NAME = 'meta'
DATABASE_USER = 'mos'
DATABASE_PASSWORD = ''
DATABASE_HOST = ''       #Set to empty string for localhost.
DATABASE_PORT = ''       # Set to empty string for default.

# Local timezone
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR.child("metalab", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader', 
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'mos.core.middleware.SetStatFooter', # remove this row to disable
                                         #footer stats
)

ROOT_URLCONF = 'mos.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_DIR.child("metalab", "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'mos.core.context_processors.custom_settings_global',
)

INSTALLED_APPS = (
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'mos.web',
    'mos.projects',
    'mos.cal',
    'mos.members',
    'mos.rss',
    'mos.announce',
    'mos.core',
    'mos.scrooge',
)


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

#---  Custom Options ----------------------------------------------------------


HOS_URL_PREFIX = '/'
HOS_NAME = 'Metalab OS'
HOS_HOME_EVENT_NUM = 5
HOS_WIKI_URL = '/wiki/'
HOS_ANNOUNCE_FROM = 'core@metalab.at'
HOS_WIKI_CHANGE_URL = ''

# ----------------- Style ---------------------
HOS_CUSTOM_STYLE = '' # name of the custom style, blank for default
HOS_METASENSE = True
HOS_LOCATION_GALLERY = True
HOS_MEMBER_GALLERY = True
HOS_CALENDAR = True
HOS_OPENLAB = True
HOS_INTRODUCTION = True
HOS_PROJECTS = True
HOS_RECENT_CHANGES = True

HOS_WIKI_CHANGE_URL = 'https://metalab.at/wiki/index.php?title=Spezial:Letzte_%C3%84nderungen&feed=atom'
