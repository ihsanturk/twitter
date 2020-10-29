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
import redis
import twint
import logging
from docopt import docopt
from twitter.util import *
from twitter.redis_credentials import port, username, password, host

logging.basicConfig(level=logging.DEBUG)
debug = logging.debug

r = redis.Redis(username=username, password=password, host=host, port=port, ssl=True)

# overwrite json method to store tweets in redis.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__
	# r.set('tweets.$company') #TODO#0: JSON.set('tweets.company.'+tweet) see: https://github.com/RedisJSON/redisjson-py
	print(type(tweet), tweet)
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
	while True:
		for company in companies:
			lp = get_lastpos(r, company)
			if not lp: lp = init_lastpos(r, company)
			c.Search = company
			c.Since = lp
			tweet = twint.run.Search(c)
			time.sleep(1)
			# redis.JSON.set(company, tweet, lp) #TODO#0

			# #TODO#1: queue mechanism for getting like after t+5m, t+10m t+15m
			# redis_push_queue(after_5_min, company)


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


def readfile(fl):
	debug(f'reading file: {fl}')
	try:
		with open(fl) as f:
			return f.read().splitlines()
			f.close()
	except FileNotFoundError:
		yellerr(f'no such file or directory: {arg["<queryfile>"]}\n')
		sys.exit(2)

def set_lastpos(redis_client, query, date):
	debug('setting last pos value')
	lastpos = redis_client.set('lastpos:'+query, date)
	return date

def get_lastpos(redis_client, query):
	#TODO#p: handle errors
	debug('getting last pos value')
	lastpos = redis_client.get('lastpos:'+query).decode("utf-8")
	return lastpos

def init_lastpos(redis_client, query):
	debug('initializing last pos value')
	p = '2000-01-01 00:00:00'
	p = '2020-10-27 21:00:00' #TODO#p: dd
	lastpos = redis_client.set('lastpos:'+query, p)
	return p

if __name__ == '__main__':
	main()

