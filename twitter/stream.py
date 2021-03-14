from __future__ import print_function
from requests import get # TODO: delete
from twitter.util import get_guest_token
from twitter.user import get_user_last_tweets
import sys

def stream(user=None):
    if user is not None:
        print('getting tweets:', user)
    else:
        print("no user specified", file=sys.stderr)
