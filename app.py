from flask import Flask, render_template
import flask.ext.sqlalchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
import flask.ext.restless
import datetime

# Create the app for Flask
app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zoubpmfsdtxwoq:3G0ELHUf2BcAOSF1hUxDceKsQL@ec2-23-23-234-187.compute-1.amazonaws.com/resource44881'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite'
db = flask.ext.sqlalchemy.SQLAlchemy(app)

# User Table Exception and Validation handling
class userValidation(Exception):
	pass

# Star Table Exception and Validation handling
class starValidation(Exception):
	pass


#Star Table that stores Star information between two users
class Star(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Unicode)
	category = db.Column(db.Unicode)
	created = db.Column(db.DateTime, default = datetime.datetime.now())
	issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	hashtag = db.Column(db.Unicode)
	issuer = db.relationship("User", backref="issued", primaryjoin='Star.issuer_id==User.id')
	owner = db.relationship("User", backref="stars", primaryjoin="Star.owner_id==User.id")
	#Validation defs which validate 1 parameter of the table at a time

	#Validates the Description
	@validates('description')
	def validate_description(self, key, string):
		e = ""
		string = string.strip()
		if len(string) > 120:
			e = "Description Length is too long"
		if len(e) > 0:
			exception = starValidation();
			exception.errors = dict(description = e)
			raise exception
		return unicode(string)

	#Validates the Category
	@validates('category')
	def validate_category(self, key, string):
		e = ""
		string = string.strip()
		if len(string) > 100:
			e = "Category Length is too long"
		if len(e) > 0:
			exception = starValidation()
			exception.errors = dict(category = e)
			raise exception
		return unicode(string)

	#Validates the owner ID
	@validates('owner_id')
	def validate_owner_id(self, key, string):
		e=""
		string = str(string)
		if not string.isdigit():
			e = "Digits are only allowed for the ID"
		if str(self.issuer_id) == string:
			e = "Can't give yourself a star"
		if len(e):
			exception = starValidation()
			exception.errors = dict(owner_id = e)
			raise exception
		return int(string)

	#Validates the issuer ID
	@validates('issuer_id')
	def validate_issuer_id(self, key, string):
		e=""
		string = str(string)
		if not string.isdigit():
			e = "Digits are only allowed for the ID"
		if len(e):
			exception = starValidation()
			exception.errors = dict(issuer_id = e)
			raise exception
		return int(string)

#User Table which stores user information and links to stars
class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)


	password = db.Column(db.Unicode)

	firstName = db.Column(db.Unicode)#, nullable = False)
	lastName = db.Column(db.Unicode)#, nullable = False)
	email = db.Column((db.Unicode), unique=True)#, nullable = False)
	
	#Validation defs which validate 1 parameter of the table at a time

	#Validates the First Name
	@validates('firstName')
	def validate_firstName(self, key, string):
		string = string.strip()
		if not string.isalpha() or not len(string):
			exception = userValidation()
			exception.errors = dict(firstName = 'Invalid First Name')
			raise exception
		return unicode(string)

	#Validates the Last Name
	@validates('lastName')
	def validate_lastName(self, key, string):
		string = string.strip()
		if not string.isalpha() or not len(string):
			exception = userValidation()
			exception.errors = dict(lastName = 'Invalid Last Name')
			raise exception
		return unicode(string)

	#Validates the Email
	@validates('email')
	def validate_email(self, key, string):
		e = ""
		string = string.strip()
		if not "@" in string:
			e = u"There is no @ in the email"
		if not "." in string:
			e = u"There is no . in the email"
		elif len(string) == 0:
			e = u"No Email Entered"
		elif User.query.filter_by(email = unicode(string)).count() > 0:
			e = u"Email is already being used"
		if len(e) != 0:
			exception = userValidation()
			exception.errors = dict(email = e)
			raise exception
		return unicode(string)


#The main index of the Gold Star App
@app.route('/')
@app.route('/index.html')
def index_route():
	return render_template('index.html')

#Displays the entire Gold Star App
@app.route('/main.html')
def main_route():
	return render_template('main.html')
	
@app.route('/mobileview.html')
def mobileview_route():
	return render_template('mobileview.html')

#Redirect which has a lot of server requests
@app.route('/results.html')
def result_route():
	return render_template('results.html')


#Initialize the Database
db.create_all()

#Flask Login Information
@app.route('/login', methods = ['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username, password = form.username.data, form.password.data
		username = username.lower()
		user = User.query.filter_by(email = username).one()
		if bcrypt.hashpw(password, user.password) == user.password:
			login_user(user)
			print "Logged In successfully"
			return render_template("main.html", loginID = user.id)
	return render_template("login.html", form=form)


#Creates an API manager
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

#Creates the API
manager.create_api(User, methods=['GET', 'POST'], validation_exceptions=[userValidation])
manager.create_api(Star, methods=['GET', 'POST'], validation_exceptions=[starValidation])

#manager.create_api(User, methods=['GET', 'POST'])
#manager.create_api(Star, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':
	app.run('0.0.0.0')


