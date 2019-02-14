from async_timeout import timeout
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import socket
import aiohttp
import asyncio
import concurrent.futures
import random
from json import loads
from aiohttp_socks import SocksConnector, SocksVer

from . import url
from .output import Tweets, Users
from .user import inf

#import logging

httpproxy = None

def get_connector(config):
    _connector = None
    if config.Proxy_host is not None:
        if config.Proxy_host.lower() == "tor":
            _connector = SocksConnector(
                socks_ver=SocksVer.SOCKS5,
                host='127.0.0.1',
                port=9050,
                rdns=True)
        elif config.Proxy_port and config.Proxy_type:
            if config.Proxy_type.lower() == "socks5":
                _type = SocksVer.SOCKS5
            elif config.Proxy_type.lower() == "socks4":
                _type = SocksVer.SOCKS4
            elif config.Proxy_type.lower() == "http":
                global httpproxy
                httpproxy = "http://" + config.Proxy_host + ":" + str(config.Proxy_port)
                return _connector
            else:
                print("Error: Proxy types allowed are: http, socks5 and socks4. No https.")
                sys.exit(1)
            _connector = SocksConnector(
                socks_ver=_type,
                host=config.Proxy_host,
                port=config.Proxy_port,
                rdns=True)
        else:
            print("Error: Please specify --proxy-host, --proxy-port, and --proxy-type")
            sys.exit(1)
    else:
        if config.Proxy_port or config.Proxy_type:
            print("Error: Please specify --proxy-host, --proxy-port, and --proxy-type")
            sys.exit(1)

    return _connector


async def RequestUrl(config, init, headers = []):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+requestURL')
    _connector = get_connector(config)

    if config.Profile:
        if config.Profile_full:
            _url = await url.MobileProfile(config.Username, init)
            response = await MobileRequest(_url, connector=_connector)
        else:
            _url = await url.Profile(config.Username, init)
            response = await Request(_url, connector=_connector, headers=headers)
    elif config.TwitterSearch:
        _url, params = await url.Search(config, init)
        response = await Request(_url, params=params, connector=_connector, headers=headers)
    else:
        if config.Following:
            _url = await url.Following(config.Username, init)
        elif config.Followers:
            _url = await url.Followers(config.Username, init)
        else:
            _url = await url.Favorites(config.Username, init)
        response = await MobileRequest(_url, connector=_connector)

    if config.Debug:
        print(_url, file=open("twint-request_urls.log", "a", encoding="utf-8"))

    return response

async def MobileRequest(url, **options):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+MobileRequest')
    connector = options.get("connector")
    if connector:
        async with aiohttp.ClientSession(connector=connector) as session:
            return await Response(session, url)
    async with aiohttp.ClientSession() as session:
        return await Response(session, url)

def ForceNewTorIdentity(config):
    try:
        tor_c = socket.create_connection(('127.0.0.1', config.Tor_control_port))
        tor_c.send('AUTHENTICATE "{}"\r\nSIGNAL NEWNYM\r\n'.format(config.Tor_control_password).encode())
        response = tor_c.recv(1024)
        if response != b'250 OK\r\n250 OK\r\n':
            sys.stderr.write('Unexpected response from Tor control port: {}\n'.format(response))
    except Exception as e:
        sys.stderr.write('Error connecting to Tor control port: {}\n'.format(repr(e)))
        sys.stderr.write('If you want to rotate Tor ports automatically - enable Tor control port\n')

async def Request(url, connector=None, params=[], headers=[]):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+Request')
    if connector:
        async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
            return await Response(session, url, params)
    async with aiohttp.ClientSession() as session:
        return await Response(session, url, params)

async def Response(session, url, params=[]):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+Response')
    with timeout(30):
        async with session.get(url, ssl=False, params=params, proxy=httpproxy) as response:
            return await response.text()

async def RandomUserAgent():
    url = "https://fake-useragent.herokuapp.com/browsers/0.1.8"
    r = await Request(url)
    browsers = loads(r)['browsers']
    return random.choice(browsers[random.choice(list(browsers))])

async def Username(_id):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+Username')
    url = f"https://twitter.com/intent/user?user_id={_id}&lang=en"
    r = await Request(url)
    soup = BeautifulSoup(r, "html.parser")

    return soup.find("a", "fn url alternate-context")["href"].replace("/", "")

async def Tweet(url, config, conn):
    #loggin.info("[<] " + str(datetime.now()) + ':: Tweet')
    try:
        response = await Request(url)
        soup = BeautifulSoup(response, "html.parser")
        location = soup.find("span", "ProfileHeaderCard-locationText u-dir").text
        location = location[15:].replace("\n", " ")[:-10]
        tweets = soup.find_all("div", "tweet")
        await Tweets(tweets, location, config, conn, url)
    except Exception as e:
        print(str(e) + " [x] get.Tweet")

async def User(url, config, conn, user_id = False):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+User')
    _connector = get_connector(config)
    try:
        response = await Request(url, connector=_connector)
        soup = BeautifulSoup(response, "html.parser")
        await Users(soup, config, conn)
        if user_id:
            return int(inf(soup, "id"))
    except Exception as e:
        print(str(e) + " [x] get.User")

def Limit(Limit, count):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+Limit')
    if Limit is not None and count >= int(Limit):
        return True

async def Multi(feed, config, conn):
    #loggin.info("[<] " + str(datetime.now()) + ':: get+Multi')
    count = 0
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for tweet in feed:
                count += 1
                if config.Favorites or config.Profile_full:
                    link = tweet.find("a")["href"]
                    url = f"https://twitter.com{link}&lang=en"
                elif config.User_full:
                    username = tweet.find("a")["name"]
                    url = f"http://twitter.com/{username}?lang=en"
                else:
                    link = tweet.find("a", "tweet-timestamp js-permalink js-nav js-tooltip")["href"]
                    url = f"https://twitter.com{link}?lang=en"

                if config.User_full:
                    futures.append(loop.run_in_executor(executor, await User(url,
                        config, conn)))
                else:
                    futures.append(loop.run_in_executor(executor, await Tweet(url,
                        config, conn)))

            await asyncio.gather(*futures)
    except Exception as e:
        # TODO: fix error not error
        # print(str(e) + " [x] get.Multi")
        # will return "'NoneType' object is not callable"
        # but still works
        pass

    return count
