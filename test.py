import unittest
from app import *

class testdb(unittest.TestCase):
	def setUp(self):
		db.create_all()
	def tearDown(self):
		db.drop_all()
	def test_add_user(self):
		u = User()
		u.firstName=u"Walt"
		u.lastName=u"Grata"
		u.email=u"wegrata@gmail.com"
		u1 = User()
		u1.firstName=u"John"
		u1.lastName=u"Smith"
		u1.email=u"jsmith@gmail.com"
		db.session.add(u)
		db.session.add(u1)
		db.session.commit()
	def test_save_star(self):
		u = User()
		u.firstName=u"Walt"
		u.lastName=u"Grata"
		u.email=u"wegrata@gmail.com"
		u1 = User()
		u1.firstName=u"John"
		u1.lastName=u"Smith"
		u1.email=u"jsmith@gmail.com"
		db.session.add(u)
		db.session.add(u1)
		db.session.commit()
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




if __name__ == "__main__":
	unittest.main()