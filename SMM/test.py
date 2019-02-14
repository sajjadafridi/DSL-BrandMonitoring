import pip 
from collections import Counter
from setmoke.sentiment_urdu import utilities
from UrduSentimentPredication import *

data = 'آج موسم بہت خوبصورت ہے'
data = data.split('\n')
loadData()
data = predOnData(data)
print(max(data,key=data.count))