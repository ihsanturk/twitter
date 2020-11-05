import sys
import logging
import pymongo
import twitter.error

debug = logging.debug

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
	date = '2020-11-02 15:00:00' #TODO#p: dd
	return set_lastpos(mongocollection, query, date)

def set_lastpos(mongocollection, query, date):
	#TODO#1: store date as python date object.
	debug(f'setting last pos value for {query} to {date}')
	d = { "_id": query, "lastpos": date }
	# try:
	server_result = mongocollection.replace_one(d, d, True)
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
	#TODO#1: convert from date object to string.
	debug(f'getting last pos value for {query}')
	try:
		result = mongocollection.find_one({"_id": query}, {'lastpos': 1, '_id': 0})
		if not result: raise twitter.error.NoLastPositionData(query)
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)
	date = result['lastpos']
	debug(f'last pos value for {query} is {date}')
	return date

def mongo_save(db, document, query):
	debug(f'saving: {document}')
	try:
		db.tweets.insert_one(document)
	except pymongo.errors.DuplicateKeyError:
		# logging.error('duplication')
		pass
	else: # not a duplicate
		db.info.update_one({"_id": query}, { '$push': { 'tweetids': document['_id'] } })
		print(document['link'])

