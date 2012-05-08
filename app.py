from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask.ext.restless import APIManager
import datetime

# Create the app for Flask
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sql'
db = SQLAlchemy(app)

# User Table Exception and Validation handling
class userValidation(Exception):
	pass

# Star Table Exception and Validation handling
class starValidation(Exception):
	pass


class Star(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Unicode(120))
	category = db.Column(db.Unicode(100))
	created = db.Column(db.DateTime, default = datetime.datetime.now())
	issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issuer = db.relationship("User", backref="issued", primaryjoin='Star.issuer_id==User.id')
	owner = db.relationship("User", backref="stars", primaryjoin="Star.owner_id==User.id")

	#Validation defs which validate 1 parameter of the table at a time

	#Validates the Description
	@validates('description')
	def validate_description(self, key, string):
		e = ""
		if len(string) > 120:
			e = "Description Length is too long"
		if len(e) > 0:
			exception = starValidation();
			exception.errors = dict(description = e)
			return exception
		return string

	#Validates the Category
	@validates('category')
	def validate_category(self, key, string):
		e = ""
		if len(string) > 100:
			e = "Category Length is too long"
		if len(e) > 0:
			exception = starValidation()
			exception.errors = dict(category = e)
			return exception
		return string

	#Validates the owner ID
	@validates('owner_id')
	def validate_owner_id(self, key, string):
		e=""
		string = str(string)
		if not string.isdigit():
			e = "Digits are only allowed for the ID"
			exception = starValidation()
			exception.errors = dict(owner_id = e)
			return exception
		return int(string)

	#Validates the issuer ID
	@validates('issuer_id')
	def validate_issuer_id(self, key, string):
		e=""
		string = str(string)
		if not string.isdigit():
			e = "Digits are only allowed for the ID"
			exception = starValidation()
			exception.errors = dict(issuer_id = e)
			return exception
		return int(string)

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	firstName = db.Column(db.Unicode(50), nullable = False)
	lastName = db.Column(db.Unicode(50), nullable = False)
	email = db.Column(db.Unicode(100), nullable = False)
	
	#Validation defs which validate 1 parameter of the table at a time

	#Validates the First Name
	@validates('firstName')
	def validate_firstName(self, key, string):
		if string.isalpha() == False:
			exception = userValidation()
			exception.errors = dict(firstName = 'Invalid First Name')
			raise exception
		return string

	#Validates the Last Name
	@validates('lastName')
	def validate_lastName(self, key, string):
		if string.isalpha() == False:
			exception = userValidation()
			exception.errors = dict(lastName = 'Invalid Last Name')
			raise exception
		return string

	#Validates the Email
	@validates('email')
	def validate_email(self, key, string):
		e = ""
		if not "@" in string:
			e = u"Invalid Email"
		elif len(string) == 0:
			e = u"No Email Entered"
		elif User.query.filter_by(email = unicode(string)).count() > 0:
			e = u"User already exists"
		if len(e) != 0:
			exception = userValidation()
			exception.errors = dict(email = e)
			raise exception
		return string

def main():
	#The main index of the Gold Star App
	@app.route('/')
	def index_route():
		return render_template('index.html')

	#Displays the entire Gold Star App
	@app.route('/main.html')
	def main_route():
		return render_template('main.html')

	#Redirect which has a lot of server requests
	@app.route('/results.html')
	def result_route():
		return render_template('results.html')

	#Initialize the Database
	db.create_all()

	#Creates an API manager
	manager = APIManager(app, flask_sqlalchemy_db=db)

	#Creates the API
	manager.create_api(User, methods=['GET', 'POST'], validation_exceptions=[userValidation])
	manager.create_api(Star, methods=['GET', 'POST'], validation_exceptions=[starValidation])
<<<<<<< HEAD




	#Start the flask loop
	app.run('0.0.0.0')

if __name__ == "__main__":
	main()
=======
>>>>>>> 538f307bd9c0abc7c4158c37e133533f3ec241a5
