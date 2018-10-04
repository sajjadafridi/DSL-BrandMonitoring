import twitter
from SMM.Post import Post
from SMM.User import User
import time
from datetime import datetime


def get_twitter_feed():
    api = twitter.Api(consumer_key='kWYGRMr4OuWGK2RfUs0dz1mRR',
                          consumer_secret='s298yX6M0hyIA460O320k7uM5ZfpVdqhbBYwWd7i5t6gfiOene',
                          access_token_key='3306982388-gaQA7otFm27ra1jnDvzEOpRm91PgOCpMbfTF7CK',
                          access_token_secret='jgYGV56beqcZBtnuUGBW0cUpr0Fvy830vrEFpYY2OVypB',
                           tweet_mode='extended',
                           sleep_on_rate_limit=True,
                      )
    resp =api.GetSearch(term = "Imran", count = 100)
    tweet_reponse_list=[]
    count=0
    for tweet in resp:
        tweet_info = Post()
        tweet_user = User()
        retweeter_list = []
        tweet_info.set_text(tweet.full_text)
        tweet_info.set_status_id(tweet.id_str)
        print(tweet.id_str)
        tweet_info.set_reshare_count(tweet.retweet_count)
        tweet_info.set_source("twitter")
        created_at = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
        tweet_info.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
        tweet_info.set_time(created_at)
        tweet_user.set_display_name(tweet.user.screen_name)
        tweet_user.set_display_picture(tweet.user.profile_image_url)
        tweet_user.set_follower_count(tweet.user.followers_count)
        tweet_user.set_following_count(tweet.user.friends_count)
        tweet_user.set_total_likes(tweet.user.favourites_count)
        tweet_user.set_total_post(tweet.user.statuses_count)
        tweet_user.set_user_id(tweet.user.id_str)
        tweet_user.set_location(tweet.user.location)
        created_at = datetime.strptime(tweet.user.created_at, '%a %b %d %H:%M:%S %z %Y')
        tweet_user.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
        retweeter_resp = api.GetRetweets(tweet.id_str)
        for retweeter in retweeter_resp:
            retweet_user = User()
            retweet_user.set_display_name(retweeter.user.screen_name)
            retweet_user.set_display_picture(retweeter.user.profile_image_url)
            retweet_user.set_follower_count(retweeter.user.followers_count)
            retweet_user.set_following_count(retweeter.user.friends_count)
            retweet_user.set_total_likes(retweeter.user.favourites_count)
            retweet_user.set_total_post(retweeter.user.statuses_count)
            retweet_user.set_user_id(retweeter.user.id_str)
            retweet_user.set_location(retweeter.user.location)
            created_at = datetime.strptime(retweeter.user.created_at, '%a %b %d %H:%M:%S %z %Y')
            retweet_user.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
            retweeter_list.append(retweet_user)
        count=count+1
        tweet_info.set_user(tweet_user)
        tweet_info.set_resharer(retweeter_list)
        tweet_reponse_list.append(tweet_info)
        print(count)











get_twitter_feed()