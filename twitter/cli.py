"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] [<queryfile>]
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
  --mongo-host <string>     MongoDB host ip [default: localhost].
  --mongo-port <numeric>    MongoDB port [default: 27017].
  --mongo-pass <string>     MongoDB password.
  --mongo-user <string>     MongoDB username.
  -h --help                 Show this screen.
  --version                 Show the version.

"""

import sys
import json
import time
import twint
import logging
import twitter.error
from docopt import docopt
import asyncio.exceptions
from twitter.util import *
import twitter.proxy as proxy
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

version = '1.0.1'
max_thread_workers = 30 # 40:1m10s # 50:1m32s gives ocasianally warnings
logging.basicConfig(level=logging.ERROR)
suggest = lambda e: err(f'suggestion: {color.GREEN}{twitter.error.suggestions[e]}{color.END}')

def main():

	n, arg, queries = initialize()
	while True:
		config_list = [
			twint.Config(Search=q, Store_json=True, Store_object=True,
			Output="tweets.json", Hide_output = True, Lang = arg['--lang'])
			for q in queries
		]
		with ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
			executor.map(fetch, config_list)
			executor.shutdown(wait=True)
		err(f'cycle {cycle}')
		cycle += 1

# ---===---===---===---===---===---===---===---===---===---===---===---===--- #

def initialize():
	global db
	arg = docopt(__doc__, version=version)
	queries = readfile(arg['<queryfile>']) if arg['<queryfile>'] else sys.stdin.read().splitlines()
	dbclient = MongoClient(
		host = arg["--mongo-host"],
		port = int(arg["--mongo-port"]),
		username = arg["--mongo-user"],
		password = arg["--mongo-pass"]
	)
	db = dbclient['twitter']
	while True:
		try:
			warn('connecting & creating index for db:twitter->coll:tweets->field:tweet...')
			db.tweets.create_index([("tweet", pymongo.TEXT)], background=True)
			break
		except pymongo.errors.ServerSelectionTimeoutError:
			err(f'{color.RED}mongo timeout{color.END}')
			suggest("mongo_cannot_connect")
			# notify_error_via_email() #NOTE: Not implemented
			continue
	return 0, arg, queries

def fetch(c):
	lastpos_date = lastposf(db.info, c.Search).astimezone(tz=timezone.utc)
	c.Since = lastpos_date.strftime(dateformat) # string
	try: twint.run.Search(c)
	except asyncio.exceptions.TimeoutError as e:
		sys.stderr.write(str(e) + '\n'); pass
	else:
		try:
			lt = twint.output.tweets_list[0] # latest tweet
			err(f'{c.Search}: {len(twint.output.tweets_list) - 1} new tweet(s) since {c.Since}')
		except IndexError:
			err(f'no tweets found: {c.Search}')
			set_lastpos(db.info, c.Search, now())
		else: set_lastpos(db.info, c.Search, dateparse(f"{lt.datestamp} {lt.timestamp} {lt.timezone}"))
	twint.output.clean_lists()

# overwrite json method to store tweets in db.
def Json(obj, config):
	t = obj.__dict__ # see: readme.md twint tweets section to see fields.
	t['_id'] = t.pop('id'); # mongodb compatible id
	datestring = f"{t['datestamp']} {t['timestamp']} {t['timezone']}"
	t['datetime'] = dateparse(datestring)
	t['captured_datetime'] = now()
	delta = t['captured_datetime'] - t['datetime']
	t['capture_delay_sec'] = delta.total_seconds()
	mongo_save(db, t, config)
sys.modules["twint.storage.write"].Json = Json

import signal
def signal_handler(sig, frame): # clean up code
	err('killing...')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
