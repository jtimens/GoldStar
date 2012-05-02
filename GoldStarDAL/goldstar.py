from sqlalchemy import create_engine, Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
engine = create_engine('sqlite:///:memory:', echo = False)
Base = declarative_base()
class User(Base):
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
	stars = relationship("Star", order_by="Star.id", backref="user")

class Star(Base):
	__tablename__ = 'star'

	id = Column(Integer, primary_key = True)
	issueID = Column(Integer, ForeignKey(users.id))
	ownerID = Column(Integer, ForeignKey(users.id))
	user = relationship("User", backref=backref('star', order_by=id))


Base.metadata.create_all(engine)
def addusertodatabase(firstnamefromhtml, lastnamefromhtml, emailfromhtml):
	success = False
	if len(firstnamefromhtml) > 50 or len(lastnamefromhtml) > 50 or len(emailfromhtml) > 100:
		firstnamefromhtml = firstnamefromhtml[:50]
		lastnamefromhtml = lastnamefromhtml[:50]
		emailfromhtml = emailfromhtml[:100]
	if len(firstnamefromhtml) != 0 and lastnamefromhtml != 0 and emailfromhtml != 0:
		if firstnamefromhtml.isalpha() and lastnamefromhtml.isalpha():
			Session = sessionmaker(bind = engine)
			session = Session()
			newUser = User(firstnamefromhtml, lastnamefromhtml, emailfromhtml)
			session.add(newUser)
			session.commit()
			success = True
	return success
def listtheusers():
	Session = sessionmaker(bind = engine)
	session = Session()
	for instance in session.query(User).order_by(User.firstName):
		print instance.firstName