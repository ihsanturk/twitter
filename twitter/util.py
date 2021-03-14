from requests import get
import re

url_base     = 'https://twitter.com'
url_mobile   = 'https://mobile.twitter.com'
url_activate = 'https://api.twitter.com/1.1/guest/activate.json'

bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
useragent    = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'

def getguesttoken():
    response = get(url_base, headers={'User-Agent': useragent})
    if response.ok:
        match = re.search(r'\("gt=(\d+);', response.text)
        if match:
            return match.group(1)
        else:
            raise(Exception('no guest token found in response'))
    else:
        response.raise_for_status()

