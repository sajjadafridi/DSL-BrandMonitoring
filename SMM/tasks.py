from __future__ import absolute_import, unicode_literals
from celery import task
from SETMOK_API.SETMOKE_API import SETMOKE_API

@task()
def scheduling_script():
 setmoke=SETMOKE_API("","")
 setmoke.read_and_update_database('localhost','root','rehab105','SMM_DB3')
