from datetime import timedelta
from requests import get, exceptions
from sys import stderr
from time import sleep, time
from twitter.constant import bearer_token, url_user_screen, user_agent
from twitter.util import get_guest_token, snowflake2utc
import twitter.proxy as proxy

headers = {
    'User-Agent': user_agent,
    'authorization': bearer_token,
    'x-guest-token': get_guest_token()
}
retry_on_http_error = [429, 500, 403, 503]
proxies_ = proxy.refresh()
proxy_index = 0
current_proxy = proxy.get_nth(proxies_, proxy_index)


def refresh_guest_token(verbose=False):
    global headers
    if verbose:
        print('guest token changed from ',headers['x-guest-token'], end='',
              file=stderr)
    headers['x-guest-token'] = get_guest_token()
    if verbose:
        print(' {}'.format(headers['x-guest-token']), file=stderr)


def profile(user=None, verbose=False, useproxies=False):
    """
    Returns user profile as JSON, with last tatuses (tweets) that includes
    both Tweet & Replies.
    """
    global current_proxy
    global proxies_
    global proxy_index

    if user is not None:

        try:
            if useproxies:
                if proxies_ == []:
                    proxies_ = proxy.refresh()
                    current_proxy = proxy.get_nth(proxies_, proxy_index)
                response = get(url_user_screen + user, headers=headers,
                               proxies=current_proxy)
            else:
                response = get(url_user_screen + user, headers=headers)
        except Exception as e:
            print(e, file=stderr)

            # rotate proxies_
            proxy_index += 1
            if proxy_index > len(proxies_)-1:
                proxies_ = proxy.refresh()
                proxy_index = 0
                if verbose:
                    print(f"{proxy_index = }", file=stderr)
                    print("refresh: proxies", file=stderr)
            if verbose:
                print(f"proxy changed from {current_proxy}", file=stderr,end='')
            current_proxy = proxy.get_nth(proxies_, proxy_index)
            if verbose:
                print(f" -> {current_proxy}", file=stderr)

            return profile(user=user, verbose=verbose, useproxies=useproxies)

        if response.ok:
            response_json = response.json()
            response_json['captured_at'] = time()
            return response_json

        # TODO: better retry logic: https://stackoverflow.com/a/35504626/12536010
        elif response.status_code in retry_on_http_error:
            if verbose:
                print(f'\ngot {response.status_code}. refreshing guest token...',
                      file=stderr)
            refresh_guest_token(verbose=verbose)
            return profile(user=user, verbose=verbose, useproxies=useproxies)

        else:
            response.raise_for_status()

    else:
        raise(Exception('no user specified for function: profile()'))


def stream(user=None, verbose=False, useproxies=False):
    last_reported_tweet = {'id': 0}
    counter = 0 # requests sent

    global current_proxy
    global proxies_
    global proxy_index

    while True:
        counter += 1

        profile_screen = profile(user=user, verbose=verbose,
                                 useproxies=useproxies)
        if 'status' in profile_screen:  # if last tweet exists in response JSON
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

        if time_delta < 60 and new_tweet['id'] != last_reported_tweet['id']:
            last_reported_tweet['id'] = new_tweet['id']
            yield new_tweet
