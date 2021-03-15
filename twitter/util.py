from twitter.constant import url_base, bearer_token, user_agent
from requests import get
import re

def get_guest_token():
    response = get(url_base, headers={'User-Agent': user_agent})
    if response.ok:
        match = re.search(r'\("gt=(\d+);', response.text)
        if match:
            return match.group(1)
        else:
            raise(Exception('no guest token found in response'))
    else:
        response.raise_for_status()

