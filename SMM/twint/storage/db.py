import sqlite3
import sys
import time
import hashlib

from SMM.TwintThread import TwintThread
from SMM.Posts import Posts
from SMM.Users import Users

databaseThread=TwintThread();

def Conn(database):
    if database:
        print("[+] Inserting into Database: " + str(database))
        conn = init(database)
        if isinstance(conn, str):
            print(str)
            sys.exit(1)
    else:
        conn = ""

    return conn

def init(db):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        table_users = """
            CREATE TABLE IF NOT EXISTS
                users(
                    id integer not null,
                    id_str text not null,
                    name text,
                    username text not null,
                    bio text,
                    location text,
                    url text,
                    join_date text not null,
                    join_time text not null,
                    tweets integer,
                    following integer,
                    followers integer,
                    likes integer,
                    media integer,
                    private integer not null,
                    verified integer not null,
                    profile_image_url text not null,
                    background_image text,
                    hex_dig  text not null,
                    time_update integer not null,
                    CONSTRAINT users_pk PRIMARY KEY (id, hex_dig)
                );
            """
        cursor.execute(table_users)

        table_tweets = """
            CREATE TABLE IF NOT EXISTS
                tweets (
                    id integer not null,
                    id_str text not null,
                    tweet text default '',
                    conversation_id text not null,
                    created_at integer not null,
                    date text not null,
                    time text not null,
                    timezone text not null,
                    place text default '',
                    location text not null,
                    replies_count integer,
                    likes_count integer,
                    retweets_count integer,
                    user_id integer not null,
                    user_id_str text not null,
                    screen_name text not null,
                    name text default '',
                    profile_image_url text,
                    link text,
                    mentions text,
                    hashtags text,
                    urls text,
                    photos text,
                    quote_url text,
                    video integer,
                    time_update integer not null,
                    PRIMARY KEY (id)
                );
        """
        cursor.execute(table_tweets)

        table_retweets = """
            CREATE TABLE IF NOT EXISTS
                retweets(
                    user_id integer not null,
                    tweet_id integer not null,
                    CONSTRAINT retweets_pk PRIMARY KEY(user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY(tweet_id) REFERENCES tweets(id)
                );
        """
        cursor.execute(table_retweets)

        table_favorites =  """
            CREATE TABLE IF NOT EXISTS
                favorites(
                    user_id integer not null,
                    tweet_id integer not null,
                    CONSTRAINT favorites_pk PRIMARY KEY (user_id, tweet_id),
                    CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users(id),
                    CONSTRAINT tweet_id_fk FOREIGN KEY (tweet_id) REFERENCES tweets(id)
                );
        """
        cursor.execute(table_favorites)

        table_followers = """
            CREATE TABLE IF NOT EXISTS
                followers (
                    id integer not null,
                    follower_id integer not null,
                    CONSTRAINT followers_pk PRIMARY KEY (id, follower_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT follower_id_fk FOREIGN KEY(follower_id) REFERENCES users(id)
                );
        """
        cursor.execute(table_followers)

        table_following = """
            CREATE TABLE IF NOT EXISTS
                following (
                    id integer not null,
                    following_id integer not null,
                    CONSTRAINT following_pk PRIMARY KEY (id, following_id),
                    CONSTRAINT id_fk FOREIGN KEY(id) REFERENCES users(id),
                    CONSTRAINT following_id_fk FOREIGN KEY(following_id) REFERENCES users(id)
                );
        """
        cursor.execute(table_following)

        table_followers_names = """
            CREATE TABLE IF NOT EXISTS
                followers_names (
                    user text not null,
                    time_update integer not null,
                    follower text not null,
                    PRIMARY KEY (user, follower)
                );
        """
        cursor.execute(table_followers_names)

        table_following_names = """
            CREATE TABLE IF NOT EXISTS
                following_names (
                    user text not null,
                    time_update integer not null,
                    follows text not null,
                    PRIMARY KEY (user, follows)
                );
        """
        cursor.execute(table_following_names)

        return conn
    except Exception as e:
        return str(e)

def fTable(Followers):
    if Followers:
        table = "followers_names"
    else:
        table = "following_names"

    return table

