from time import sleep, time
from twitter.constant import bearer_token, url_user_screen, user_agent
from twitter.util import get_guest_token, snowflake2utc
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
    Returns user profile as JSON, with last tatuses (tweets) that includes
    both Tweet & Replies.
    """
    global headers
    if user is not None:

        response = get(url_user_screen + user, headers=headers)

        if response.ok:
            now = time()  # UTC
            response_json = response.json()
            response_json['captured_at'] = now
            return response_json

        elif response.status_code == 429:  # too many requests (rate limit)
            print('got 429 too many requests: refreshing guest token...',
                  file=stderr)
            print('guest token changed from ',headers['x-guest-token'],
                    end='', file=stderr)
            headers['x-guest-token'] = get_guest_token()
            print(' {}'.format(headers['x-guest-token']), file=stderr)
            return profile(user=user)

        else:
            response.raise_for_status()

    else:
        raise(Exception('no user specified for function: profile()'))


def stream(user=None):
    last_reported_tweet = {}
    counter = 0
    while True:
        counter += 1

        profile_screen = profile(user=user)
        if 'status' in profile_screen:  # if last tweet exists in JSON
            new_tweet = profile_screen['status']
            new_tweet['captured_at'] = profile_screen['captured_at']
        else:
            print('\nno last tweet object in profile JSON', file=stderr)
            continue

        created_at  = snowflake2utc(new_tweet['id'])
        time_delta  = (profile_screen['captured_at'] - created_at)
        new_tweet['capture_latency_seconds'] = time_delta

        print(f"\r{counter}\tsince last tweet: {time_delta}",
              end='', file=stderr)

        if time_delta < 60 and new_tweet['id'] is not last_reported_tweet['id']:
            last_reported_tweet = new_tweet
            yield new_tweet
