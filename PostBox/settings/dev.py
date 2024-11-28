import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]
WSGI_APPLICATION = "PostBox.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "posetboxdb",
        "USER": "root",
        "PASSWORD": "0123",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
