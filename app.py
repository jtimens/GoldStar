from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have an id column of type Integer.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).

class Star(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Unicode(120))
	category = db.Column(db.Unicode(100))
	issuer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	issuer = db.relationship("User", backref="issued",primaryjoin='Star.issuer_id==User.id')
	owner = db.relationship("User", backref="stars", primaryjoin="Star.owner_id==User.id")

class User(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	firstName = db.Column(db.Unicode(50))
	lastName = db.Column(db.Unicode(50))
	email = db.Column(db.Unicode(100))
	def __init__(self, firstname, lastname, email):
		self.firstName = firstname
		self.lastName = lastname
		self.email = email
	def __repr__(self):
		return "<User('%s', '%s' , '%s')>" % (self.firstName, self.lastName, self.email)


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Star, methods=['GET', 'POST', 'DELETE'])

# start the flask loop
app.run()