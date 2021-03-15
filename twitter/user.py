from datetime import datetime, timezone
from requests import get
from twitter.constant import bearer_token, url_user_screen, user_agent
from twitter.util import get_guest_token
import sys

headers = {
    'User-Agent': user_agent,
    'authorization': bearer_token,
    'x-guest-token': get_guest_token()
}


def profile(user=None):
    """
    Returns User profile as JSON, with last status (tweet) that includes both
    Tweet & Replies.
    """
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

        profile_screen = profile(user=user)
        if 'status' in profile_screen:
            new_tweet = profile_screen['status']
        else:
            continue

        created_at = datetime.strptime(new_tweet['created_at'], time_format)
        captured_at = datetime.now(timezone.utc)
        time_delta = (captured_at - created_at)

        # TODO: delete ap
        print(f"since last tweet: {time_delta}", file=sys.stderr)

        # TODO: lower time_delta second check: it is currently 20 second range
        if time_delta.seconds < 10 and new_tweet is not last_reported_tweet:
            last_reported_tweet = new_tweet
            yield new_tweet
