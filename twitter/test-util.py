import unittest
from twitter.util import *
from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

unittest.TestLoader.sortTestMethodsUsing = None

class TestDbFunctions(unittest.TestCase):

	def setUp(s):
		s.c = "test-company"
		s.dbname = 'test-twitter'
		s.dbclient = MongoClient(f'mongodb://{host}:{port}')
		s.db = s.dbclient[s.dbname]

	def test_init_lastpos(s):
		date = datetime(2000, 1, 1, 0, 0, 0)
		# date = '2020-11-02 15:00:00' #TODO#p: dd
		s.assertEqual(init_lastpos(s.db.tweets, s.c), date)

	def test_set_get_lastpos(s):
		set_lastpos(s.db['info'], s.c, datetime(2020, 11, 2, 20, 0, 57))
		s.assertEqual(get_lastpos(s.db['info'], s.c), datetime(2020, 11, 2, 20, 0, 57))

	def tearDown(s):
		s.dbclient.drop_database('test-twitter')


if __name__ == '__main__':
	unittest.main()
