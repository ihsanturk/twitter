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

# redis -------------------------------------------------------------------
def set_lastpos(redis_client, query, date):
	debug('setting last pos value', date)
	lastpos = redis_client.set('lastpos:'+query, date)
	return date

def get_lastpos(redis_client, query):
	#TODO#p: handle errors
	debug('getting last pos value for ', query)
	lastpos = redis_client.get('lastpos:'+query).decode("utf-8")
	return lastpos

def init_lastpos(redis_client, query):
	debug('initializing last pos value for', query)
	p = '2000-01-01 00:00:00'
	p = '2020-10-27 21:00:00' #TODO#p: dd
	lastpos = redis_client.set('lastpos:'+query, p)
	return p

def redis_save(query, value, lastpos):
	print('redis_save: unimplemented')

