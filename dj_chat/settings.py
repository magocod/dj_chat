"""
Django settings for djrepo project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import asyncio
import json
# standard library
import os
import sys

import django_heroku

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy(),
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = None

with open(os.path.join(BASE_DIR, 'config.json')) as json_file:
    ENV = json.load(json_file)


# SECURITY WARNING keep the secret key used in production secret
SECRET_KEY = ENV['APP']['SECRET_KEY']

# SECURITY WARNING don't run with debug turned on in production
DEBUG = ENV['APP']['DEBUG']

ALLOWED_HOSTS = ENV['APP']['ALLOWED_HOSTS']

"""
APPLICATION DEFINITION
"""

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    # local Django
    'chat',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dj_chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_chat.wsgi.application'
ASGI_APPLICATION = 'dj_chat.routing.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation' +
        '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation' +
        '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation' +
        '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation' +
        '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

"""
API REST CONFIG
"""

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = ENV['APP']['CORS_ORIGIN_WHITELIST']

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Origin'
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination' +
    '.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

"""
DATABASE CONFIG
https://docs.djangoproject.com/en/2.2/ref/settings/#databases
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    },
}

"""
MEDIA && STATIC FILES
https://docs.djangoproject.com/en/2.2/howto/static-files/
"""

# Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# # STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# # Media files (JPG, PNG, PDF, ...)
# # ...

# # ruta
# MEDIA_URL = '/media/'
# # ruta base directorio de archivos
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

"""
HEROKU APP
"""

# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
# STATIC_URL = '/static/'

# # # Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, 'static'),
# ]

IS_CI = os.environ.get('IS_CI', False)
if not IS_CI:
    django_heroku.settings(locals())
