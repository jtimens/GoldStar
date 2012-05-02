from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
userEngine = create_engine('sqlite:///:memory:', echo = False)
userBase = declarative_base()
starBase = declarative_base()
class User(userBase):
	__tablename__ = 'users'

	id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
	firstName = Column(String(50))
	lastName = Column(String(50))
	email = Column(String(100))

	def __init__(self, firstname, lastname, email):
		self.firstName = firstname
		self.lastName = lastname
		self.email = email
	def __repr__(self):
		return "<User('%s', '%s' , '%s')>" % (self.firstName, self.lastName, self.email)

class Star(starBase):
	__tablename__ = 'star'

	id = Column(Integer, Sequence('star_id_seq'), primary_key = True)
	

userBase.metadata.create_all(userEngine)
def addusertodatabase(firstnamefromhtml, lastnamefromhtml, emailfromhtml):
	success = False
	if len(firstnamefromhtml) > 50 or len(lastnamefromhtml) > 50 or len(emailfromhtml) > 100:
		firstnamefromhtml = firstnamefromhtml[:50]
		lastnamefromhtml = lastnamefromhtml[:50]
		emailfromhtml = emailfromhtml[:100]
	if len(firstnamefromhtml) != 0 and lastnamefromhtml != 0 and emailfromhtml != 0:
		if firstnamefromhtml.isalpha() and lastnamefromhtml.isalpha():
			Session = sessionmaker(bind = userEngine)
			session = Session()
			newUser = User(firstnamefromhtml, lastnamefromhtml, emailfromhtml)
			session.add(newUser)
			session.commit()
			success = True
	return success
def listtheusers():
	Session = sessionmaker(bind = userEngine)
	session = Session()
	for instance in session.query(User).order_by(User.firstName):
		print instance.firstName