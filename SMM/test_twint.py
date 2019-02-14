from datetime import datetime, timedelta

from SMM import twint

def get_updated_tweets(keyword_id, keyword):
    print("Keyword: " + keyword)

    # configure config object to get tweets
    c = twint.Config()
    c.Search = keyword
    c.KwdID = keyword_id
    c.Database = "dbTweets"
    c.Since = datetime.strftime(datetime.now() - timedelta(5), '%Y-%m-%d')
    print(c.Since)
    c.Until = datetime.strftime(datetime.now(), '%Y-%m-%d')
    print(c.Until)
    c.Store_object = True

    # search keyword with above configuration and the tweets will be stored sequentially after being scrapped
    twitter_response=twint.run.Search(c)
    print(twitter_response)

if __name__=="__main__":
    get_updated_tweets(3,"PayPal")