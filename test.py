import unittest
import os
import json
import requests
from app import *

class testdb(unittest.TestCase):

	def setUp(self):
		os.remove('tmp/test.db')
		db.create_all()



	def testAddUsersToDatabase(self):
		newUser = {"firstName": "Jay", "lastName":"Ostinowsky", "email":"dukebdfan@comcast.net"}
		r = requests.post('/api/user', data=json.dumps(newUser), headers={'content-type': 'application/json'})


if __name__ == "__main__":
	unittest.main()