import pymysql
pymysql.install_as_MySQLdb()

from .celery import app as celery_app  # noqa: E402,F401

__all__ = ('celery_app',)
