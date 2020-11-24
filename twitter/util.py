import sys
import logging
import pymongo
import twitter.error
from datetime import datetime, timezone
from twitter.color import Colors as color
# from confusables import normalize

debug = logging.debug
err   = lambda m: sys.stderr.write(str(m)+'\n')
info  = lambda m: logging.info(f'{color.BLUE}{m}{color.END}')
warn  = lambda m: logging.warn(f'{color.YELLOW}{m}{color.END}')
wo_mentions = lambda t: " ".join(filter(lambda x: x[0]!='@', t.split()))
dateparse = lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M:%S %z')
now = lambda: datetime.now(timezone.utc)
dateformat = '%Y-%m-%d %H:%M:%S'

def readfile(fl):
	debug(f'reading file: {fl}')
	try:
		with open(fl) as f:
			return f.read().splitlines()
			f.close()
	except FileNotFoundError:
		sys.stderr.write(f'no such file or directory: {fl}\n')
		sys.exit(2)

def lastposf(mongocollection, query):
	try: return get_lastpos(mongocollection, query)
	except twitter.error.NoLastPositionData:
		return init_lastpos(mongocollection, query)

def init_lastpos(mongocollection, query):
	debug(f'initializing last pos value for {query}')
	return set_lastpos(mongocollection, query, now())

def set_lastpos(mongocollection, query, date):
	debug(f'setting last pos value for {query} to {date}')
	a = { "_id": query }
	b = { "_id": query, "lastpos": date }
	# try:
	server_result = mongocollection.replace_one(a, b, True)
	debug(f'replace_one() server result: {server_result.raw_result}')
	if server_result.raw_result['ok'] == 1.0: return date
	else:
		raise Exception() # TODO#2: dd
		# raise CannotSetLastPos(mongocollection, query, date) TODO#2: add this to twitter/error.py
	# except pymongo.errors.ServerSelectionTimeoutError:
	# 	logging.critical(f'could not connected to mongodb')
		# sys.exit(2)

def get_lastpos(mongocollection, query):
	debug(f'getting last pos value for {query}')
	try:
		result = mongocollection.find_one({"_id":query}, {'lastpos': 1, '_id': 0})
		if not result: raise twitter.error.NoLastPositionData(query)
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)
	date = result['lastpos']
	debug(f'last pos value for {query} is {date}')
	return date

def mongo_save(db, document, config):
	debug(f'saving: {document}')
	if not filters_pass(config.Search, document, config.Lang): return
	try: db.tweets.insert_one(document)
	except pymongo.errors.DuplicateKeyError: return
	else: # not a duplicate
		print(f'{document["capture_delay_sec"]:4.4f}',
			config.Search, document["tweet"], sep='\t')

def filters_pass(q, d, lang):
	language_is(lang, d['lang']) and includes(q, d['tweet'])

language_is = lambda l, d: d == l or d == 'und' # NOTE: Why the fuck twint
#                                                  language detecion is not
#                                                  working? So I have to write
#                                                  an extra filter?!!!

def includes(x, y):
	debug(f'checking whether or not {y} includes {x}')
	if x.lower() in wo_mentions(y.lower()):
		info(f'YES {x}: `{y}`')
		return True
	else:
		warn(f"NO {x}: `{y}`")
		return False
	# # FIXME: normalize('YEŞİL') -> ['#yefil', '#yefll', '#yesil', '#yesll']
	# if x.lower() in y.lower(): return True
	# # elif x.lower() in normalize(y, prioritize_alpha=True)[0]: return True
	# else: return False

