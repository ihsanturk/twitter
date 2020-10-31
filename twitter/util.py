import sys
import logging
import pymongo

debug = logging.debug
# yellerr = lambda msg: sys.stderr.write(sys.argv[0]+': '+str(msg))

def readfile(fl):
	debug(f'reading file: {fl}')
	try:
		with open(fl) as f:
			return f.read().splitlines()
			f.close()
	except FileNotFoundError:
		logging.error(f'no such file or directory: {arg["<queryfile>"]}\n')
		sys.exit(2)

# mongo -----------------------------------------------------------------------
def init_lastpos(coll, query):
	debug(f'initializing last pos value for {query}')
	date = '2000-01-01 00:00:00'
	date = '2020-10-27 21:00:00' #TODO#p: dd
	return set_lastpos(coll, query, date)

def set_lastpos(coll, query, date):
	#TODO#0: store date as python date object.
	debug(f'setting last pos value for {query} to {date}')
	try:
		lastpos = coll.insert_one({ "_id": query, 'lastpos': date }, upsert=True)
		return date
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)

def get_lastpos(coll, query):
	#TODO#0: convert from date object to string.
	debug(f'getting last pos value for {query}')
	try:
		date = coll.find_one({"_id": query}, { 'lastpos': 1, '_id': 0 })
		return date
	except pymongo.errors.ServerSelectionTimeoutError:
		logging.critical(f'could not connected to mongodb')
		sys.exit(2)

def mongo_save(coll, data):
	coll.insert_one(data)

# # redis ---------------------------------------------------------------------
# def set_lastpos(redis_client, query, date):
# 	debug('setting last pos value', date)
# 	lastpos = redis_client.set('lastpos:'+query, date)
# 	return date

# def get_lastpos(redis_client, query):
# 	#TODO#p: handle errors
# 	debug('getting last pos value for ', query)
# 	lastpos = redis_client.get('lastpos:'+query).decode("utf-8")
# 	return lastpos

# def init_lastpos(redis_client, query):
# 	debug('initializing last pos value for', query)
# 	p = '2000-01-01 00:00:00'
# 	p = '2020-10-27 21:00:00' #TODO#p: dd
# 	lastpos = redis_client.set('lastpos:'+query, p)
# 	return p

# def redis_save(query, value, lastpos):
# 	print('redis_save: unimplemented')

