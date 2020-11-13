import sys
import logging
import pymongo
import twitter.error
from color import Colors as color
# from confusables import normalize

debug = logging.debug
info  = lambda m: logging.info(f'{color.BLUE}{m}{color.END}')
warn  = lambda m: logging.warn(f'{color.RED}{m}{color.END}')

def readfile(fl):
	debug(f'reading file: {fl}')
	try:
		with open(fl) as f:
			return f.read().splitlines()
			f.close()
	except FileNotFoundError:
		logging.error(f'no such file or directory: {arg["<queryfile>"]}\n')
		sys.exit(2)

def lastposf(mongocollection, query):
	try:
		return get_lastpos(mongocollection, query)
	except twitter.error.NoLastPositionData:
		return init_lastpos(mongocollection, query)

def init_lastpos(mongocollection, query):
	debug(f'initializing last pos value for {query}')
	date = '2000-01-01 00:00:00'
	# date = '2020-11-02 15:00:00' #TODO#p: dd
	return set_lastpos(mongocollection, query, date)

def set_lastpos(mongocollection, query, date):
	debug(f'setting last pos value for {query} to {date}')
	a = { "_id": query }
	b = { "_id": query, "lastpos": date }
	# try:
	server_result = mongocollection.replace_one(a, b, True)
	if server_result.raw_result['ok'] == 1.0:
		debug(f'replace_one() server result: {server_result}')
		return date
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

def mongo_save(db, document, query):
	# info(f'saving: {document}')
	if not includes(query, document['tweet']): return
	try: db.tweets.insert_one(document)
	except pymongo.errors.DuplicateKeyError: pass
	else: # not a duplicate
		print(f'{document[capture_delay_sec]:4.4f}',
			query, document["tweet"], sep='\t')

def includes(x, y):
	info(f'checking whether or not {y} includes {x}')
	if x.lower() in wo_mentions(y.lower()):
		info(f'YES, `{y}` includes `{x}`.')
		return True
	else:
		warn(f"NO, `{y}` does not include `{x}`")
		return False
	# # FIXME: normalize('YEŞİL') -> ['#yefil', '#yefll', '#yesil', '#yesll']
	# if x.lower() in y.lower(): return True
	# # elif x.lower() in normalize(y, prioritize_alpha=True)[0]: return True
	# else: return False

wo_mentions = lambda t: " ".join(filter(lambda x: x[0]!='@', t.split()))

