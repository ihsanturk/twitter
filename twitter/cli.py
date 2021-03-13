"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] -u <username>
  twitter (-h | --help)
  twitter --version

Options:
  -h --help                 Show this screen.
  -u <username>             Get user latest tweets.
  --version                 Show the version.

"""

from docopt import docopt
import sys
from twitter import stream

version = '2.0.1-alpha'


def main():
    arg = docopt(__doc__, version=version)
    print(arg)
    if arg['stream'] and arg['-u'] != None:
        stream()
    else:
        print('no user specified, please see help using -h', file=sys.stderr)


if __name__ == '__main__':
    main()
