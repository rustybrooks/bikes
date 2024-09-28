import os, sys
sys.path.append("/home/ubuntu/programs/django/photos")
sys.path.append("/Users/rbrooks/programs/django/photos")

os.environ['PYTHONWARNINGS']="ignore:Unverified HTTPS request"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Rusty Brooks', 'me@rustybrooks.com'),
)

MANAGERS = ADMINS

DATABASES = {}
if os.getenv('DJANGO_LOCAL', "0") == "1":
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './bikething.db',                      # Or path to database file if using sqlite3.
        'USER': 'bikedb',                      # Not used with sqlite3.
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bike',                      # Or path to database file if using sqlite3.
        'USER': 'rbrooks',
#        'PASSWORD': 'As3sang!',
        'PASSWORD': 'ntypitp',
        'HOST': 'localhost',
#        'HOST': 'bike.cwrbtizazqua.us-west-2.rds.amazonaws.com',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '5555',                      # Set to empty string for default.        
    }

print DATABASES

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.rustybrooks.com', 'bike-home.rustybrooks.com', '192.168.1.5']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/bikething/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%@!sf+v-7vm+lr_u(i57b$klgrl0$-g5c8o)jkr4dp)xiivf!d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangomako.middleware.MakoMiddleware',
)

ROOT_URLCONF = 'bikething.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bikething.wsgi.application'

TEMPLATE_DIRS = (
 '/templates',
)
TEMPLATE_DIRS = [BASE_PATH + path for path in TEMPLATE_DIRS]

MAKO_MODULE_DIR = BASE_PATH + '/tmp/templates'
MAKO_TEMPLATE_DIRS = ('/templates', '/../../django/photos/templates/')
MAKO_TEMPLATE_DIRS = [BASE_PATH + path for path in MAKO_TEMPLATE_DIRS]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'bikecal',
    'bikething',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING_FILENAME = '/tmp/django.log'
if not os.path.exists(LOGGING_FILENAME):
    basedir = os.path.dirname(LOGGING_FILENAME)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    open(LOGGING_FILENAME, 'a').close()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        "default": {
            'class': 'logging.FileHandler',
            'filename': LOGGING_FILENAME,
            'formatter': 'standard',
            "level": "DEBUG",
        },
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handers': ['console', 'default'],
        },
        'django': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console', 'default'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
   "formatters": {
        "standard": {"format": "[pid: %(process)d] %(asctime)-15s %(levelname)s: %(name)s: %(message)s"}
    },
   "root": {"level": "INFO", "handlers": ["default"]}
}



TEST_RUNNER = 'django.test.runner.DiscoverRunner'

