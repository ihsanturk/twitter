from __future__ import print_function
from requests import get # TODO: delete
from util import getguesttoken
import sys

# baseurl = 'https://mobile.twitter.com'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'

# re.sub(r'gt=\d\+',)
# re.sub('[0-9]\+')


def search(phrase):
    getguesttoken()
    return get() # FIXME: find the url to get after guest token


def stream(user=None):
    if user is not None:
        print('getting tweets:', user)
    else:
        print("no user specified", file=sys.stderr)
