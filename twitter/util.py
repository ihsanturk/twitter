from requests import get

url_activate = 'https://api.twitter.com/1.1/guest/activate.json'
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


def getguesttoken():
    return get(url_activate, headers={'authorization': bearer_token}).json()


