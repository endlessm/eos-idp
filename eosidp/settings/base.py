"""
Django settings for eosidp project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from django.contrib.messages import constants as messages
from email.utils import parseaddr

from .util import (  # noqa: F401
    BASE_DIR,
    base_path,
    database_config,
    env_bool,
    env_str,
    env_int,
    env_list,
    load_env_file,
    Vault,
)

load_env_file()
vault = Vault()


# Basic settings
DEBUG = env_bool('DEBUG', False)
SECRET_KEY = vault.env_secret_str('SECRET_KEY', 'app', 'secret_key',
                                  'badsecret' if DEBUG else '')
ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')


# Application definition
INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'oidc_provider',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eosidp.urls'
WSGI_APPLICATION = 'eosidp.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': database_config(vault,
                               'sqlite:///{}'.format(base_path('db.sqlite3')))
}


# Authentication settings
AUTH_USER_MODEL = 'main.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# OpenID Connect settings
# https://django-oidc-provider.readthedocs.io/en/latest/sections/settings.html
OIDC_USERINFO = 'main.utils.oidc_userinfo'


# Allauth settings
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_FORM_CLASS = 'main.forms.SignupForm'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True


# Social account provider settings
SOCIALACCOUNT_PROVIDERS = {}
GOOGLE_CLIENT_ID = vault.env_secret_str('GOOGLE_CLIENT_ID', 'google',
                                        'client_id')
GOOGLE_CLIENT_SECRET = vault.env_secret_str('GOOGLE_CLIENT_SECRET', 'google',
                                            'client_secret')
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    INSTALLED_APPS.append('allauth.socialaccount.providers.google')
    SOCIALACCOUNT_PROVIDERS['google'] = {
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': ''
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Site ID, required for allauth
# https://docs.djangoproject.com/en/3.0/ref/contrib/sites/
SITE_ID = env_int('SITE_ID', 1)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = base_path('staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Email
# https://docs.djangoproject.com/en/3.0/topics/email/
ADMINS = [parseaddr(addr) for addr in env_list('ADMINS', separator=',')]
SERVER_EMAIL = env_str('SERVER_EMAIL', 'root@localhost')
DEFAULT_FROM_EMAIL = env_str('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
EMAIL_HOST = env_str('EMAIL_HOST', 'localhost')
EMAIL_PORT = env_int('EMAIL_PORT', 25)
EMAIL_HOST_USER = env_str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env_bool('EMAIL_USE_SSL', False)


# Logging
# https://docs.djangoproject.com/en/3.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'main': {
            'handlers': ['console'],
            'level': env_str('LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO'),
            'propagate': False,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': env_str('ROOT_LOG_LEVEL', 'WARNING'),
    }
}


# Load local settings
try:
    from .local import *  # noqa
except ModuleNotFoundError:
    pass
