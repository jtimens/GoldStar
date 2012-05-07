import string
from sqlalchemy.orm import validates
User_Error = {'firstName':'Invalid firstName', 
				'lastName':'Invalid lastName',
				'email':'Invalid email'}

def userValidation(Exception):
	if firstName.isalpha() == False:
		return User_Error['firstName']

def starValidation(Exception):
	return