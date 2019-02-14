## TODO - Fix Weekday situation
from elasticsearch import Elasticsearch, helpers
from geopy.geocoders import Nominatim
from time import strftime, localtime
import contextlib
import sys

_index_tweet_status = False
_index_follow_status = False
_index_user_status = False
_is_near_def = False
_is_location_def = False
_near = {}
_location = {}

geolocator = Nominatim(user_agent="twint-1.2")

class RecycleObject(object):
    def write(self, junk): pass
    def flush(self): pass

def getLocation(place, **options):
    location = geolocator.geocode(place)
    if location:
        if options.get("near"):
            global _near
            _near = {"lat": location.latitude, "lon": location.longitude}
            return True
        elif options.get("location"):
            global _location
            _location = {"lat": location.latitude, "lon": location.longitude}
            return True
        return {"lat": location.latitude, "lon": location.longitude}
    else:
        return {}

def handleIndexResponse(response):
    try:
        if response["status"] == 400:
            return True
    except KeyError:
        pass
    if response["acknowledged"]:
        print("[+] Index \"" + response["index"] + "\" created!")
    else:
        print("[x] error index creation :: storage.elasticsearch.handleIndexCreation")
    if response["shards_acknowledged"]:
        print("[+] Shards acknowledged, everything is ready to be used!")
        return True
    else:
        print("[x] error with shards :: storage.elasticsearch.HandleIndexCreation")
        return False

def createIndex(config, instance, **scope):
    if scope.get("scope") == "tweet":
        tweets_body = {
                "mappings": {
                    "items": {
                        "properties": {
                            "id": {"type": "long"},
                            "conversation_id": {"type": "long"},
                            "created_at": {"type": "long"},
                            "date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                            "timezone": {"type": "keyword"},
                            "place": {"type": "keyword"},
                            "location": {"type": "keyword"},
                            "tweet": {"type": "text"},
                            "hashtags": {"type": "keyword"},
                            "user_id": {"type": "long"},
                            "user_id_str": {"type": "keyword"},
                            "username": {"type": "keyword"},
                            "name": {"type": "text"},
                            "profile_image_url": {"type": "text"},
                            "day": {"type": "integer"},
                            "hour": {"type": "integer"},
                            "link": {"type": "text"},
                            "retweet": {"type": "text"},
                            "essid": {"type": "keyword"},
                            "nlikes": {"type": "integer"},
                            "nreplies": {"type": "integer"},
                            "nretweets": {"type": "integer"},
                            "quote_url": {"type": "text"},
                            "search": {"type": "text"},
                            "near": {"type": "text"},
                            "geo_near": {"type": "geo_point"},
                            "geo_tweet": {"type": "geo_point"}
                            }
                        }
                    },
                    "settings": {
                        "number_of_shards": 1
                    }
                }
        with nostdout():
            resp = instance.indices.create(index=config.Index_tweets, body=tweets_body, ignore=400)
        return handleIndexResponse(resp)
    elif scope.get("scope") == "follow":
        follow_body = {
                "mappings": {
                    "items": {
                        "properties": {
                            "user": {"type": "keyword"},
                            "follow": {"type": "keyword"},
                            "essid": {"type": "keyword"}
                            }
                        }
                    },
                    "settings": {
                        "number_of_shards": 1
                    }
                }
        with nostdout():
            resp = instance.indices.create(index=config.Index_follow, body=follow_body, ignore=400)
        return handleIndexResponse(resp)
    elif scope.get("scope") == "user":
        user_body = {
                "mappings": {
                    "items": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "name": {"type": "keyword"},
                            "username": {"type": "keyword"},
                            "bio": {"type": "text"},
                            "location": {"type": "keyword"},
                            "url": {"type": "text"},
                            "join_datetime": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                            "join_date": {"type": "date", "format": "yyyy-MM-dd"},
                            "join_time": {"type": "date", "format": "HH:mm:ss"},
                            "tweets": {"type": "integer"},
                            "following": {"type": "integer"},
                            "followers": {"type": "integer"},
                            "likes": {"type": "integer"},
                            "media": {"type": "integer"},
                            "private": {"type": "integer"},
                            "verified": {"type": "integer"},
                            "avatar": {"type": "text"},
                            "background_image": {"type": "text"},
                            "session": {"type": "keyword"},
                            "geo_user": {"type": "geo_point"}
                            }
                        }
                    },
                    "settings": {
                        "number_of_shards": 1
                    }
                }
        with nostdout():
            resp = instance.indices.create(index=config.Index_users, body=user_body, ignore=400)
        return handleIndexResponse(resp)
    else:
        print("[x] error index pre-creation :: storage.elasticsearch.createIndex")
        return False

