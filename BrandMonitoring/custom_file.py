from django.db import connection
import os
import sys
from settings import SITE_ROOT

sys.path.append(SITE_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def init():
    cursor = connection.cursor()
    tables = connection.introspection.table_names()

    for table in tables:
        if(table == 'Post'):
            sql = "ALTER TABLE Post MODIFY COLUMN Content VARCHAR(4000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;"
            print(cursor.execute(sql))
            print("Table %s set to utf8" % table)

    print("DONE!")


init()