def uTable(Followers):
    if Followers:
        table = "followers"
    else:
        table = "following"

    return table

def follow(conn, Username, Followers, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        entry = (User, time_ms, Username,)
        table = fTable(Followers)
        query = f"INSERT INTO {table} VALUES(?,?,?)"
        cursor.execute(query, entry)
        conn.commit()
    except sqlite3.IntegrityError:
        pass

def get_hash_id(conn, id):
    cursor = conn.cursor()
    cursor.execute('SELECT hex_dig FROM users WHERE id = ? LIMIT 1', (id,))
    resultset = cursor.fetchall()
    return resultset[0][0] if resultset else -1

def user(conn, config, User):
    try:
        time_ms = round(time.time()*1000)
        cursor = conn.cursor()
        user = [int(User.id), User.id, User.name, User.username, User.bio, User.location, User.url,User.join_date, User.join_time, User.tweets, User.following, User.followers, User.likes, User.media_count, User.is_private, User.is_verified, User.avatar, User.background_image]

        hex_dig = hashlib.sha256(','.join(str(v) for v in user).encode()).hexdigest()
        entry = tuple(user) + (hex_dig,time_ms,)
        old_hash = get_hash_id(conn, User.id)

        if old_hash == -1 or old_hash != hex_dig:
            query = f"INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            cursor.execute(query, entry)
        else:
            pass

        if config.Followers or config.Following:
            table = uTable(config.Followers)
            query = f"INSERT INTO {table} VALUES(?,?)"
            cursor.execute(query, (config.User_id, int(User.id)))

        conn.commit()
    except sqlite3.IntegrityError:
        pass

#  store the tweet in django model in mysql instead of twint sqlite3
def tweets(conn, tweet, config):
    result=[]
    twitter_posts = Posts()
    twitter_posts_user = Users()
    twitter_posts.set_keyword(config.Search)
    text = tweet.tweet
    twitter_posts.set_text(text)
    twitter_posts.set_status_id(tweet.id)
    twitter_posts.set_time(tweet.datestamp + " " + tweet.timestamp)
    twitter_posts_user.set_display_name(tweet.username)
    twitter_posts_user.set_display_picture(tweet.profile_image_url)
    twitter_posts_user.set_user_id(tweet.user_id_str)
    twitter_posts.set_user(twitter_posts_user)
    result.append(twitter_posts)
    print(tweet.tweet)

    if (TwintThread.checkExistenceOfAPostForAUserKeyword(config.KwdID,tweet.id)):
        databaseThread.add_to_database(result,config.KwdID)

# def tweets(conn, Tweet, config):
#     try:
#         time_ms = round(time.time()*1000)
#         cursor = conn.cursor()
#         entry = (Tweet.id,
#                     Tweet.id_str,
#                     Tweet.tweet,
#                     Tweet.conversation_id,
#                     Tweet.datetime,
#                     Tweet.datestamp,
#                     Tweet.timestamp,
#                     Tweet.timezone,
#                     Tweet.place,
#                     Tweet.location,
#                     Tweet.replies_count,
#                     Tweet.likes_count,
#                     Tweet.retweets_count,
#                     Tweet.user_id,
#                     Tweet.user_id_str,
#                     Tweet.username,
#                     Tweet.name,
#                     Tweet.profile_image_url,
#                     Tweet.link,
#                     ",".join(Tweet.mentions),
#                     ",".join(Tweet.hashtags),
#                     ",".join(Tweet.urls),
#                     ",".join(Tweet.photos),
#                     Tweet.quote_url,
#                     Tweet.video,
#                     time_ms)
#         cursor.execute('INSERT INTO tweets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', entry)
#
#         if config.Favorites:
#             query = 'INSERT INTO favorites VALUES(?,?)'
#             cursor.execute(query, (config.User_id, Tweet.id))
#
#         if Tweet.retweet == 1:
#             query = 'INSERT INTO retweets VALUES(?,?)'
#             cursor.execute(query, (config.User_id, Tweet.id))
#
#         conn.commit()
#     except sqlite3.IntegrityError:
#         pass