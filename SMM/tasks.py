import twitter
import moment
from celery.task import periodic_task
from celery.task import task
from apiclient import discovery
from SMM.Posts import Posts
from SMM.Users import Users
from SMM.models import *
from datetime import datetime
from celery.schedules import  crontab
from Analysis.SentimentAnalysis import SentimentAnalysis
import re
@task()
def scheduling_script():
    keywords = {}
    Keyword_table = Keyword.objects.all()
    for kwd in Keyword_table:
        if kwd.source_googleplus==True:
            googleplus_response = get_gplus_feed(kwd.alert_name, 3)
            add_to_database(googleplus_response, kwd.id)
        if kwd.source_twitter == True :
            twitter_response = get_twitter_feed(kwd.alert_name, 3)
            add_to_database(twitter_response, kwd.id)



def get_twitter_feed(keyword, limit=1):
    api = twitter.Api(consumer_key='kWYGRMr4OuWGK2RfUs0dz1mRR',
                          consumer_secret = 's298yX6M0hyIA460O320k7uM5ZfpVdqhbBYwWd7i5t6gfiOene',
                          access_token_key = '3306982388-gaQA7otFm27ra1jnDvzEOpRm91PgOCpMbfTF7CK',
                          access_token_secret = 'jgYGV56beqcZBtnuUGBW0cUpr0Fvy830vrEFpYY2OVypB',
                           tweet_mode = 'extended',
                           sleep_on_rate_limit=True,
                      )
    keyword_to_search = keyword
    resp = api.GetSearch(term = keyword_to_search, count = limit)
    tweet_reponse_list=[]
    count = 0
    for tweet in resp:
        tweet_info = Posts()
        tweet_user = Users()
        retweeter_list = []
        tweet_info.set_text(tweet.full_text)
        tweet_info.set_status_id(tweet.id_str)
        print(tweet.id_str)
        tweet_info.set_reshare_count(tweet.retweet_count)
        created_at = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S %z %Y')
        tweet_info.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
        tweet_info.set_time(created_at)
        tweet_info.set_keyword(keyword_to_search)
        tweet_info.set_source(1)
        user_name=''
        no_of_followers_share = 0
        no_of_follower=0



        if tweet.retweet_count==0:
            user_name=tweet.user.screen_name
            tweet_user.set_display_name(user_name)
            tweet_user.set_display_picture(tweet.user.profile_image_url)
            tweet_user.set_follower_count(tweet.user.followers_count)
            no_of_follower = tweet.user.followers_count
            print(tweet.user.followers_count)
            tweet_user.set_following_count(tweet.user.friends_count)
            tweet_user.set_total_likes(tweet.user.favourites_count)
            tweet_user.set_total_post(tweet.user.statuses_count)
            tweet_user.set_user_id(tweet.user.id_str)
            tweet_user.set_location(tweet.user.location)
            created_at = datetime.strptime(tweet.user.created_at, '%a %b %d %H:%M:%S %z %Y')
            tweet_user.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            user_name = tweet.retweeted_status.user.screen_name
            tweet_user.set_display_name(user_name)
            tweet_user.set_display_picture(tweet.retweeted_status.user.profile_image_url)
            tweet_user.set_follower_count(tweet.retweeted_status.user.followers_count)
            follower_count =tweet.retweeted_status.user.followers_count
            print(tweet.retweeted_status.user.followers_count)
            tweet_user.set_following_count(tweet.retweeted_status.user.friends_count)
            tweet_user.set_total_likes(tweet.retweeted_status.user.favourites_count)
            tweet_user.set_total_post(tweet.retweeted_status.user.statuses_count)
            tweet_user.set_user_id(tweet.retweeted_status.user.id_str)
            tweet_user.set_location(tweet.retweeted_status.user.location)
            created_at = datetime.strptime(tweet.retweeted_status.user.created_at, '%a %b %d %H:%M:%S %z %Y')
            tweet_user.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))

            reach= get_reach(user_name, api, follower_count,  tweet.id_str)

            retweeter_resp = api.GetRetweets(tweet.id_str)
            for retweeter in retweeter_resp:
                retweet_user = Users()
                retweet_user.set_display_name(retweeter.user.screen_name)
                retweet_user.set_display_picture(retweeter.user.profile_image_url)
                retweet_user.set_follower_count(retweeter.user.followers_count)
                retweet_user.set_following_count(retweeter.user.friends_count)
                retweet_user.set_total_likes(retweeter.user.favourites_count)
                retweet_user.set_total_post(retweeter.user.statuses_count)
                retweet_user.set_user_id(retweeter.user.id_str)

                statuses = api.GetUserTimeline(user_id=retweeter.user.id_str, count=10)
                t_text = ''
                for status in statuses:
                    t_text += status.full_text

                keyword_mentioned_count = len(re.findall(keyword_to_search.lower(), t_text.lower()))
                influence_score = keyword_mentioned_count * retweeter.user.followers_count
                retweet_user.set_influence_score(influence_score)
                retweet_user.set_location(retweeter.user.location)
                print(influence_score)
                created_at = datetime.strptime(retweeter.user.created_at, '%a %b %d %H:%M:%S %z %Y')
                retweet_user.set_time(created_at.strftime('%Y-%m-%d %H:%M:%S'))
                retweeter_list.append(retweet_user)
        count = count + 1
        tweet_info.set_user(tweet_user)
        tweet_info.set_resharer(retweeter_list)
        tweet_reponse_list.append(tweet_info)
        print(count)
    return tweet_reponse_list


