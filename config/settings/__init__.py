from decouple import config

from .celery import app as celery_app

__all__ = ('celery_app',)

DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    from .development import *
else:
    from .production import *
