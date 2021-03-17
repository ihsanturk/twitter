from requests import get
from twitter.constant import url_base, bearer_token, user_agent
import re
import sys

stderr = sys.stderr

def get_guest_token():
    response = get(url_base, headers={'User-Agent': user_agent})
    if response.ok:
        match = re.search(r'\("gt=(\d+);', response.text)
        if match:
            return match.group(1)
        else:
            print(f'no guest token found in response: {url_base}. retrying to'\
                   ' get guest token...', file=stderr)
            get_guest_token()
    else:
        response.raise_for_status()

