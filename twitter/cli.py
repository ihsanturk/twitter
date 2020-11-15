"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] <queryfile>
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
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
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from twitter.mongo_credentials import port, username, password, host

max_thread_workers = 40 # 40:1m10s # 50:1m32s gives ocasianally warnings
logging.basicConfig(level=logging.ERROR)
dbclient = MongoClient(f'mongodb://{host}:{port}')
db = dbclient['twitter']

suggest = lambda e: sys.stderr.write('suggestion: '+twitter.error.suggestions[e]+'\n')

def main():

	arg = docopt(__doc__, version='0.1.0')
	queries = readfile(arg['<queryfile>'])
	while True:
		try:
			db.tweets.create_index([("tweet", pymongo.TEXT)], # respects if exists
				background=True)
			break
		except pymongo.errors.ServerSelectionTimeoutError:
			suggest("mongo_cannot_connect")
			# notify_error_via_email() #NOTE: Not implemented
			continue

	# action
	#TODO#0: while loop: vip
	config_list = [
		twint.Config(Search=q, Store_json=True, Store_object=True,
		Output="tweets.json", Hide_output = True, Lang = arg['--lang'])
		for q in queries
	]
	with ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
		executor.map(fetch, config_list)
		executor.shutdown(wait=True)

	print('END') #TODO#: dd

def fetch(c):
	c.Since = lastposf(db.info,
		c.Search).astimezone(tz=timezone.utc).strftime(dateformat)
	print(f'{c.Search} since {c.Since}')
	try: twint.run.Search(c)
	except asyncio.exceptions.TimeoutError as e: error(e); pass
	else:
		try:
			lt = twint.output.tweets_list[0] # latest tweet
			print(f'tweet count: {len(twint.output.tweets_list)}') #TODO: dd
		except IndexError:
			sys.stderr.write(f'no tweets found: {c.Search}')
			set_lastpos(db.info, c.Search, now())
		else: set_lastpos(db.info, c.Search, dateparse(f"{lt.datestamp} {lt.timestamp} {lt.timezone}"))
	twint.output.clean_lists()

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	t = obj.__dict__ # see: readme.md twint tweets section to see fields.
	t['_id'] = t.pop('id'); # mongodb compatible id
	datestring = f"{t['datestamp']} {t['timestamp']} {t['timezone']}"
	t['datetime'] = dateparse(datestring)
	t['captured_datetime'] = now()
	delta = t['captured_datetime'] - t['datetime']
	t['capture_delay_sec'] = delta.total_seconds()
	mongo_save(db, t, config.Search)
module.Json = Json

import signal
def signal_handler(sig, frame): # clean up code
	sys.stderr.write('killing...\n')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