@contextlib.contextmanager
def nostdout():
    savestdout = sys.stdout
    sys.stdout = RecycleObject()
    yield
    sys.stdout = savestdout

def weekday(day):
    weekdays = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
            }

    return weekdays[day]

def hour(datetime):
    return strftime("%H", localtime(datetime))

def Tweet(Tweet, config):
    global _index_tweet_status
    global _is_near_def
    weekdays = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
            }
    day = weekdays[strftime("%A", localtime(Tweet.datetime))]

    actions = []

    dt = f"{Tweet.datestamp} {Tweet.timestamp}"

    j_data = {
            "_index": config.Index_tweets,
            "_type": config.Index_type,
            "_id": str(Tweet.id) + "_raw_" + config.Essid,
            "_source": {
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
                "essid": config.Essid,
                "nlikes": int(Tweet.likes_count),
                "nreplies": int(Tweet.replies_count),
                "nretweets": int(Tweet.retweets_count),
                "quote_url": Tweet.quote_url,
                "search": str(config.Search),
                "near": config.Near
                }
            }
    if config.Near or config.Geo:
        if not _is_near_def:
            __geo = ""
            __near = ""
            if config.Geo:
                __geo = config.Geo
            if config.Near:
                __near = config.Near
            _is_near_def = getLocation(__near + __geo, near=True)
        if _near:
            j_data["_source"].update({"geo_near": _near})
    if Tweet.place:
        _t_place = getLocation(Tweet.place)
        if _t_place:
            j_data["_source"].update({"geo_tweet": getLocation(Tweet.place)})
    actions.append(j_data)

    es = Elasticsearch(config.Elasticsearch)
    if not _index_tweet_status:
        _index_tweet_status = createIndex(config, es, scope="tweet")
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []

def Follow(user, config):
    global _index_follow_status
    actions = []

    j_data = {
            "_index": config.Index_follow,
            "_type": config.Index_type,
            "_id": user + "_" + config.Username + "_" + config.Essid,
            "_source": {
                "user": user,
                "follow": config.Username,
                "essid": config.Essid
                }
            }
    actions.append(j_data)

    es = Elasticsearch(config.Elasticsearch)
    if not _index_follow_status:
        _index_follow_status = createIndex(config, es, scope="follow")
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []

def UserProfile(user, config):
    global _index_user_status
    global _is_location_def
    actions = []

    j_data = {
            "_index": config.Index_users,
            "_type": config.Index_type,
            "_id": user.id + "_" + user.join_date + "_" + user.join_time + "_" + config.Essid,
            "_source": {
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
                "session": config.Essid
                }
            }
    if config.Location:
        if not _is_location_def:
            _is_location_def = getLocation(user.location, location=True)
        if _location:
            j_data["_source"].update({"geo_user": _location})
    actions.append(j_data)

    es = Elasticsearch(config.Elasticsearch)
    if not _index_user_status:
        _index_user_status = createIndex(config, es, scope="user")
    with nostdout():
        helpers.bulk(es, actions, chunk_size=2000, request_timeout=200)
    actions = []
