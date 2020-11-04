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

# mongo ---------------------------------------------------------------------
def init_lastpos(mongocollection, query):
	debug(f'initializing last pos value for {query}')
	date = '2000-01-01 00:00:00'
	date = '2020-11-02 15:00:00' #TODO#p: dd
	return set_lastpos(mongocollection, query, date)

def set_lastpos(mongocollection, query, date):
	#TODO#0: store date as python date object.
	debug(f'setting last pos value for {query} to {date}')
	d = { "_id": query, "lastpos": date }
	# try:
	if mongocollection.replace_one(d, d, True).raw_result['ok'] == 1.0:
		return date
	else:
		raise Exception() # TODO#2: dd
		# raise CannotSetLastPos(mongocollection, query, date) TODO#2: add this to twitter/error.py
	# except pymongo.errors.ServerSelectionTimeoutError:
	# 	logging.critical(f'could not connected to mongodb')
		# sys.exit(2)

def get_lastpos(mongocollection, query):
	#TODO#0: convert from date object to string.
	debug(f'getting last pos value for {query}')
	try:
		date = mongocollection.find_one({"_id": query}, {'lastpos': 1, '_id':
			0})['lastpos']
		if not date: raise twitter.error.NoLastPositionData(query)
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)
	return date

def mongo_save(mongocollection, document):
	print(document['datetime'])
	# mongocollection.(document)

