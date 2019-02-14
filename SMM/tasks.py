import asyncio
import time
from datetime import datetime, timedelta

from celery.contrib import rdb
from celery.task import task

from SMM import twint
from SMM.models import *
from SMM.TwintThread import TwintThread
from threading import Thread

@task
def scheduling_script():
    Keyword_table = Keyword.objects.all()
    for kwd in Keyword_table:
        startThreadTwitterUpdatedFeeds(kwd.id, kwd.alert_name)

def startThreadTwitterUpdatedFeeds(kwd_id, keyword):
    t = Thread(target=get_update_feeds, args=(kwd_id, keyword))
    t.start()
    t.join()

def get_update_feeds(kwd_id, keyword):
    asyncio.set_event_loop(asyncio.new_event_loop())
    get_daily_tweets(kwd_id, keyword)

def get_daily_tweets(keyword_id, keyword):
    print("Keyword: " + keyword)
    c = None
    c = twint.Config()
    c.Search = keyword
    c.Since = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    c.Until = datetime.strftime(datetime.now(), '%Y-%m-%d')
    c.KwdID = keyword_id
    c.Database = "db_tweets"
    twint.run.Search(c)
