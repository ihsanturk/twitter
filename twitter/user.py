from datetime import datetime, timezone
from time import sleep
from twitter.constant import bearer_token, url_user_screen, user_agent, time_format
from twitter.util import get_guest_token
from requests import get
import sys

headers = {
    'User-Agent': user_agent,
    'authorization': bearer_token,
    'x-guest-token': get_guest_token()
}
stderr = sys.stderr


def profile(user=None):
    """
    Returns user profile as JSON, with last statuses (tweets) that includes
    both Tweet & Replies.
    """
    global headers
    if user is not None:

        response = get(url_user_screen + user, headers=headers)

        if response.ok:
            now = datetime.strftime(datetime.now(timezone.utc), time_format)
            response_json = response.json()
            response_json['captured_at'] = now
            return response_json

        elif response.status_code == 429:  # too many requests (rate limit)
            print('got 429 too many requests: refreshing guest token...',
                  file=stderr)
            print('guest token changed from ',headers['x-guest-token'],
                    end='', file=stderr)
            headers['x-guest-token']: get_guest_token()
            print(' {}'.format(headers['x-guest-token']), file=stderr)
            profile(user=user)

        else:
            response.raise_for_status()

    else:
        raise(Exception('no user specified for function: profile()'))


def stream(user=None):
    last_reported_tweet = {}
    counter = 1
    while True:

        print(counter, end='\t', file=stderr)
        counter += 1

        profile_screen = profile(user=user)
        if 'status' in profile_screen:  # if last tweet exists in JSON
            new_tweet = profile_screen['status']
        else:
            print('no last tweet object in profile JSON', file=stderr)
            continue

        created_at  = datetime.strptime(new_tweet['created_at'], time_format)
        captured_at = datetime.strptime(profile_screen['captured_at'],
                                        time_format)
        time_delta = (captured_at - created_at)

        print(f"since last tweet: {time_delta}", file=stderr)

        if time_delta.seconds < 60 and new_tweet is not last_reported_tweet:
            last_reported_tweet = new_tweet
            yield new_tweet
