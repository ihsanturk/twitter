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

from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

import sys
import json
import time
import twint
import logging
import twitter.error
from docopt import docopt
from twitter.util import *

logging.basicConfig(level=logging.WARN) #DEBUG)
debug = logging.debug

dbclient = MongoClient(f'mongodb://{host}:{port}')
db = dbclient['twitter']

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

