from .base import *

# Development settings
DEBUG = True
ALLOWED_HOSTS = ['*']

# Database settings for development (could be SQLite, or another DB like PostgreSQL)
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db_dev.sqlite3',
}
