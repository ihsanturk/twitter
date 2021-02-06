import aiohttp

baseurl = 'mobile.twitter.com'


def getauthtoken():
    return aiohttp.get()


def search(phrase):
    getauthtoken()
    return aiohttp
