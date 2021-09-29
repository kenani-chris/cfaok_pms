"""
Django settings for cfaok_pms project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import pymysql
import os
from account.conf import AccountAppConf


pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*$r)=p%%jlt=*umvkq^+p1us1o5(_@ue=_&cpr74iil-b100k='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.40.13.25', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cfao_kenya.apps.CfaoKenyaConfig',
    'colorfield'
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

MIDDLEWARE_CLASSES = {
    "account.middleware.ExpiredPasswordMiddleware",
}

ROOT_URLCONF = 'cfaok_pms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'cfaok_pms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cfaok_pms_v3',
        'USER': 'cfaok_pms',
        'PASSWORD': 'ChangemeHR*12',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cfaok_pms',
        'USER': 'cfaok_pms',
        'PASSWORD': 'XJ;&z[|Fgt!(1~S|t*QlZ9u9kWVsPt2N',
        'HOST': 'ls-fcd4a90cb760069e747f52d43c81980f8213bf57.cull5gpq2pfe.ap-south-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}
'''


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

LOGIN_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.c-k.co.ke'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'pms_notifier@c-k.co.ke'
EMAIL_HOST_PASSWORD = 'Kenani1997.'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

ACCOUNT_PASSWORD_EXPIRY = 5
ACCOUNT_PASSWORD_USE_HISTORY = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = (
    ('Kenani Chris', 'kenanichris@outlook.com'), ('Peris Oloo', 'poloo@cfao.com'), ('Kenani Chris', 'ckenani@cfao.com'),
    ('Rebecca Odede', 'reodede@cfao.com')
)

MANAGERS = ADMINS
