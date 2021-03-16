from datetime import datetime, timezone
from fake_useragent import UserAgent
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from twitter.constant import bearer_token, url_user_screen, user_agent, time_format
from twitter.util import get_guest_token
import sys

retry_strategy = Retry(
    total=1000,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'authorization': bearer_token,
    'x-guest-token': get_guest_token()
}


def profile(user=None):
    """
    Returns user profile as JSON, with last statuses (tweets) that includes
    both Tweet & Replies.
    """
    if user is not None:

        response = http.get(url_user_screen + user, headers=headers)

        if response.ok:
            now = datetime.strftime(datetime.now(timezone.utc), time_format)
            response_json = response.json()
            response_json['captured_at'] = now
            return response_json
        else:
            response.raise_for_status()

    else:
        raise(Exception('no user specified for function: profile()'))


def stream(user=None):
    global headers
    last_reported_tweet = {}
    counter = 1  # NOTE: stuck after 180
    while True:

        print(counter, end='\t', file=sys.stderr)
        counter += 1

        headers['User-Agent'] = ua.random
        profile_screen = profile(user=user)
        if 'status' in profile_screen:  # if last tweet exists in JSON
            new_tweet = profile_screen['status']
        else:
            print('no last tweet object in profile JSON', file=sys.stderr)
            continue

        created_at  = datetime.strptime(new_tweet['created_at'], time_format)
        captured_at = datetime.strptime(profile_screen['captured_at'],
                                        time_format)
        time_delta = (captured_at - created_at)

        # TODO: delete ap
        print(f"since last tweet: {time_delta}", file=sys.stderr)

        # TODO: lower time_delta second check: it is currently 20 second range
        if time_delta.seconds < 10 and new_tweet is not last_reported_tweet:
            last_reported_tweet = new_tweet
            yield new_tweet
