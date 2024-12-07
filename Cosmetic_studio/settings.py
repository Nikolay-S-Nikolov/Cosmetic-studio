"""
Django settings for Cosmetic_studio project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import logging.config

from django.urls import reverse_lazy

# Quick-start development settings - unsuitable for production, see https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
# import logging

# Set up logging
# logging.basicConfig(level=logging.DEBUG)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# Log the path and existence of .env file
# logging.debug(f".env file path: {env_path}")
# logging.debug(f".env file exists: {env_path.exists()}")

# Log the value of SECRET_KEY
# logging.debug(f"SECRET_KEY: {SECRET_KEY}")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = True
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", None) == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", None).split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'widget_tweaks',

    # my apps
    "Cosmetic_studio.common.apps.CommonConfig",
    "Cosmetic_studio.accounts.apps.AccountsConfig",
    "Cosmetic_studio.services.apps.ServicesConfig",
    "Cosmetic_studio.blog.apps.BlogConfig",
    "Cosmetic_studio.contact.apps.ContactConfig",
    "Cosmetic_studio.product.apps.ProductConfig",
    "Cosmetic_studio.orders.apps.OrdersConfig"
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

ROOT_URLCONF = 'Cosmetic_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Cosmetic_studio.wsgi.application'

# ASGI_APPLICATION = 'Cosmetic_studio.asgi.application'

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(",")
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", None),
            "USER": os.environ.get("DB_USER", None),
            "PASSWORD": os.environ.get("DB_PASSWORD", None),
            "HOST": os.environ.get("DB_HOST", None),
            "PORT": os.environ.get("DB_PORT", 5432),
        }
    }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("DB_NAME", None),
#         "USER": os.environ.get("DB_USER", None),
#         "PASSWORD": os.environ.get("DB_PASSWORD", None),
#         "HOST": os.environ.get("DB_HOST", None),
#         "PORT": os.environ.get("DB_PORT", 5432),
#     }
# }
#

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# if DEBUG:
#     AUTH_PASSWORD_VALIDATORS = ()

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR / "staticfiles",
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = BASE_DIR / "static_files/"

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media/"
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.StudioUser"

LOGIN_REDIRECT_URL = reverse_lazy("index")
LOGOUT_REDIRECT_URL = reverse_lazy("index")
# LOGIN_URL = reverse_lazy("login_user")

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", None)
EMAIL_HOST = os.environ.get("EMAIL_HOST", None)
EMAIL_PORT = os.environ.get("EMAIL_PORT", None)
EMAIL_USE_TLS = os.environ.get("EMAIL_PORT", None) == 'True'
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", None)
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", None)
MY_EMAIL = os.environ.get("MY_EMAIL", None)

# SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", None) == 'True'
# if SECURE_SSL_REDIRECT:
#     SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
#     CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'debug.log'),
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG' if DEBUG else 'INFO',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#     },
# }
