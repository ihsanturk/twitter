"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] [<queryfile>]
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
  -h --help                 Show this screen.
  --version                 Show the version.

"""

from docopt import docopt

version = '2.0.0-alpha'


def main():
    arg = docopt(__doc__, version=version)
    print(arg)
    pass


if __name__ == '__main__':
    main()
