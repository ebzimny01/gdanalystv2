"""
Production Settings for Heroku
"""

import environ
import os
from urllib.parse import urlparse

# If using in your own project, update the project namespace below
from gd.settings import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

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

redis_url = urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))
print(redis_url.hostname)
print(redis_url.port)
print(redis_url.password)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port), 
        'OPTIONS': { 
            'DB': 0,
            'PASSWORD': redis_url.password,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient', 
            'MAX_ENTRIES': 5000, 
        }, 
    },
}