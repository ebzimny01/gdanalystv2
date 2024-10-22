"""
Production Settings for Heroku
"""

import environ
import os
from urllib.parse import urlparse

# If using in your own project, update the project namespace below
from .settings import *

# Sentry integration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    integrations=[DjangoIntegration(), RedisIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    # traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    # send_default_pii=True
)


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}

redis_url = urlparse(os.environ.get('REDIS_URL', 'redis://localhost:6959'))
print(redis_url.hostname)
print(redis_url.port)
print(redis_url.password)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'rediss://%s:%s' % (redis_url.hostname, redis_url.port), 
        'OPTIONS': { 
            'DB': 0,
            'PASSWORD': redis_url.password,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient', 
            'CONNECTION_POOL_KWARGS': {
                {"ssl_cert_reqs": "CERT_NONE"}
            },
            'MAX_ENTRIES': 5000,
        }, 
    },
}