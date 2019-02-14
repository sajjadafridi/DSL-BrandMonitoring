"""
Django settings for BrandMonitoring project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from celery.schedules import crontab


#  for email verificaiton

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'muhammad.sajjad@kics.edu.pk'
EMAIL_HOST_PASSWORD = 'saj427272727()()()()()()()'
EMAIL_PORT = 587


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import os.path
# SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7wua1i=7zyr+ffg$qr_+m1+^!6)dnobrs4$th+g2j^%1%#)&on'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'celery',
    'SMM.apps.SmmConfig',

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

ROOT_URLCONF = 'BrandMonitoring.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend']

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
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
CORS_ORIGIN_ALLOW_ALL = True

WSGI_APPLICATION = 'BrandMonitoring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SMM_DB',
        'USER': 'root',
        # 'PASSWORD': 'fatima103',
        #'PASSWORD': 'sajjadafridi',
	'PASSWORD' : 'smm',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'autocommit': True,
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
# MEDIA_URL = '/media/'
# # MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)
# STATIC_ROOT="E:/Pycharm Project/"
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/redis-


STATIC_URL = '/static/'
LOGIN_URL = 'remember_me_login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'redirect_login'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'
CELERY_BEAT_SCHEDULE = {

    'scheduling_script': {
        'task': 'SMM.tasks.scheduling_script',
        'schedule': crontab(hour='*/24,0'),
    }
}
