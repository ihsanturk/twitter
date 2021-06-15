from requests import get
from random import randint
from os import getenv

type_ = 'http'

# # free
# url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http'\
# '&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true'

# premium
url = 'https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list'\
     f'?auth={getenv("PROXYSCRAPE_API")}&protocol=http'


def refresh():
    """
    >>> proxies = refresh()
    ['ip:port', ...]
    """
    response = get(url)
    # if proxy scrape stop its service this will cause infinite loop
    return response.text.splitlines() if response.ok else refresh()


def get_nth(proxies, n):
    """
    >>> proxies = refresh()
    >>> proxy_dict = proxy.get_nth(proxies, 15)
    """
    return {
        'http':  'http://' + proxies[n],
        'https': 'http://' + proxies[n]
    }


def get_one_random(proxies):
    """
    >>> proxies = refresh()
    >>> proxy_dict = proxy.get_one_random(proxies)
    """
    random_index = randint(0, len(proxies)-1)
    return {
        'http':  'http://' + proxies[random_index],
        'https': 'http://' + proxies[random_index]
    }
