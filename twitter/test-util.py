import unittest
from twitter.util import *
from pymongo import MongoClient
from twitter.mongo_credentials import port, username, password, host

# NOTE: NOT TESTED: THIS FILE

class TestDbFunctions(unittest.TestCase):

	def setUp(self):
		self.c = "test-company"
		self.d = "2020-10-30 12:24:55"
		self.dbclient = MongoClient(f'mongodb://{host}:{port}')
		self.db = dbclient['twitter']

	def test_set_lastpos(self, )
		pass

	def test_init_lastpos(self, ):
		pass

	def test_get_lastpos(self, ):
		pass

	def tearDown(self):
		db.


if __name__ = '__main__':
	unittest.main()
