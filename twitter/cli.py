"""twitter - Twitter scraper, streamer

Usage:
  twitter stream [options] [<queryfile>]
  twitter (-h | --help)
  twitter --version

Options:
  -l <lang>, --lang <lang>  Tweet language [default: tr].
  --mongo-host <string>     MongoDB host ip [default: localhost].
  --mongo-port <numeric>    MongoDB port [default: 27017].
  --mongo-pass <string>     MongoDB password.
  --mongo-user <string>     MongoDB username.
  -h --help                 Show this screen.
  --version                 Show the version.

"""

import sys
# import time
import twint
import signal
import logging
import twitter.error
from docopt import docopt
import asyncio.exceptions
import twitter.util as util
from datetime import timezone
import twitter.proxy as proxy
from twitter.color import Colors as color
from pymongo import MongoClient, TEXT, errors
import nest_asyncio
nest_asyncio.apply()

version = '1.2.3'
logging.basicConfig(level=logging.ERROR)


async def async_main(queries, lang):
	# issue: ~/Sync/issue/max-recursion.txt
	limit = 90  # TODO: make this auto (now: specific to the hardware)
	proxies = proxy.refresh()
	util.info(f'got {len(proxies)} proxies from proxyscrape')
	c = 0
	lastpos_dict = {
	    q: util.lastposf(db.info, q).astimezone(tz=timezone.utc)
	    for q in queries
	}
	print(lastpos_dict)  # TODO: dd
	sys.exit(0)  # TODO: dd
	while True:
		tasks = []
		for q in queries:
			ph, pp = proxy.get_one(proxies, (c % len(proxies)))
			util.info(f'using proxy: {ph}:{pp}')
			tasks.append(fetch(twint.Config(
			    Search=q, Store_json=True,
			    Store_object=True,
			    Output="tweets.json",
			    Hide_output=True, Lang=lang,
			    Proxy_host=ph, Proxy_port=pp,
			    Proxy_type=proxy.type_
			)))
			c += 1
		await util.gather_with_concurrency(limit, *tasks)


def initialize():
	global db
	arg = docopt(__doc__, version=version)
	if (arg['<queryfile>']) and (not arg['<queryfile>'] == '-'):
		queries = util.readfile(arg['<queryfile>'])
	else:
		queries = sys.stdin.read().splitlines()
	dbclient = MongoClient(host=arg["--mongo-host"],
	                       port=int(arg["--mongo-port"]),
	                       username=arg["--mongo-user"],
	                       password=arg["--mongo-pass"])
	db = dbclient['twitter']
	while True:
		util.warn('connecting & creating index for '
		          'db:twitter->coll:tweets->field:tweet...')
		try:
			db.tweets.create_index([("tweet", TEXT)], background=True)
		except errors.ServerSelectionTimeoutError:
			util.err(f'{color.RED}mongo timeout{color.END}')
			suggest("mongo_cannot_connect")
			# notify_error_via_email() #NOTE: Not implemented
			continue
		else:
			break

	return arg, queries


async def fetch(c):
	lastpos_date = util.lastposf(db.info, c.Search).astimezone(tz=timezone.utc)
	c.Since = lastpos_date.strftime(util.dateformat)  # string
	try:
		print(f'fetching tweets including {c.Search}')
		twint.run.Search(c)
	except (asyncio.exceptions.TimeoutError,
	        twint.token.RefreshTokenException) as e:
		util.err(str(e))
		# print('waiting for 5 secs')  # TODO: dd
		# time.sleep(5)  # TODO: dd
		pass
	else:
		try:
			lt = twint.output.tweets_list[0]  # latest tweet
		except IndexError:
			util.err(f'no tweets found: {c.Search}')
			util.set_lastpos(db.info, c.Search, util.now())
		else:
			util.err(f'{c.Search}: {len(twint.output.tweets_list) - 1} '
			         f'new tweet(s) since {c.Since}')
			util.set_lastpos(db.info, c.Search,
			                 util.dateparse(f'{lt.datestamp} {lt.timestamp} '
			                                f'{lt.timezone}'))
	twint.output.clean_lists()


def Json(obj, config):  # overwrite json method to store tweets in db.
	t = obj.__dict__  # see: readme.md twint tweets section to see fields.
	t['_id'] = t.pop('id')  # mongodb compatible id
	datestring = f"{t['datestamp']} {t['timestamp']} {t['timezone']}"
	t['datetime'] = util.dateparse(datestring)
	t['captured_datetime'] = util.now()
	delta = t['captured_datetime'] - t['datetime']
	t['capture_delay_sec'] = delta.total_seconds()
	util.mongo_save(db, t, config)


sys.modules["twint.storage.write"].Json = Json


def signal_handler(sig, frame):  # clean up code
	util.err('killing...')
	sys.exit(0)


def suggest(e):
	util.err('suggestion: '
	         f'{color.GREEN}{twitter.error.suggestions[e]}{color.END}')


def main():
	signal.signal(signal.SIGINT, signal_handler)
	arg, queries = initialize()
	asyncio.run(async_main(queries, arg['--lang']))


if __name__ == '__main__':
	main()
