"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] <queryfile>
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
  --mongo-host <string>     MongoDB host ip [default: localhost].
  --mongo-port <numeric>    MongoDB port [default: 27017].
  --mongo-pass <string>     MongoDB password.
  --mongo-user <string>     MongoDB username.
  -l <lang>, --lang <lang>  Tweet language [default: tr].
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

max_thread_workers = 40 # 40:1m10s # 50:1m32s gives ocasianally warnings
logging.basicConfig(level=logging.DEBUG) #ERROR)
suggest = lambda e: sys.stderr.write('suggestion: '+twitter.error.suggestions[e]+'\n')

def main():

	arg = docopt(__doc__, version='0.1.0')
	queries = readfile(arg['<queryfile>'])
	dbclient = MongoClient(
		host = arg["--mongo-host"],
		port = int(arg["--mongo-port"]),
		username = arg["--mongo-user"],
		password = arg["--mongo-pass"]
	)
	if not input("""This program will [create and] use "twitter" db in mongodb.
Are you okay with that? [y/N]: """).startswith('y'):
		sys.stderr.write('bye then.\n')
		sys.exit(0)
	db = dbclient['twitter']
	while True:
		try:
			sys.stderr.write('creating index for db:twitter->coll:tweets->field:tweet\n')
			db.tweets.create_index([("tweet", pymongo.TEXT)], # respects if exists
				background=True)
			break
		except pymongo.errors.ServerSelectionTimeoutError:
			suggest("mongo_cannot_connect")
			# notify_error_via_email() #NOTE: Not implemented
			continue

	# action
	while True:
		config_list = [
			twint.Config(Search=q, Store_json=True, Store_object=True,
			Output="tweets.json", Hide_output = True, Lang = arg['--lang'])
			for q in queries
		]
		with ThreadPoolExecutor(max_workers=max_thread_workers) as executor:
			executor.map(fetch, config_list)
			executor.shutdown(wait=True)

def fetch(c):
	lastpos_date = lastposf(db.info, c.Search).astimezone(tz=timezone.utc)
	c.Since = lastpos_date.strftime(dateformat) # string
	try: twint.run.Search(c)
	except asyncio.exceptions.TimeoutError as e: error(e); pass
	else:
		try:
			lt = twint.output.tweets_list[0] # latest tweet
			sys.stderr.write(f'{c.Search}: {len(twint.output.tweets_list)} new tweet(s) since {c.Since}\n')
		except IndexError:
			sys.stderr.write(f'no tweets found: {c.Search}\n')
			set_lastpos(db.info, c.Search, now())
		else: set_lastpos(db.info, c.Search, dateparse(f"{lt.datestamp} {lt.timestamp} {lt.timezone}"))
	twint.output.clean_lists()

# no finished message should be
class NoMoreTweetsException(Exception):
	def __init__(self, msg): super().__init__()
sys.modules["twint.feed"].NoMoreTweetsException = NoMoreTweetsException

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
	sys.stderr.write('killing...\n')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
