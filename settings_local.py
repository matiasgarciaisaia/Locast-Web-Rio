###################################################
# Local settings file                             #
# Place any overrides to settings.py in here      #
###################################################

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Whether or not this is a production machine
# (Used for Google analytics type things)
PRODUCTION = False

#ADMINS = ()
#MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'unicef3',                      # Or path to database file if using sqlite3.
        'USER': 'locast',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# configure the available languages

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
     ('en', 'English'),
     ('fr', 'Francais')
 )

#SITE_ID = 1

# The host address of this installation, i.e. http://locast.mit.edu
# settings_local
HOST = ''

# The absolute URL of the application, i.e. /civicmedia
# settings_local
BASE_URL = ''

# Generally, FULL_BASE_URL = HOST + BASE_URL
# settings_local
FULL_BASE_URL = ''

# settings_local
LOGIN_REDIRECT_URL = ''
LOGIN_URL = ''

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# settings_local
MEDIA_ROOT = '/Users/mverzilli/Documents/trabajo/repos/Locast-Web-Unicef/static/'
STATIC_ROOT= '/Users/mverzilli/Documents/trabajo/repos/Locast-Web-Unicef/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

# settings_local
MEDIA_URL = '/static/'
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

# settings_local
ADMIN_MEDIA_PREFIX = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

############ 
# Locast-specific settings

DEFAULT_LON = -58.469238
DEFAULT_LAT = -34.633208
DEFAULT_ZOOM = 0

GOOGLE_MAPS_API_KEY = ''

FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''

PLACEHOLDER_PATH = MEDIA_ROOT + "castPlaceholder.png"

POSTGIS_TEMPLATE = 'template_postgis2'
