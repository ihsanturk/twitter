from requests import get
from sys import stderr
from twitter.constant import bearer_token
from twitter.constant import url_base
from twitter.constant import url_user_by_screen_name
from twitter.constant import user_agent
import re

proxies_ = {}

def get_guest_token():
    response = get(url_base, headers={'User-Agent':user_agent},proxies=proxies_)
    if response.ok:
        match = re.search(r'\("gt=(\d+);', response.text)
        if match:
            return match.group(1)
        else:
            print(f'no guest token found in response: {url_base}. retrying to'\
                   ' get guest token...', file=stderr)
            return get_guest_token()
    else:
        response.raise_for_status()


def get_user_id(username):
    headers = {
        'User-Agent': user_agent,
        'authorization': bearer_token,
        'x-guest-token': get_guest_token()
    }
    response = get(url_user_by_screen_name, headers=headers, proxies=proxies_)
    if response.ok:
        print(response.json)
    else:
        response.raise_for_status()


def snowflake2utc(tweetid):
    return ((tweetid >> 22) + 1288834974657) / 1000.0

