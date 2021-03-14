"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] -u <username>
  twitter profile <username>
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
from twitter.util import get_guest_token
import json
import sys
import twitter.user

version = '2.0.1-alpha'


def main():
    arg = docopt(__doc__, version=version)

    if arg['--guest-token']:
        print(get_guest_token())

    if arg['profile']:
        if arg['<username>'] is not None:
            print(json.dumps(twitter.user.profile(user=arg['<username>'])))

    elif arg['stream']:
        if arg['--user'] is not None:
            twitter.user.stream(user=arg['--user'])
        else:
            print('no user specified, please see --help', file=sys.stderr)

    else:
        if arg['--user'] is not None:
            print(twitter.user.last_tweets(arg['--user']))


if __name__ == '__main__':
    main()
