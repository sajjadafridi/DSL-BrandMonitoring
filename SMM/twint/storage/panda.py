from time import strftime, localtime
import pandas as pd
import warnings
from .elasticsearch import hour

Tweets_df = None
Follow_df = None
User_df = None

_object_blocks = {
    "tweet": [],
    "user": [],
    "following": [],
    "followers": []
}

weekdays = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5,
        "Saturday": 6,
        "Sunday": 7,
        }

_type = ""

def _concat(df, type):
    if df is None:
        df = pd.DataFrame(_object_blocks[type])
    else:
        _df = pd.DataFrame(_object_blocks[type])
        df = pd.concat([df, _df], sort=True)
    return df

def _autoget(type):
    global Tweets_df
    global Follow_df
    global User_df

    if type == "tweet":
        Tweets_df = _concat(Tweets_df, type)
    if type == "followers" or type == "following":
        Follow_df = _concat(Follow_df, type)
    if type == "user":
        User_df = _concat(User_df, type)


def update(object, config):
    global _type

    try:
        _type = ((object.type == "tweet")*"tweet" +
                 (object.type == "user")*"user")
    except AttributeError:
        _type = config.Following*"following" + config.Followers*"followers"

    if _type == "tweet":
        Tweet = object
        day = weekdays[strftime("%A", localtime(Tweet.datetime))]
        dt = f"{object.datestamp} {object.timestamp}"
        _data = {
            "id": str(Tweet.id),
            "conversation_id": Tweet.conversation_id,
            "created_at": Tweet.datetime,
            "date": dt,
            "timezone": Tweet.timezone,
            "place": Tweet.place,
            "location": Tweet.location,
            "tweet": Tweet.tweet,
            "hashtags": Tweet.hashtags,
            "user_id": Tweet.user_id,
            "user_id_str": Tweet.user_id_str,
            "username": Tweet.username,
            "name": Tweet.name,
            "profile_image_url": Tweet.profile_image_url,
            "day": day,
            "hour": hour(Tweet.datetime),
            "link": Tweet.link,
            "retweet": Tweet.retweet,
            "nlikes": int(Tweet.likes_count),
            "nreplies": int(Tweet.replies_count),
            "nretweets": int(Tweet.retweets_count),
            "quote_url": Tweet.quote_url,
            "search": str(config.Search),
            "near": config.Near
            }
        _object_blocks[_type].append(_data)
    elif _type == "user":
        user = object
        _data = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "bio": user.bio,
            "location": user.location,
            "url": user.url,
            "join_datetime": user.join_date + " " + user.join_time,
            "join_date": user.join_date,
            "join_time": user.join_time,
            "tweets": user.tweets,
            "following": user.following,
            "followers": user.followers,
            "likes": user.likes,
            "media": user.media_count,
            "private": user.is_private,
            "verified": user.is_verified,
            "avatar": user.avatar,
            "background_image": user.background_image,
            }
        _object_blocks[_type].append(_data)
    elif _type == "followers" or _type == "following":
        _data = {
            config.Following*"following" + config.Followers*"followers" :
                             {config.Username: object[_type]}
        }
        _object_blocks[_type] = _data
    else:
        print("Wrong type of object passed!")


def clean():
    _object_blocks["tweet"].clear()
    _object_blocks["following"].clear()
    _object_blocks["followers"].clear()
    _object_blocks["user"].clear()

def save(_filename, _dataframe, **options):
    if options.get("dataname"):
        _dataname = options.get("dataname")
    else:
        _dataname = "twint"

    if not options.get("type"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _store = pd.HDFStore(_filename + ".h5")
            _store[_dataname] = _dataframe
            _store.close()
    elif options.get("type") == "Pickle":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            _dataframe.to_pickle(_filename + ".pkl")
    else:
        print("""Please specify: filename, DataFrame, DataFrame name and type
              (HDF5, default, or Pickle)""")

def read(_filename, **options):
    if not options.get("dataname"):
        _dataname = "twint"
    else:
        _dataname = options.get("dataname")

    if not options.get("type"):
        _store = pd.HDFStore(_filename + ".h5")
        _df = _store[_dataname]
        return _df
    elif options.get("type") == "Pickle":
        _df = pd.read_pickle(_filename + ".pkl")
        return _df
    else:
        print("""Please specify: DataFrame, DataFrame name (twint as default),
              filename and type (HDF5, default, or Pickle""")