def get_gplus_feed(keyword, limit=1):
    GPLUS = discovery.build('plus', 'v1', developerKey="AIzaSyBL8f2kQJSgpAu2pXdnqXhmGEcm3yXYtj0")
    postList = []
    try:
        activity = GPLUS.activities().search(query=keyword, maxResults=20).execute()
        counter = 0
        while (True):

            nextToken = activity['nextPageToken']
            items = activity.get('items', [])
            for data in items:
                post = ' '.join(data['title'].strip().split())
                if post:
                    post_info = Posts()
                    post_user = Users()
                    post_info.set_source('GooglePlus')
                    url = data["url"].split("/")
                    post_info.set_status_id(url[-1])
                    post_info.set_reshare_count(str(data["object"]["resharers"]['totalItems']))
                    post_info.set_text(data["object"]['content'])
                    post_info.set_source("googleplus")
                    post_info.set_keyword(keyword)
                    date = moment.date(data["published"], '%Y-%m-%dT%H:%M:%SZ')
                    sql_format = date.strftime('%Y-%m-%d %H:%M:%S')
                    post_info.set_time(sql_format)
                    post_user.set_user_id(data['actor']["id"])
                    post_user.set_display_name(data['actor']['displayName'])
                    post_user.set_display_picture(data['actor']['image']['url'])
                    post_info.set_user(post_user)
                    postList.append(post_info)
                    counter = counter + 1
                    print("--------------------------------------------" + str(counter))
                    if counter >= limit:
                        break
            if counter < limit:
                activity = GPLUS.activities().search(query=keyword, maxResults=20, pageToken=nextToken).execute()
            else:
                break
        return postList

    except Exception:
            print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')


def add_to_database(list, kwd_id):

    for message in list:
        analysis = SentimentAnalysis()
        sentiment=0
        sent = analysis.analysis(message.get_text(), "NLTK","/home/rehab/PycharmProjects/PYPI package/SentimentAnalysis/my_classifier.pickle")
        if sent=='Negative':
            sentiment=0
        else:
            sentiment=1


        users = PostUser(UserID=message.get_user().get_user_id(), DisplayName=message.get_user().get_display_name(),
                         DisplayPicture=message.get_user().get_display_picture(),
                         TotalLikes=message.get_user().get_total_likes(),
                         TotalPosts=message.get_user().get_total_post(),
                         FollowingCount=message.get_user().get_following_count(),
                         FollowerCount=message.get_user().get_follower_count(),
                         Location=message.get_user().get_location())
        users.save()
        post = Post(PostUser_id=users.id, Keyword_id=kwd_id, StatusID=message.get_status_id(),
                    Content=message.get_text(),
                    CreatedAt=message.get_time(), ResharerCount=message.get_reshare_count(),
                    Sentiment=sentiment, Source=message.get_Source()
                  )
        post.save()
        for resharer in [resharer for resharer in (message.get_resharer() or [])]:

            resharer_user = PostUser(UserID=resharer.get_user_id(), DisplayName=resharer.get_display_name(),
                                     DisplayPicture=resharer.get_display_picture(),
                                     TotalLikes=resharer.get_total_likes(), TotalPosts=resharer.get_total_post(),
                                     FollowingCount=resharer.get_following_count(),
                                     FollowerCount=resharer.get_follower_count(),
                                     Location=resharer.get_location())
            resharer_user.save()
            resharers = Resharer(PostUser_id=resharer_user.id, Post_id=post.id, Influence_score=resharer.get_influence_score())
            resharers.save()

def get_reach(user_name, api, follower_count, post_id):
    page_count = 0
    loop = follower_count / 200
    iterations = follower_count % 200
    next_page = -1

    while page_count < loop:

        followers_list = api.GetFollowersPaged(screen_name=user_name, cursor=next_page)
        next_page = followers_list[0]
        for follower in followers_list[2]:
            statuses = api.GetUserTimeline(user_id=follower.id)
            for status in statuses:
                if status.id_str == post_id:
                    no_of_followers_share = no_of_followers_share + 1

        page_count = page_count + 1

    else:

        followers_list = api.GetFollowersPaged(screen_name=user_name, count=iterations)
        for follower in followers_list[2]:
            statuses = api.GetUserTimeline(user_id=follower.id)
            for status in statuses:
                if status.id_str == post_id:
                    no_of_followers_share = no_of_followers_share + 1

    reach = follower_count + no_of_followers_share



