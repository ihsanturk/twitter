from time import sleep, time
from datetime import timedelta
from twitter.constant import bearer_token, url_user_screen, user_agent
from twitter.util import get_guest_token, snowflake2utc
from requests import get
from sys import stderr

headers = {
    'User-Agent': user_agent,
    'authorization': bearer_token,
    'x-guest-token': get_guest_token()
}
retry_on_http_error = [429, 500, 403]


def refresh_guest_token(verbose=False):
    global headers
    if verbose:
        print('guest token changed from ',headers['x-guest-token'], end='',
              file=stderr)
    headers['x-guest-token'] = get_guest_token()
    if verbose:
        print(' {}'.format(headers['x-guest-token']), file=stderr)


def profile(user=None, verbose=False):
    """
    Returns user profile as JSON, with last tatuses (tweets) that includes
    both Tweet & Replies.
    """
    if user is not None:

        response = get(url_user_screen + user, headers=headers)

        if response.ok:
            response_json = response.json()
            response_json['captured_at'] = time()
            return response_json

        elif response.status_code in retry_on_http_error:
            if verbose:
                print(f'\ngot {response.status_code}: refreshing guest token...',
                      file=stderr)
            refresh_guest_token(verbose=verbose)
            return profile(user=user, verbose=verbose)

        else:
            response.raise_for_status()

    else:
        raise(Exception('no user specified for function: profile()'))


def stream(user=None, verbose=False):
    last_reported_tweet = {'id': 0}
    counter = 0
    while True:
        counter += 1

        profile_screen = profile(user=user, verbose=verbose)
        if 'status' in profile_screen:  # if last tweet exists in JSON
            new_tweet = profile_screen['status']
        else:
            if verbose:
                print('\nno last tweet object in profile JSON', file=stderr)
            continue  # try again

        created_at = snowflake2utc(new_tweet['id'])
        time_delta = (profile_screen['captured_at'] - created_at)
        new_tweet['capture_latency_seconds'] = time_delta

        if verbose:
            print("\r{}\tsince {}'s last tweet: \033[33m{}\033[0m".format(
                  counter, user, timedelta(seconds=time_delta)),
                  end='', file=stderr)

        if time_delta < 60 and new_tweet['id'] is not last_reported_tweet['id']:
            last_reported_tweet = new_tweet
            yield new_tweet
