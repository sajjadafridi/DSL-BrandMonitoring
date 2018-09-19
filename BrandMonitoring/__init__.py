from __future__ import absolute_import, unicode_literals
import pymysql
from .celerytask import app as celery_app


__all__ = ['celery_app']
pymysql.install_as_MySQLdb()



# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
