# Django settings for hos

from unipath import FSPath as Path

BASE_DIR = Path(__file__).absolute().ancestor(3)

DEBUG = False
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ASGI_APPLICATION = "mos.routing.application"

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

DATABASES = {
    'default': {
        'NAME': 'meta',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mos',
        'PASSWORD': ''
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [
            BASE_DIR.child('templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                'core.context_processors.custom_settings_global',
            ],
        },
    },
]

# Local timezone
TIME_ZONE = 'Europe/Vienna'

USE_TZ = False

# Set first day of week to monday
FIRST_DAY_OF_WEEK = 1

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
LANGUAGE_CODE = 'en-us'
USE_L10N = False
DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
MONTH_DAY_FORMAT = "d.m"

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

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'members.middleware.DeactivateUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'core.middleware.SetStatFooter',  # remove this row to disable
                                      # footer stats
)

ROOT_URLCONF = 'mos.urls'


INSTALLED_APPS = (
    'django_extensions',
    'members',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.messages',
    'easy_thumbnails',
    'import_export',
    'web',
    'projects',
    'cal',
    'sources',
    'announce',
    'core',
    'channels',
    'things',
)


LOGIN_REDIRECT_URL = '/mos'
LOGIN_URL = '/member/login/'

DATA_UPLOAD_MAX_NUMBER_FIELDS=3000

#---  Custom Options ----------------------------------------------------------
HOS_URL_PREFIX = '/'
HOS_NAME = 'Metalab OS'
HOS_HOME_EVENT_NUM = 5
HOS_WIKI_URL = '/wiki/'
HOS_WIKI_FULL_URL = 'https://metalab.at/wiki/'
MEDIAWIKI_API = HOS_WIKI_FULL_URL + "api.php"
HOS_ANNOUNCE_FROM = 'core@metalab.at'
HOS_SEPA_CREDITOR_ID = 'AT12ZZZ00000000001'
HOS_SEPA_CREDITOR_NAME = 'Verein Metalab'
HOS_SEPA_CREDITOR_IBAN = 'AT483200000012345864'
HOS_SEPA_CREDITOR_BIC = 'GIBAATWWXXX'
HOS_SEPA_SCHEMA = 'pain.008.001.02'
HOS_SEPA_CURRENCY = 'EUR' # ISO 4217
HOS_SEPA_BATCH = True

HOS_ANNOUNCE_LOG = '../announce.log'
HOS_EMAIL_LOG = '../email.log'

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

# ----------------- Jour Fixe Reminder ------------
MOS_JF_DAYS_IN_ADVANCE = 3
MOS_JF_DB_ID = 2 # id of events of type "Jour Fixe" in the database
MOS_JF_SENDER = 'jf-reminder@metalab.at'
MOS_JF_RECIPIENTS = ['intern@lists.metalab.at']

# ----------------- Thumbnail Settings ------------
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (120, 120), 'crop': False},
    },
}

# ------------- Matrix Intern Inviter -------------
MATRIX_USERNAME = "@metalab_room_inviter_bot:matrix.org"
MATRIX_PASSWORD = None # Is setup in environment variables
MATRIX_ROOM_NAME = "#metalab-intern:matrix.org"
MATRIX_ROOM_ID = None # Is setup in environment variables
