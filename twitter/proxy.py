from requests import get

type_ = 'http'
url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http'
'&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true'


def refresh():
    """
    >>> proxies = refresh()
    """
    return get(url).text.splitlines()


def get_one(proxies, i):
    """
    >>> proxies = refresh()
    >>> ip, port = proxy.get_one(proxies, 15)
    """
    return (proxies[i].split(':')[0], proxies[i].split(':')[1])
