from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask.ext.restless import APIManager
import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
db = SQLAlchemy(app)

class userValidation(Exception):
	pass

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

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	firstName = db.Column(db.Unicode(50), nullable = False)
	lastName = db.Column(db.Unicode(50), nullable = False)
	email = db.Column(db.Unicode(100), nullable = False)
	
	@validates('firstName')
	def validate_firstName(self, key, string):
		if string.isalpha() == False:
			exception = userValidation()
			exception.errors = dict(firstName = 'Invalid First Name')
			raise exception
		return string
		
	@validates('lastName')
	def validate_lastName(self, key, string):
		if string.isalpha() == False:
			exception = userValidation()
			exception.errors = dict(lastName = 'Invalid Last Name')
			raise exception
		return string

	@validates('email')
	def validate_email(self, key, string):
		e = u""
		if not "@" in string:
			e = u"Invalid Email"
		if len(string) == 0:
			e = u"No Email Entered"
		if User.query.filter_by(email = string).count() > 0:
			e = u"User already exists"
		if len(e) != 0:
			exception = userValidation()
			exception.errors = dict(email = e)
			raise exception
		return string

def main():
	@app.route('/')
	def index_route():
		return render_template('index.html')

	@app.route('/main.html')
	def main_route():
		return render_template('main.html')

	@app.route('/results.html')
	def result_route():
		return render_template('results.html')

	db.create_all()


	manager = APIManager(app, flask_sqlalchemy_db=db)


	manager.create_api(User, methods=['GET', 'POST'], validation_exceptions=[userValidation])
	manager.create_api(Star, methods=['GET', 'POST'], validation_exceptions=[starValidation])




	# start the flask loop
	app.run('0.0.0.0')

if __name__ == "__main__":
	main()
