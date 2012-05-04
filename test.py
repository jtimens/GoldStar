import unittest
import os
from app import *

class testdb(unittest.TestCase):

	def setUp(self):
		os.remove('tmp/test.db')
		db.create_all()



	def testAddUsersToDatabase(self):
		A = User()
		A.firstName = u"Jay"
		A.lastName = u"Ostinowsky"
		A.email = u"dukebdfan@comcast.net"
		B = User()
		B.firstName = u"Matt"
		B.lastName = u"Graham"
		B.email = u"mgraham@problemsolutions.net"
		db.session.add(B)
		db.session.add(A)
		db.session.commit()




if __name__ == "__main__":
	unittest.main()