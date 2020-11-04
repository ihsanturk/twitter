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

# NOTE: THIS FILE MAY NOT WORK

import redis
from twitter.redis_credentials import port, username, password, host

import sys
import json
import time
import twint
import logging
from docopt import docopt
from twitter.util import *

logging.basicConfig(level=logging.DEBUG) #WARN)
debug = logging.debug

dbclient = redis.Redis(username=username, password=password, host=host, port=port, ssl=True)

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__ # see: readme.md twint tweets section to see fields.
	print(tweet['username']+'\t'+tweet['_id']) #TODO#p: DELETE
	# redis_save(db.tweets, tweet) #TODO#0
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
	#TODO#0: db duplicate issue
	while True:
		for company in companies:
			lp = get_lastpos(db.info, company)
			if not lp: lp = init_lastpos(db.info, company)
			print(lp) #TODO#p: delete
			c.Search = company
			c.Since = lp
			twint.run.Search(c)
			set_lastpos(db.lastpos, company, twint.output.tweet_list[0].datetime)
			# #TODO#2: queue mechanism for getting like after t+5m, t+10m t+15m
			time.sleep(10) #TODO#p: DELETE

if __name__ == '__main__':
	main()


