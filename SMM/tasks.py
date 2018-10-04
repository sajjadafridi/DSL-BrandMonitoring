import twitter
from SMM.PostMessage import Message
def get_twitter_feed():
    api = twitter.Api(consumer_key='kWYGRMr4OuWGK2RfUs0dz1mRR',
                          consumer_secret='s298yX6M0hyIA460O320k7uM5ZfpVdqhbBYwWd7i5t6gfiOene',
                          access_token_key='3306982388-gaQA7otFm27ra1jnDvzEOpRm91PgOCpMbfTF7CK',
                          access_token_secret='jgYGV56beqcZBtnuUGBW0cUpr0Fvy830vrEFpYY2OVypB',
                      tweet_mode='extended')
    resp =api.GetSearch(term="Imran",count=15)
    for tweet in resp:
        tweet_info =Message()
        tweet_info.set_Content(str(tweet.full_text))
        tweet_info.set_DisplayPicture()







get_twitter_feed()