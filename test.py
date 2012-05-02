from GoldStarDAL.goldstar import *
import string
import random
import unittest
class testDatabaseFunctions(unittest.TestCase):
	def test_addgoodinput(self):
		fn = "a"
		ln = "a"
		em = "a"
		print "GOOD INPUT"
		for x in range(1,50):
			fn = fn + random.choice(string.ascii_letters)
		for x in range(1,50):
			ln = ln + random.choice(string.ascii_letters)
		for x in range(1,100):
			em = em + random.choice(string.ascii_letters)
		success = addusertodatabase(fn,ln,em)
		print success
	def test_addbadinput(self):
		fn = "a"
		ln = "a"
		em = "a"
		print "BAD INPUT"
		for x in range(1,52):
			fn = fn + random.choice(string.ascii_letters + string.digits)
		for x in range(1,52):
			ln = ln + random.choice(string.ascii_letters + string.digits)
		for x in range(1,102):
			em = em + random.choice(string.ascii_letters + string.digits)
		success = addusertodatabase(fn,ln,em)
		print success
	def test_noinput(self):
		print "NO INPUT"
		fn=""
		ln=""
		em=""
		success = addusertodatabase(fn,ln,em)
		print success
	def test_listofusers(self):
		listtheusers()


if __name__ == "__main__":
	unittest.main()