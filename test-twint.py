import sys
import twint
from datetime import datetime

# overwrite json method to store tweets in db.
module = sys.modules["twint.storage.write"]
def Json(obj, config):
	tweet = obj.__dict__ # see: readme.md twint tweets section to see fields.
	tweet['_id'] = tweet.pop('id'); # mongodb compatible id
	tweet['datetime'] = datetime.strptime(tweet.pop('datetime'), '%Y-%m-%d %H:%M:%S %Z') # convert string date to date object
	tweet['captured_datetime'] = datetime.now();
	delta = tweet['captured_datetime'] - tweet['datetime']
	tweet['captured_delay_sec'] = delta.total_seconds()
	# print(tweet)
module.Json = Json

default = lambda d, v: d if not any(v) else v

def main():

	try: query = default('$thyao', sys.argv[1])
	except IndexError: query = '$thyao'

	# twint config
	c = twint.Config()
	c.Lang = 'tr'
	c.Search = query
	c.Search = query
	c.Store_json = True
	c.Hide_output = False
	# c.Store_object = True
	c.Since = '2020-01-01 22:00:01'
	c.Output = "tweets.json" # just to satisfy the twint, not acutal write.

	# action
	twint.run.Search(c)

	print(len(twint.output.tweets_list)) # count of tweets
	# print(twint.output.tweets_list[0].tweet) # first tweet text

import signal
def signal_handler(sig, frame): # clean up code
	sys.stderr.write('killing...\n')
	sys.exit(0)

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler)
	main()

