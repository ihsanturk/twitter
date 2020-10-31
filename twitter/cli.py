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

# import redis
# from twitter.redis_credentials import port, username, password, host

from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

import sys
import json
import time
import twint
import logging
from docopt import docopt
from twitter.util import *

logging.basicConfig(level=logging.DEBUG) #WARN)
debug = logging.debug

# dbclient = redis.Redis(username=username, password=password, host=host, port=port, ssl=True)
dbclient = MongoClient(f'mongodb://{host}:{port}')
db = dbclient['twitter']

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__ # see: readme.md twint tweets section to see fields.
	tweet['_id'] = tweet.pop('id'); # mongodb compatible id
	print(tweet['username']+'\t'+tweet['_id']) #TODO#p: DELETE
	# mongo_save(db.tweets, tweet)
module.Json = Json

def main():
	arg = docopt(__doc__, version='0.0.1')
	companies = readfile(arg['<queryfile>'])

	# twint config
	c = twint.Config()
	c.Store_json = True
	c.Output = "tweets.json"
	c.Custom["tweet"] = ['id', 'username', 'date', 'time', 'timezone',
		'language', 'geo', 'link', 'replies', 'retweets', 'likes', 'tweet']
	c.Hide_output = True
	c.Lang = arg['--lang']

	# action
	#TODO#1: db duplicate issue
	while True:
		for company in companies:
			lp = get_lastpos(db.info, company)
			if not lp:
				debug(f"can't find last position value for {company}")
				lp = init_lastpos(db.info, company)
			print(lp)
			c.Search = company
			c.Since = lp
			twint.run.Search(c)
			set_lastpos(db.lastpos, company, twint.output.tweet_list[0].datetime)
			# #TODO#2: queue mechanism for getting like after t+5m, t+10m t+15m
			time.sleep(10) #TODO#p: DELETE

	# # action
	# lastpos = get_lastpos(r, company)
	# if not any(lastpos):
	# 	init_lastpos(lastpos_path)
	# if arg['stream']:
	# 	while True:
	# 		c.Since = get_lastpos(lastpos_path)
	# 		twint.run.Search(c)
	# 		try:
	# 			lt = twint.output.tweets_list[0] # latest tweet
	# 			lastpos = set_lastpos(lastpos_path, lt.datestamp+' '+lt.timestamp)
	# 		except IndexError:
	# 			sys.stderr.write(f'twint could not fetch the tweets for {arg["<query>"]}\n')
	# 		time.sleep(1)


if __name__ == '__main__':
	main()

