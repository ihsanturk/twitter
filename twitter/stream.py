from __future__ import print_function
from requests import get # TODO: delete
from twitter.util import getguesttoken
import sys

# baseurl = 'https://mobile.twitter.com'

def search(phrase):
    getguesttoken()
    return get() # FIXME: find the url to get after guest token


def stream(user=None):
    if user is not None:
        print('getting tweets:', user)
    else:
        print("no user specified", file=sys.stderr)
