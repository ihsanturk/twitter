"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] <query>
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
  -h --help                 Show this screen.
  --version                 Show the version.

"""

import sys
import time
import twint
from pathlib import Path
from docopt import docopt


def main():

	# var
	arg = docopt(__doc__, version='0.0.1')
	lastpos_dir = 'lastpos'
	lastpos_path = f"{lastpos_dir}/{arg['<query>']}"

	# twint config
	c = twint.Config()
	c.Search = arg['<query>']
	c.Lang = arg['--lang']
	c.Store_object = True
	# c.Hide_output = True
	outputformat = [ # TODO: get this from user
		'{id}',
		'{username}',
		'{date} {time} {timezone}',
		'{language}',
		'{geo}',
		'{link}',
		'{replies}',
		'{retweets}',
		'{likes}',
		'{tweet}'
	]
	c.Format = '\t'.join(outputformat)

	# action
	mkdir(lastpos_dir)
	lastpos = get_lastpos(lastpos_path)
	if not any(lastpos):
		init_lastpos(lastpos_path)
	if arg['stream']:
		while True:
			c.Since = get_lastpos(lastpos_path)
			twint.run.Search(c)
			try:
				lt = twint.output.tweets_list[0] # latest tweet
				lastpos = set_lastpos(lastpos_path, lt.datestamp+' '+lt.timestamp)
			except IndexError:
				sys.stderr.write(f'twint could not fetch the tweets for {arg["<query>"]}\n')
			time.sleep(1)


def set_lastpos(path, date):
	with open(path, 'w') as f:
		lastpos = f.write(date)
		f.close()
	return date

def get_lastpos(path):
	try:
		with open(path, 'r') as f:
			lastpos = f.read().strip()
			f.close()
		return lastpos
	except FileNotFoundError:
		return ''

def init_lastpos(path):
	p = '2000-01-01 00:00:00'
	p = '2020-10-27 21:00:00' # TODO: dd
	with open(path, 'w') as f: f.write(p); f.close();
	return p

def mkdir(path):
	# TODO: increment dirname until it gets unique
	Path(path).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
	main()

