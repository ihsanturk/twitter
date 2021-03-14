"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] [ -u <username> ]
  twitter (-h | --help)
  twitter --version

Options:
  -g                        Get a guest token from Twitter.
  -h --help                 Show this screen.
  -u <username>             Get user latest tweets.
  --version                 Show the version.

"""

from docopt import docopt
import sys
from twitter.stream import stream
from twitter.util import getguesttoken

version = '2.0.1-alpha'


def main():
    arg = docopt(__doc__, version=version)

    print(arg)  # TODO: delete

    if arg['-g']:
        print(getguesttoken())
    if arg['stream'] is True and arg['-u'] is not None:
        stream(user=arg['-u'])
    else:
        print('no user specified, please see help using -h', file=sys.stderr)


if __name__ == '__main__':
    main()
