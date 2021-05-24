"""twitter - Twitter scraper, streamer

Usage:
  twitter (profile | stream) <username> [options]
  twitter (-g | --guest-token)
  twitter (-h | --help)
  twitter --version

Options:
  -v --verbose              Print additional messages about processes.
  -h --help                 Show this screen.
  -p --proxyscrape          ProxyScrape API key to use premium proxies.
  --version                 Show the version."""

from docopt import docopt
from twitter.util import get_guest_token
from json import dumps
from sys import stdout, stderr, exit
import twitter.user

version = '2.2.3'


def main():

    arg = docopt(__doc__, version=version)

    if arg['-g'] or arg['--guest-token']:
        print(get_guest_token())

    if arg['profile']:
        if arg['<username>'] is not None:
            print(dumps(twitter.user.profile(user=arg['<username>'],
                                             verbose=arg['--verbose'],
                                             useproxies=arg['--proxyscrape'])),
                  flush=True)

    elif arg['stream']:
        if arg['<username>'] is not None:
            try:
                for tweet in twitter.user.stream(user=arg['<username>'],
                                               verbose=arg['--verbose'],
                                               useproxies=arg['--proxyscrape']):
                    print(dumps(tweet))
                    stdout.flush()
            except KeyboardInterrupt:
                print('^C')
        else:
            print('no user specified, please see --help', file=stderr)

    elif arg['--help']:
        print(__doc__, file=stderr)
        exit(0)

    else:
        print(__doc__, file=stderr)
        exit(1)


if __name__ == '__main__':
    main()
