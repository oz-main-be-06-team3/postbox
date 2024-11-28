from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']
WSGI_APPLICATION = 'PostBox.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'posetboxdb' / 'db.sqlite3',
        'USER': 'root',
        'PASSWORD': '0123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}