def tweetData(t):
    data = {
            "id": int(t.id),
            "conversation_id": t.conversation_id,
            "created_at": t.datetime,
            "date": t.datestamp,
            "time": t.timestamp,
            "timezone": t.timezone,
            "user_id": t.user_id,
            "username": t.username,
            "name": t.name,
            "place": t.place,
            "tweet": t.tweet,
            "mentions": t.mentions,
            "urls": t.urls,
            "photos": t.photos,
            "replies_count": int(t.replies_count),
            "retweets_count": int(t.retweets_count),
            "likes_count": int(t.likes_count),
            "location": t.location,
            "hashtags": t.hashtags,
            "link": t.link,
            "retweet": t.retweet,
            "quote_url": t.quote_url
            }
    return data

def tweetFieldnames():
    fieldnames = [
            "id",
            "conversation_id",
            "created_at",
            "date",
            "time",
            "timezone",
            "user_id",
            "username",
            "name",
            "place",
            "tweet",
            "mentions",
            "urls",
            "photos",
            "replies_count",
            "retweets_count",
            "likes_count",
            "location",
            "hashtags",
            "link",
            "retweet",
            "quote_url"
            ]
    return fieldnames

def userData(u):
    data = {
            "id": int(u.id),
            "name": u.name,
            "username": u.username,
            "bio": u.bio,
            "location": u.location,
            "url": u.url,
            "join_date": u.join_date,
            "join_time": u.join_time,
            "tweets": int(u.tweets),
            "following": int(u.following),
            "followers": int(u.followers),
            "likes": int(u.likes),
            "media": int(u.media_count),
            "private": u.is_private,
            "verified": u.is_verified,
            "profile_image_url": u.avatar,
            "background_image": u.background_image
            }
    return data

def userFieldnames():
    fieldnames = [
            "id",
            "name",
            "username",
            "bio",
            "location",
            "url",
            "join_date",
            "join_time",
            "tweets",
            "following",
            "followers",
            "likes",
            "media",
            "private",
            "verified",
            "profile_image_url",
            "background_image"
            ]
    return fieldnames

def usernameData(u):
    return {"username": u}

def usernameFieldnames():
    return ["username"]

def Data(obj, _type):
    if _type == "user":
        ret = userData(obj)
    elif _type == "username":
        ret = usernameData(obj)
    else:
        ret = tweetData(obj)

    return ret

def Fieldnames(_type):
    if _type == "user":
        ret = userFieldnames()
    elif _type == "username":
        ret = usernameFieldnames()
    else:
        ret = tweetFieldnames()

    return ret
