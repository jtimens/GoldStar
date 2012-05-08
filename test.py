import unittest
from app import *

class testdb(unittest.TestCase):
	def setUp(self):
		db.create_all()
		try:
			u = User()
			u.firstName=u"Walt"
			u.lastName=u"Grata"
			u.email=u"wegrata@gmail.com"
			u1 = User()
			u1.firstName=u"John"
			u1.lastName=u"Smith"
			u1.email=u"jsmith@gmail.com"
			u2 = User()
			u2.firstName = u"Jay"
			u2.lastName = u"Ostinowsky"
			u2.email = u"dukebdfan@comcast.net"
			u3 = User()
			u3.firstName=u"Walt"
			u3.lastName=u"Grata"
			u3.email=u"wegrata@gmail.com"
			db.session.add(u)
			db.session.add(u3)
			db.session.add(u1)
			db.session.add(u2)
			db.session.commit()
		except Exception as ex:
			print ex.message
	def tearDown(self):
		db.drop_all()
	def test_save_star(self):
		issuer = User.query.get(1)
		owner = User.query.get(2)
		s = Star()
		s.issuer_id = issuer.id
		s.owner_id = owner.id
		db.session.add(s)
		db.session.commit()
		issuer = User.query.get(1)
		owner = User.query.get(2)
		print issuer.issued
		print owner.stars
	def test_save_stars_more_than_one(self):
		A = User.query.get(1)
		B = User.query.get(2)
		C = User.query.get(3)
		s1 = Star()
		s1.category = u"INFLUENCED"
		s1.description = u"This is a test"
		s2 = Star()
		s2.category = u"HELPED"
		s2.description = u"THIS IS ANOTHER TEST"
		s1.issuer_id = A.id
		s1.owner_id = B.id
		s2.owner_id = A.id
		s2.issuer_id = C.id
		db.session.add(s1)
		db.session.add(s2)
		db.session.commit()
		A = User.query.get(1)
		B = User.query.get(2)
		C = User.query.get(3)
		print A.stars
		print C.issued
		print B.stars
		print A.issued
	def test_dupe_user(self):
		try:
			A = User.query.get(1)
			B = User.query.get(2)
			C = User.query.get(3)
			D = User.query.get(4)
			print A.firstName
			print B.firstName
			print C.firstName
			print D.firstName
		except Exception as ex:
			print ex.message




if __name__ == "__main__":
	unittest.main()