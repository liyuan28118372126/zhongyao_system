"""Production settings for Zhongyao System project."""

from .base import *

# Production-specific settings
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = ['example.com', 'www.example.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Production database settings
# Update with your production database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zhongyao_system',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
