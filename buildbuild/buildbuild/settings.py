"""
Django settings for buildbuild project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# exception message handling
# when we are attempt to save a naive datetime, warning occurs
# During development, such warnings into ignore status
import warnings 
warnings.filterwarnings(
        'ignore', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z84x8kvgq3oxtz%p@_m_td!d_@ebx-*b&4n$ad-*he@nhusni)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Docker text form files is located in /media/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ALLOWED_HOSTS = []

# For additional fixture path
FIXTURES_DIRS = (
    os.path.join(BASE_DIR, 'fixtures')
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Python Packages
    'djcelery',
    'djangobower',
    'rest_framework',

    # Kombu transport using the Django database as a message store.
    'kombu.transport.django',

    # Custom Apps
    'api',
    'users',
    'teams',
    'projects',
    'deploys',
    'properties',
    'dockerbuild',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'buildbuild.urls'

WSGI_APPLICATION = 'buildbuild.wsgi.application'

"""
# for postgresql
if "BUILDBUILD_PASSWORD" in os.environ:
    DB_PASSWORD = os.environ['BUILDBUILD_PASSWORD']
else:
    DB_PASSWORD = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'buildbuildDB',
        'USER': 'buildbuild',
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

BOWER_INSTALLED_APPS = (
    'angular#1.2.23',
)


AUTH_USER_MODEL = 'users.User'

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/users/account/" # Not Implemented : should have chnage to /profile or /dashboard stuff


# Celery Integration

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_BEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Defalut SMTP Host Setting

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  #for submission
EMAIL_HOST_USER = "buildbuildteam@gmail.com"

CELERY_ALWAYS_EAGER = True

if "BUILDBUILD_PASSWORD" in os.environ:
    EMAIL_HOST_PASSWORD = os.environ['BUILDBUILD_PASSWORD']
else:
    EMAIL_HOST_PASSWORD = ""

DEFAULT_FROM_EMAIL = "buildbuild@gmail.com"
SERVER_EMAIL = "buildbuildteam@gmail.com"
#DEFAULT_TO_EMAIL = 'to email'

# The mailing contents for new user
SUBJECT = " Welcome to buidlbuild team! "
CONTENTS = "Hello~"


