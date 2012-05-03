from GoldStarDAL.goldstar import *
import string
import random
import unittest
class testDatabaseFunctions(unittest.TestCase):

	def test_addgoodinput(self):
		fn = "Jay"
		ln = "Ostinowsky"
		em = "dukebdfan@comcast.net"
		self.assertEqual(addusertodatabase(fn, ln, em), True)

	def test_addbadinput(self):
		fn = "a"
		ln = "a"
		em = "a"
		for x in range(1,52):
			fn = fn + random.choice(string.ascii_letters + string.digits)
		for x in range(1,52):
			ln = ln + random.choice(string.ascii_letters + string.digits)
		for x in range(1,102):
			em = em + random.choice(string.ascii_letters + string.digits)
		self.assertEqual(addusertodatabase(fn, ln, em), False)

	def test_noinput(self):
		fn=""
		ln=""
		em=""
		success = addusertodatabase(fn,ln,em)

	def test_listofusers(self):
		listtheusers()
	def test_giveastarexists(self):
		issuerEmail = "dukebdfan@comcast.net"
		ownerEmail = "mgraham@problemsolutions.net"
		category = "INFLUENCED"
		description = "This is a test description"
		addusertodatabase("Matt", "Graham", ownerEmail)
		self.assertEqual(giveastar(issuerEmail, ownerEmail, category, description), True)


if __name__ == "__main__":
	unittest.main()