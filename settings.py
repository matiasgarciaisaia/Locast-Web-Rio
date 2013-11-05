# Django settings for the locast travels project.

# All variables indicated as "settings_local" should be overriden
# within a deployment specific settings_local.py file

# settings_local
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Whether or not this is a production machine
# (Used for google analytics type things)
PRODUCTION = False

# settings_local
ADMINS = None
MANAGERS = None

# Set this in settings_local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Placeholder for a caching backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.

# This should always be UTC. All timezone conversion should happen on the client side.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

# settings_local
LANGUAGE_CODE = None
LANGUAGES = None

# settings_local
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# The host address of this installation, i.e. http://locast.mit.edu
# settings_local
HOST = ''

# The absolute URL of the application, i.e. /civicmedia
# settings_local
BASE_URL = None

# Generally, FULL_BASE_URL = HOST + BASE_URL
# settings_local
FULL_BASE_URL = ''

# settings_local
LOGIN_REDIRECT_URL = ''
LOGIN_URL = ''

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# settings_local
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

# settings_local
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

# settings_local
ADMIN_MEDIA_PREFIX = ''

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'locast.auth.backends.LocastEmailBackend',
    'locast.auth.backends.LocastUsernameBackend',
    'social.backends.twitter.TwitterOAuth',    
    'social.backends.facebook.FacebookOAuth2',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'locast.context_processors.settings_variables',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'travels.settings_context_processor.project_settings',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'locast.middleware.LocastMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'

import os
BASE_PATH = os.path.split(__file__)[0]

TEMPLATE_DIRS = (
    # These are loaded by the template app loader
)

LOCALE_PATHS = (
    '%s/locale' % BASE_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'locast',
    'south',
    'sorl.thumbnail',
    'modeltranslation',
    'social.apps.django_app.default',
    'travels',
    #'debug_toolbar',
)

MODELTRANSLATION_TRANSLATION_REGISTRY = 'travels.translation'

### LOCAST SETTINGS ###

LOCAST_CORE_VERSION = 'dev'

APP_LABEL = 'travels'

USER_MODEL = 'travels.TravelsUser'

USER_ACTIONS = (
    'joined',
    'created',
    'commented',
)

SOCIAL_AUTH_USER_MODEL = USER_MODEL

SOCIAL_AUTH_LOGIN_URL = '/my_account/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/my_account/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/my_account/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/my_account/'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['publish_actions', 'email']
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [('username', 'username'), ('name', 'name')]

SOCIAL_AUTH_TWITTER_EXTRA_DATA = [('screen_name', 'screen_name')]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
)

# OAuth keys, fill them on settings_local
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

DEFAULT_PRIVACY = 2

# settings_local
DEFAULT_LON = 0.0
DEFAULT_LAT = 0.0
DEFAULT_ZOOM = 0

GOOGLE_MAPS_KEY = ''

# Allows arbitrary settings variables to be exposed to templates
CONTEXT_VARIABLES = (
    'GOOGLE_MAPS_KEY',
    'GOOGLE_ANALYTICS_ID',
    'FLOWPLAYER_SWF',
    'DEFAULT_LON',
    'DEFAULT_LAT',
    'DEFAULT_ZOOM',
    'PRODUCTION',
)

# import settings_local
try: from settings_local import *
except ImportError: raise 'Cannot find settings_local.py!'

