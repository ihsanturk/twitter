"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] [ -u <username> ]
  twitter (-u <username> | --username <username>)
  twitter (-g | --guest-token)
  twitter (-h | --help)
  twitter --version

Options:
  -g --guest-token          Get a guest token from Twitter.
  -h --help                 Show this screen.
  -u --user <username>      Show latest tweets of a user.
  --version                 Show the version.

"""

from docopt import docopt
from twitter.stream import stream
from twitter.util import get_guest_token
import sys

version = '2.0.1-alpha'


def main():
    arg = docopt(__doc__, version=version)

    print(arg)  # TODO: delete

    if arg['--guest-token']:
        print(get_guest_token())
    else:
        if arg['stream'] is True and arg['--user'] is not None:
            stream(user=arg['--user'])
        else:
            print('no user specified, please see help using -h', file=sys.stderr)


if __name__ == '__main__':
    main()
