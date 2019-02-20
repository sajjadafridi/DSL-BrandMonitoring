import threading

from SMM import twint
from SMM.Posts import Posts
from SMM.Users import Users
from SMM.models import *
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect_langs, DetectorFactory, detect
import operator
import re
from SMM.UrduSentimentPredication import *

import asyncio

class TwintThread(threading.Thread):

    def startThreadTwitterUpdatedFeeds(self, kwd_id, keyword):
        from threading import Thread
        t = Thread(target=self.get_update_feeds, args=(kwd_id, keyword))
        t.start()
        t.join()

    def get_feeds(self, keyword, kwd_id):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.get_twitter_feed(keyword, kwd_id)

    def startThreadTwitterFeeds(self, keyword, kwd_id):
        from threading import Thread
        t = Thread(target=self.get_feeds, args=(keyword, kwd_id))
        t.start()
        # import multiprocessing
        # p = multiprocessing.Process(target=self.get_feeds, args=(keyword, kwd_id))
        # p.start()
        # t.join()

    def get_update_feeds(self, kwd_id, keyword):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.get_daily_tweets(kwd_id, keyword)

    def get_daily_tweets(self, keyword_id, keyword):
        # print("Keyword: " + keyword)

        # configure config object to get tweets
        c = twint.Config()
        c.Search = Keyword
        c.KwdID = keyword_id
        c.Database = "dbTweets"
        c.Lang="ur"
        c.Since = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        c.Until = datetime.strftime(datetime.now(), '%Y-%m-%d')
        c.Store_object = True

        # search keyword with above configuration and the tweets will be stored sequentially after being scrapped
        twint.run.Search(c)

    def get_twitter_feed(self, keyword, kwd_id):
        keyword_result = []
        c = None
        c = twint.Config()
        c.Search = keyword
        c.KwdID = kwd_id
        c.Since = datetime.strftime(datetime.now() - timedelta(30), '%Y-%m-%d')
        print(c.Since)
        c.Until = datetime.strftime(datetime.now(), '%Y-%m-%d')
        print(c.Until)
        c.Database = "db_tweets"
        c.Store_object = True
        twint.run.Search(c)

    @staticmethod
    def checkExistenceOfAPostForAUserKeyword(kwd_id, status_id):
        posts = Post.objects.filter(Keyword_id=int(kwd_id), StatusID=status_id)
        if(posts.count() == 0):
            return True
        return False

    def add_to_database(self, list, kwd_id):

        ''' check setmoke api '''
        # install_setmoke()
        ''' load urdu_sentiment data '''
        loadData()
        ''' load english sentiment class'''
        analyser = SentimentIntensityAnalyzer()
        sentiment = 0
        result = ''
        for message in list:
            if self.language_detection(message.get_text())==('en' or 'ur'):
                result = self.detect_sentiment(message.get_text(), analyser)
                ''' result for neutral will be 0 and for negative, positive will be -1, 1 '''
                if result == 'Negative':
                    sentiment = -1
                elif result == 'Positive':
                    sentiment = 1
                else:
                    sentiment = 0
                    ''' update in database '''
                users, created = PostUser.objects.get_or_create(UserID=message.get_user().get_user_id(),
                                                                DisplayName=message.get_user().get_display_name(),
                                                                DisplayPicture=message.get_user().get_display_picture())

                users.save()
                print()
                post = Post(PostUser_id=users.id,
                            Keyword_id=kwd_id,
                            StatusID=message.get_status_id(),
                            Content=message.get_text(),
                            CreatedAt=message.get_time(),
                            Sentiment=sentiment
                            )
                post.save()

    def get_reach(self, user_name, api, follower_count, post_id):
        page_count = 0
        loop = follower_count / 200
        iterations = follower_count % 200
        next_page = -1

        while page_count < loop:

            followers_list = api.GetFollowersPaged(
                screen_name=user_name, cursor=next_page)
            next_page = followers_list[0]
            for follower in followers_list[2]:
                statuses = api.GetUserTimeline(user_id=follower.id)
                for status in statuses:
                    if status.id_str == post_id:
                        no_of_followers_share = no_of_followers_share + 1

            page_count = page_count + 1

        else:

            followers_list = api.GetFollowersPaged(
                screen_name=user_name, count=iterations)
            for follower in followers_list[2]:
                statuses = api.GetUserTimeline(user_id=follower.id)
                for status in statuses:
                    if status.id_str == post_id:
                        no_of_followers_share = no_of_followers_share + 1

        reach = follower_count + no_of_followers_share

    def language_detection(self, text):
        ''' constrain the non-determinastic beahvour '''
        try:
            DetectorFactory.seed = 0
            languages_list = dict()
            languages = detect_langs(text)
            if len(languages) > 0:
                for lang in languages:
                    la = str(lang)
                    score = la.split(":")
                    languages_list[score[0]] = float(score[1])
                return max(languages_list.items(), key=operator.itemgetter(1))[0]
            else:
                return None
        except:
            return 'en'

    def detect_sentiment(self, text, analyser):
        ''' detect language and set the sentiments '''
        lang = self.language_detection(text)
        ''' for urdu '''
        if(lang == 'ur'):
            data = text.split('\n')
            pred_sentiment = predOnData(data)
            result = max(pred_sentiment, key=pred_sentiment.count)
        elif lang == None:
            result = 0
        else:
            ''' for english '''
            result = self.english_sentiment_analysis(text, analyser)

        return result

    def english_sentiment_analysis(self, text, analyser):
        result = ""
        if not text.strip():
            print(text)
            result = "Neutral"
        else:
            clean_text = self.clean_text(text)
            score = analyser.polarity_scores(clean_text)
            if (score['compound'] >= 0.05):
                result = "Positive"
            elif (score['compound'] > -0.05 and score['compound'] < 0.05):
                result = "Neutral"
            elif (score['compound'] < -0.05):
                result = "Negative"
        return result

    def clean_text(self, text):
        text = re.sub(
            r'\b(?:(?:https?|ftp)://)?\w[\w-]*(?:\.[\w-]+)+\S*', '', text)
        text = re.sub(r'…', '', text)
        text = re.sub(r'\.+', '.', text)
        text = re.sub(r'\?+', '?', text)
        text = text.replace(r'\'', '\'').replace(
            r'\"', '"').rstrip('\'').lstrip('\'').strip()
        return text

    def get_updated_tweets(self,keyword_id, keyword):
        print("kwwd id" + str(keyword_id))
        post_table = Post.objects.filter(Keyword_id=keyword_id).latest('CreatedAt')
        created_at = str(post_table.CreatedAt).split(" ")
        keyword_result = []
        last_post_date = created_at[0]
        last_post_time = created_at[1]
        last_post_time = datetime.strptime(last_post_time[:8], '%H:%M:%S')
        c = twint.Config()
        c.Search = keyword
        c.Limit = 10
        c.Database="dbTweets"
        c.Since = created_at[0][:10]
        c.Store_object = True
        twitter_response = twint.run.Search(c)
        for tweet in twitter_response:
            time_spam = datetime.strptime(tweet.timestamp[:10], '%H:%M:%S')
            if (last_post_time.time() < time_spam.time()):
                twitter_posts = Posts()
                twitter_posts_user = Users()
                twitter_posts.set_keyword(keyword)
                text = tweet.tweet
                twitter_posts.set_text(text)
                twitter_posts.set_status_id(tweet.id)
                twitter_posts.set_time(tweet.datestamp + " " + tweet.timestamp)
                twitter_posts_user.set_display_name(tweet.username)
                twitter_posts_user.set_display_picture(tweet.profile_image_url)
                twitter_posts_user.set_user_id(tweet.user_id_str)
                twitter_posts.set_user(twitter_posts_user)
                keyword_result.append(twitter_posts)
        self.add_to_database(keyword_result, keyword_id)
