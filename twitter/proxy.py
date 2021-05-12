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
    """
    return get(url).text.splitlines()


def get_one_random(proxies):
    """
    >>> proxies = refresh()
    >>> ip, port = proxy.get_one(proxies, 15)
    """
    random_index = randint(0, len(proxies)-1)
    return {
        'http':  'http://' + proxies[random_index],
        'https': 'http://' + proxies[random_index]
    }
