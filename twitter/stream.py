# import aiohttp
# import re

from requests import get # TODO: delete

# baseurl = 'https://mobile.twitter.com'
url_activate = 'https://api.twitter.com/1.1/guest/activate.json'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

# re.sub(r'gt=\d\+',)
# re.sub('[0-9]\+')


def getguesttoken():
    return get(url_activate, headers={'authorization': bearer_token}).json()
    # return aiohttp.get()


def search(phrase):
    getguesttoken()
    return get() # FIXME: find the url to get after guest token


def stream():
    print('getting user tweets')
