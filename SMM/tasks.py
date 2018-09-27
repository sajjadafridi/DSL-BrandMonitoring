from __future__ import absolute_import, unicode_literals

from Analysis.SentimentAnalysis import SentimentAnalysis
from celery import task
from SETMOK_API.SETMOKE_API import SETMOKE_API
from SMM.Sentiment import Sentiment

@task()
def scheduling_script():
 setmoke = SETMOKE_API("", "")
 list = setmoke.read_and_fetch('localhost', 'root', 'rehab105', 'SMM_DB', 1,
                               "/home/rehab/PycharmProjects/conf/config.ini")


 for key, value in list.items():
     sent_list = []
     for mention in value:
         sent = Sentiment()
         sent.set_list(mention)
         sent.set_sentiment(0)
         sent_list.append(sent)

     setmoke.update_database(sent_list, key, 'localhost', 'root', 'rehab105', 'SMM_DB', 1)