from datetime import datetime, timezone
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
        raise(Exception('no user specified for function: profile()'))


def stream(user=None):
    last_reported_tweet = {}
    time_format = '%a %b %d %H:%M:%S %z %Y'
    while True:

        new_tweet = profile(user=user)['status']
        created_at = datetime.strptime(new_tweet['created_at'], time_format)
        time_delta = (datetime.now(timezone.utc) - created_at)

        # TODO: lower time_delta second check: it is currently 20 second range
        if time_delta.seconds < 20 and new_tweet is not last_reported_tweet:
            last_reported_tweet = new_tweet
            yield new_tweet
