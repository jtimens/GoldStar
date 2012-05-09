import unittest
from app import *

class testdb(unittest.TestCase):
	def setUp(self):
		db.create_all()
		user1 = User(firstName = u"UserA", lastName = u"UserA", email = u"UserA@gmail.com")
		user2 = User(firstName = u"UserB", lastName = u"UserB", email = u"UserB@gmail.com")
		user3 = User(firstName = u"UserC", lastName = u"UserC", email = u"UserC@gmail.com")
		user4 = User(firstName = u"UserD", lastName = u"UserD", email = u"UserD@gmail.com")
		user5 = User(firstName = u"UserE", lastName = u"UserE", email = u"UserE@gmail.com")
		user6 = User(firstName = u"UserF", lastName = u"UserF", email = u"UserF@gmail.com")
		user7 = User(firstName = u"UserG", lastName = u"UserG", email = u"UserG@gmail.com")
		user8 = User(firstName = u"UserH", lastName = u"UserH", email = u"UserH@gmail.com")
		user9 = User(firstName = u"UserI", lastName = u"UserI", email = u"UserI@gmail.com")
		user10 = User(firstName = u"UserJ", lastName = u"UserJ", email = u"UserJ@gmail.com")
		user11 = User(firstName = u"UserK", lastName = u"UserK", email = u"UserK@gmail.com")
		user12 = User(firstName = u"UserL", lastName = u"UserL", email = u"UserL@gmail.com")
		user13 = User(firstName = u"UserM", lastName = u"UserM", email = u"UserM@gmail.com")
		user14 = User(firstName = u"UserN", lastName = u"UserN", email = u"UserN@gmail.com")
		user15 = User(firstName = u"UserO", lastName = u"UserO", email = u"UserO@gmail.com")
		user16 = User(firstName = u"UserP", lastName = u"UserP", email = u"UserP@gmail.com")
		user17 = User(firstName = u"UserQ", lastName = u"UserQ", email = u"UserQ@gmail.com")
		user18 = User(firstName = u"UserR", lastName = u"UserR", email = u"UserR@gmail.com")
		user19 = User(firstName = u"UserS", lastName = u"UserS", email = u"UserS@gmail.com")
		user20 = User(firstName = u"UserT", lastName = u"UserT", email = u"UserT@gmail.com")
		db.session.add(user1)
		db.session.add(user2)
		db.session.add(user3)
		db.session.add(user4)
		db.session.add(user5)
		db.session.add(user6)
		db.session.add(user7)
		db.session.add(user8)
		db.session.add(user9)
		db.session.add(user10)
		db.session.add(user11)
		db.session.add(user12)
		db.session.add(user13)
		db.session.add(user14)
		db.session.add(user15)
		db.session.add(user16)
		db.session.add(user17)
		db.session.add(user18)
		db.session.add(user19)
		db.session.add(user20)
		db.session.commit()
	def tearDown(self):
		db.drop_all()
	def test_add_multiple_stars(self):
		s = Star(description = u"This is a star from 1 to 20", category = u"INFLUENCED", issuer_id = "1", owner_id = "20")
		db.session.add(s)
		db.session.commit()
		user1 = User.query.filter_by(email = u"UserA@gmail.com").one()
		user20 = User.query.filter_by(email = u"UserT@gmail.com").one()
		print user1.issued
		print user20.stars
		s1 = Star(description = u"This is a star from 2 to 20", category = u"INFLUENCED", issuer_id = "2", owner_id = "20")
		db.session.add(s1)
		db.session.commit()
		user2 = User.query.filter_by(email = u"UserB@gmail.com").one()
		user20 = User.query.filter_by(email = u"UserT@gmail.com").one()
		print user2.issued
		print user20.stars





if __name__ == "__main__":
	unittest.main()