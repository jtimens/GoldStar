from elixir import *

metadata.bind = 'sqlite:///:memory:'

class Star(Entity):

	id = Field(Integer, primary_key=True)
	description = Field(Unicode(120))
	category = Field(Unicode(100))
	issuer = ManyToOne('User', inverse='issued')
	owner = ManyToOne('User', inverse='owned')

class User(Entity):

	id = Field(Integer, primary_key = True)
	firstName = Field(Unicode(50))
	lastName = Field(Unicode(50))
	email = Field(Unicode(100))
	owned = OneToMany('Star', inverse='issuer')
	issued = OneToMany('Star', inverse='owner')
	def __init__(self, firstname, lastname, email):
		self.firstName = firstname
		self.lastName = lastname
		self.email = email
	def __repr__(self):
		return "<User('%s', '%s' , '%s')>" % (self.firstName, self.lastName, self.email)
	
setup_all(True)
def addusertodatabase(firstnamefromhtml, lastnamefromhtml, emailfromhtml):
	success = False
	if len(firstnamefromhtml) > 50 or len(lastnamefromhtml) > 50 or len(emailfromhtml) > 100:
		firstnamefromhtml = firstnamefromhtml[:50]
		lastnamefromhtml = lastnamefromhtml[:50]
		emailfromhtml = emailfromhtml[:100]
	if len(firstnamefromhtml) != 0 and lastnamefromhtml != 0 and emailfromhtml != 0:
		if firstnamefromhtml.isalpha() and lastnamefromhtml.isalpha():
			newUser = User(firstnamefromhtml, lastnamefromhtml, emailfromhtml)
			session.commit()
			success = True
	return success

def listtheusers():
	for instance in session.query(User).order_by(User.firstName):
		print instance.email
		print instance.stars
		print instance.issued
def giveastar(issuerEmail, ownerEmail, category, description):
	#print dir(session)
	#update().where(User.firstName == "Jay").values(firstName = "Jonathan")
	issuerObj = session.query(User).filter_by(email = issuerEmail).one()
	ownerObj = session.query(User).filter_by(email = ownerEmail).one()
	newStar = Star()
	newStar.category = category
	newStar.description = description
	newStar.issuer_id = issuerObj.id
	newStar.owner_id = ownerObj.id
	ownerObj.stars.append(newStar)
	session.commit()
	return True