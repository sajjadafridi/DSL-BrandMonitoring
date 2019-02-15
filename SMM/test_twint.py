from langdetect import detect_langs, DetectorFactory, detect
import operator
import re
import ast
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    # print(score['neg'])
    # print(score['neu'])
    # print(score['pos'])
    # print(score['compound'])
    # print("{:-<40} {}".format(sentence, str(score)))
    return score['compound']


with open('SMM/data.txt', encoding='utf-8') as f:
    # content = f.readlines()
    # content = [x.strip() for x in content]
    # for cont in content:

    text = re.sub(
        r'\b(?:(?:https?|ftp)://)?\w[\w-]*(?:\.[\w-]+)+\S*', '', 'pic.twitter.com/7sri7fSbUc')
    text = re.sub(r'…', '', text)
    text = re.sub(r'\.+', '.', text)
    text = re.sub(r'\?+', '?', text)
    text = text.replace(r'\'', '\'').replace(
        r'\"', '"').rstrip('\'').lstrip('\'').strip()
    languages_list = dict()
    languages = detect_langs(cont)
    if len(languages) > 0:
        for lang in languages:
            la = str(lang)
            score = la.split(":")
            languages_list[score[0]] = float(score[1])
        str1 = max(languages_list.items(),
                   key=operator.itemgetter(1))[0]
        # if (str1 != 'ar' or str1 != 'ja'):
           if not text.strip():
                print(text)
            else:
                temp = sentiment_analyzer_scores(text)
                if (temp >= 0.05):
                    print('positive sentiment')
                elif (temp > -0.05 and temp < 0.05):
                    print('neutral sentiment')
                elif (temp < -0.05):
                    print('negative sentiment')
