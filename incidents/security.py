import hashlib
from .models import Users
import secrets

""" the hash function was changed so remember to apply the necessay changes to all the parts of the code 
the reference/call it """
def hash_password(salt, password):
    return hashlib.sha384((salt.encode() + password.encode())).hexdigest()

def hash_phrase(phrase):
	return hashlib.sha384(phrase.encode()).hexdigest()


# SESSION_KEY= secrets.token_urlsafe()
SESSION_KEY = 'BWT0VYLt2MphwFr81JpDtCnm19sL3DamV9JPyYThqkQ'
def authenticated(username, password):
	try:
		user_object= Users.objects.get(user_name=username)
		authenticate_username=user_object.user_name
		authenticate_password=user_object.user_pass
		produce_hash=hash_password(authenticate_username, password)
		if authenticate_password == produce_hash:
			return True
		else:
			return f"The password you entered does not match the login"
	except Exception as e:
		return f"User does not exist"





