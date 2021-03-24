"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] -u <username>
  twitter profile <username>
  twitter (-u <username> | --username <username>)
  twitter (-g | --guest-token)
  twitter (-h | --help)
  twitter --version

Options:
  -v --verbose              Print additional messages about processes.
  -g --guest-token          Get a guest token from Twitter.
  -h --help                 Show this screen.
  -u --user <username>      Show latest tweets of a user.
  --version                 Show the version."""

from docopt import docopt
from twitter.util import get_guest_token
from json import dumps
from sys import stderr, exit
import twitter.user

version = '2.1.0'


def main():

    arg = docopt(__doc__, version=version)

    if arg['--guest-token']:
        print(get_guest_token())

    if arg['profile']:
        if arg['<username>'] is not None:
            print(dumps(twitter.user.profile(user=arg['<username>'])),
                    flush=True)

    elif arg['stream']:
        if arg['--user'] is not None:
            try:
                for tweet in twitter.user.stream(user=arg['--user'],
                                                 verbose=arg['--verbose']):
                    print(dumps(tweet))
                    stdout.flush()
            except KeyboardInterrupt:
                print('^C')
        else:
            print('no user specified, please see --help', file=stderr)

    else:
        if arg['--user'] is not None:
            # FIXME: not implemented
            print('user profile not implemented')
            # print(twitter.user.last_tweets(arg['--user']))


if __name__ == '__main__':
    main()
