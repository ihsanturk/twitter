from requests import get
from random import randint

type_ = 'http'
url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http'
'&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true'


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
    random_index = randint(0, len(proxies))
    return {
        'http':  'http://' + proxies[random_index],
        'https': 'http://' + proxies[random_index]
    }
