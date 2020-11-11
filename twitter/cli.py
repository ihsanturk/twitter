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
from datetime import datetime
from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

debug = logging.debug
logging.basicConfig(level=logging.WARN) #DEBUG)
dbclient = MongoClient(f'mongodb://{host}:{port}')
db = dbclient['twitter']

now = lambda: str(datetime.now()).split('.')[0]

def main():

	arg = docopt(__doc__, version='0.1.0')
	queries = readfile(arg['<queryfile>'])

	# twint config
	c = twint.Config()
	c.Store_json = True
	c.Store_object = True
	c.Output = "tweets.json" # just to satisfy the twint, not acutal write.
	c.Hide_output = True
	c.Lang = arg['--lang']

	db.tweets.create_index([("tweet", pymongo.TEXT)], # respects if exists
		background=True)

	# TODO: Create list of twint.Config for every query and use threadpool.
	# config_list = [ c for c in queries ]

	# action
	while True:

		#TODO#1: queue mechanism for getting like after t+5m, t+10m t+15m
		for query in queries:
			c.Search = query
			c.Since = str(lastposf(db.info, query))
			print(f'last position for {query}: {c.Since}') #NOTE: toggle uncomment
			try:
				twint.run.Search(c)
			except asyncio.exceptions.TimeoutError:
				continue
			try: #TODO#p: check if len(twint.output.tweets_list) > 0:
				lt = twint.output.tweets_list[0] # latest tweet
				print(f'\nlt: {lt.tweet}\n')
				set_lastpos(db.info, query, lt.datetime)
			except IndexError:
				sys.stderr.write(f'no tweets found: {query}')
				set_lastpos(db.info, query, now())

			twint.output.clean_lists()

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__ # see: readme.md twint tweets section to see fields.
	tweet['_id'] = tweet.pop('id'); # mongodb compatible id
	tweet['datetime'] = datetime.strptime(tweet.pop('datetime'),
		'%Y-%m-%d %H:%M:%S %Z') # convert string date to date object
	tweet['captured_datetime'] = datetime.now();
	delta = tweet['captured_datetime'] - tweet['datetime']
	tweet['captured_delay_sec'] = delta.total_seconds()
	mongo_save(db, tweet, config.Search)
module.Json = Json

import signal
def signal_handler(sig, frame): # clean up code
	sys.stderr.write('killing...\n')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
