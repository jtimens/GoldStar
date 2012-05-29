from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flaskext.oauth import OAuth
import flask.ext.sqlalchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
import flask.ext.restless
import datetime

# Create the app for Flask
app = Flask(__name__)
app.config['DEBUG'] = True
SECRET_KEY = 'development key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zoubpmfsdtxwoq:3G0ELHUf2BcAOSF1hUxDceKsQL@ec2-23-23-234-187.compute-1.amazonaws.com/resource44881'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.sqlite'
db = flask.ext.sqlalchemy.SQLAlchemy(app)
TWITTER_APP_ID = '8YsjtlJjL8kRaGDv1SZjmQ'
TWITTER_APP_SECRET_ID = 'QVAWDUstIpIHWhZegr5CqQm1XJHWtBIzOacQdXzP7o'

app.secret_key = SECRET_KEY
oauth = OAuth()

twitter = oauth.remote_app('twitter',
	base_url = 'http://api.twitter.com/1/',
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	#authorize_url = 'https://api.twitter.com/oauth/authorize',
	authorize_url='http://api.twitter.com/oauth/authenticate',
	consumer_key = TWITTER_APP_ID,
	consumer_secret = TWITTER_APP_SECRET_ID
	)

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
	firstName = db.Column(db.Unicode)#, nullable = False)
	lastName = db.Column(db.Unicode)#, nullable = False)
	email = db.Column((db.Unicode), unique=True)#, nullable = False)
	twitterUser = db.Column(db.Unicode)
	oauth_token = db.Column(db.Unicode)
	oauth_secret = db.Column(db.Unicode)
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

#Twitter Auth
@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.get(session['user_id'])

@app.after_request
def after_request(response):
	db.session.remove()
	return response

@twitter.tokengetter
def get_twitter_token():
	user = g.user
	if user is not None:
		return user.oauth_token, user.oauth_secret

@app.route('/login')
def login():
	return twitter.authorize(callback=url_for('oauth_authorized', 
		next = request.args.get('next') or request.referrer or None))

@app.route('/oauth_authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
	if resp is None:
		flash(u'You denied the request to sign in.')
	if resp is not None:
		user = User.query.filter_by(twitterUser=resp['screen_name']).first()
		if user is None:
			user = User()
			user.twitterUser = unicode(resp['screen_name'])
			db.session.add(user)
		user.firstName = u'Jay'
		user.lastName = u'Ostinowsky'
		user.email = u'Dukebdfan@comcast.net'	
		user.oauth_token = unicode(resp['oauth_token'])
		user.oauth_secret = unicode(resp['oauth_token_secret'])
		db.session.commit()
		session['user_id'] = user.id
		print resp['screen_name']
	return redirect('/index.html')

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

@app.route('/tweet', methods = ['POST'])
def tweet():
	if g.user is None:
		return redirect('/login')
	status = u'@juggler2009 test tag testing 1 2'
	resp = twitter.post('statuses/update.json', data = {'status': status})
	return redirect('/index.html')

#Initialize the Database
db.create_all()

#Creates an API manager
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

#Creates the API
manager.create_api(User, methods=['GET', 'POST'], validation_exceptions=[userValidation])
manager.create_api(Star, methods=['GET', 'POST'], validation_exceptions=[starValidation])
#manager.create_api(User, methods=['GET', 'POST'])
#manager.create_api(Star, methods=['GET', 'POST', 'DELETE'])

if __name__ == '__main__':
	app.run('0.0.0.0')


