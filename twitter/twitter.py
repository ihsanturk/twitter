import aiohttp
import re

baseurl = 'https://mobile.twitter.com'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

re.sub(r'gt=\d\+',)
re.sub('[0-9]\+')

def getauthtoken():
    return aiohttp.get()


def search(phrase):
    getauthtoken()
    return aiohttp
