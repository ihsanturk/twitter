from requests import get
from twitter.constant import bearer_token, url_user_screen
from twitter.util import get_guest_token

headers = { 'authorization': bearer_token, 'x-guest-token': get_guest_token() }


def profile(user=None):
    if user is not None:
        response = get(url_user_screen + user, headers=headers)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
    else:
        raise(Exception(
            'no username specified for function: get_user_last_tweets()'))
