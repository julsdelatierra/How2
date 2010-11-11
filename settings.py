# Django settings for how2 project.
import os

WELCOME = 'Bienvenido '
WS_NAME='How2'
WS_SLOGAN='share experience'
WS_LOGO='how2.png'
WS_FOOTER_CONTENT='Open Comunity'
WS_FOOTER_LINK='http://www.opencomunity.com'
PATH = os.getcwd()+os.sep
URL = 'http://localhost:8000/'
STATIC = PATH+'media/'
AUTH_PROFILE_MODULE = 'core.Profile'
#LOGIN_REDIRECT_URL='/account/home/'
AVAILABLE_ENCODINGS = ('utf-8','ascii','latin-1')
DEFAULT_CHARSET='utf-8'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Juli&aacute;n Ceballos', 'cristianjulianceballos@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PATH+'db.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PATH + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = URL + 'media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')=k@=2-5&kpf8aovy(hp!2^f2bft-(k^s9vv198swwfivcf6#9'

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
)

ROOT_URLCONF = 'how2.urls'

TEMPLATE_DIRS = (
    PATH+'templates/'
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'how2.core',
    'how2.mod_admin',
    'how2.mod_user',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'how2.core.context_processors.index',
    'how2.core.context_processors.core',
    'how2.mod_user.context_processors.data',
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
)
