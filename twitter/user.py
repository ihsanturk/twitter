from requests import get
from twitter.util import get_guest_token
from twitter.constant import bearer_token, url_user_screen

headers = { 'authorization': bearer_token, 'x-guest-token': get_guest_token() }

def get_user_last_tweets(user=None):
    if user is not None:
        response = get(url_user_screen + user, headers=headers)
        if response.ok:
            return response.text
    else:
        raise(Exception(
            'no username specified for function: get_user_last_tweets()'))
