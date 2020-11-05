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
from twitter.util import *
from datetime import datetime
from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

debug = logging.debug
logging.basicConfig(level=logging.WARN) #DEBUG)
dbclient = MongoClient(f'mongodb://{host}:{port}')
db = dbclient['twitter']

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__ # see: readme.md twint tweets section to see fields.
	tweet['_id'] = tweet.pop('id'); # mongodb compatible id
	tweet['datetime'] = datetime.strptime(tweet.pop('datetime'), '%Y-%m-%d %H:%M:%S %Z')
	tweet['captured_datetime'] = datetime.now();
	delta = tweet['captured_datetime'] - tweet['datetime']
	tweet['captured_delay_sec'] = delta.total_seconds()
	mongo_save(db, tweet, config.Search)
module.Json = Json

def main():
	arg = docopt(__doc__, version='0.0.1')
	queries = readfile(arg['<queryfile>'])

	# twint config
	c = twint.Config()
	c.Store_json = True
	c.Store_object = True
	c.Output = "tweets.json" # just to satisfy the twint, not acutal write.
	c.Hide_output = True
	c.Lang = arg['--lang']
	c.Limit = 1; #TODO#p: dd

	# action
	while True:

		#TODO#0: queue mechanism for getting like after t+5m, t+10m t+15m
		for query in queries:
			c.Search = query
			c.Since = lastposf(db.info, query)
			twint.run.Search(c)
			try:
				lt = twint.output.tweets_list[0] # latest tweet
				set_lastpos(db.info, query, lt.datetime)
				time.sleep(10) #TODO#p: delete
			except IndexError:
				sys.stderr.write(f'twint could not fetch the tweets for {query}\n')
			except Exception as e:
				break

import signal
def signal_handler(sig, frame): # clean up code
	sys.stderr.write('killing...\n')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()
	signal.pause()

# # file approach
# set_lastpos(lastpos_path, lt.datestamp+' '+lt.timestamp)
