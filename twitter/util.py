import sys
import logging
import pymongo
import twitter.error
from datetime import datetime, timezone
from twitter.color import Colors as color
# from confusables import normalize

debug        = logging.debug
dateformat   = '%Y-%m-%d %H:%M:%S'
now          = lambda: datetime.now(timezone.utc)
language_is  = lambda l, d: (d == l or d == 'und')
err          = lambda m: sys.stderr.write(str(m)+'\n')
init_lastpos = lambda mc, q: set_lastpos(mc, q, now())
includes     = lambda x, y: x.lower() in wo_mentions(y.lower())
info         = lambda m: logging.info(f'{color.BLUE}{m}{color.END}')
dateparse    = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S %z')
warn         = lambda m: logging.warn(f'{color.YELLOW}{m}{color.END}')
wo_mentions  = lambda t: " ".join(filter(lambda x: x[0]!='@', t.split()))
filters_pass = lambda q,d,l: language_is(l,d['lang']) and includes(q,d['tweet'])


def readfile(fl):
	debug(f'reading file: {fl}')
	try:
		with open(fl) as f:
			return f.read().splitlines()
			f.close()
	except FileNotFoundError:
		sys.stderr.write(f'no such file or directory: {fl}\n')
		sys.exit(2)

def lastposf(mc, query):
	try:
		return get_lastpos(mc, query)
	except twitter.error.NoLastPositionData:
		return init_lastpos(mc, query)

def set_lastpos(mc, query, date):
	debug(f'setting last pos value for {query} to {date}')
	a = { "_id": query }
	b = { "_id": query, "lastpos": date }
	# try:
	server_result = mc.replace_one(a, b, True)
	debug(f'replace_one() server result: {server_result.raw_result}')
	if server_result.raw_result['ok'] == 1.0: return date
	else:
		raise Exception() # TODO#2: dd
		# raise CannotSetLastPos(mc, query, date) TODO#2: add this to twitter/error.py
	# except pymongo.errors.ServerSelectionTimeoutError:
	# 	logging.critical(f'could not connected to mongodb')
		# sys.exit(2)

def get_lastpos(mc, query):
	debug(f'getting last pos value for {query}')
	try:
		result = mc.find_one({"_id":query}, {'lastpos': 1, '_id': 0})
		if not result:
			raise twitter.error.NoLastPositionData(query)
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)
	date = result['lastpos']
	debug(f'last pos value for {query} is {date}')
	return date

def mongo_save(db, document, config):
	debug(f'saving: {document}')
	if not filters_pass(config.Search, document, config.Lang):
		return
	try:
		db.tweets.insert_one(document)
	except pymongo.errors.DuplicateKeyError:
		return
	else: # not a duplicate
		print(f'{document["capture_delay_sec"]:4.4f}',
			config.Search, document["tweet"], sep='\t')

