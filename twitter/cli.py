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
	mongo_save(db.tweets, tweet)
module.Json = Json

def main():
	arg = docopt(__doc__, version='0.0.1')
	queries = readfile(arg['<queryfile>'])

	# twint config
	c = twint.Config()
	c.Store_json = True
	c.Output = "tweets.json" # just to satisfy the twint, not acutal write.
	# c.Custom["tweet"] = ['id', 'username', 'date', 'time', 'timezone',
	# 	'language', 'geo', 'link', 'replies', 'retweets', 'likes', 'tweet']
	c.Hide_output = True
	c.Lang = arg['--lang']

	# action
	while True:

		#TODO#2: queue mechanism for getting like after t+5m, t+10m t+15m
		for query in queries:
			c.Search = query
			c.Since = lastposf(db.info, query)
			twint.run.Search(c)
			set_lastpos(db.lastpos, query, twint.output.tweets_list[0].datetime)
			time.sleep(10) #TODO#p: delete
			print(twint.output.tweets_list[0].datetime) #TODO#p: dd
			try:
				lt = twint.output.tweets_list[0] # latest tweet
				lastpos = set_lastpos(lastpos_path, lt.datestamp+' '+lt.timestamp)
				set_lastpos(db.lastpos, query, twint.output.tweet_list[0].datetime)
			except IndexError:
				sys.stderr.write(f'twint could not fetch the tweets for {arg["<query>"]}\n')

if __name__ == '__main__':
	main()

