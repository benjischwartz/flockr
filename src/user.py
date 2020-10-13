from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token
import re

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
def check(email):
    if(re.search(regex,email)):
        return("Valid Email")
    else:
        return("Invalid Email")

def user_profile(token, u_id):
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    #Error Checking: Raise an Input Error if Names not Between 1 & 50 Characters
    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError("First Name is not Between 1 and 50 Characters")
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError("Last Name is not Between 1 and 50 Characters")

    #Error Checking: Raise an AccessError if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
    if token not in users:
        raise AccessError("Token passed is not valid.")

    #prev_name = users[token_u_id]['name_first']
    
    users[token]['name_first'] = name_first
    users[token]['name_last'] = name_last

    return {
    }

def user_profile_setemail(token, email):
    #Error Checking: Raise an InputError if the email is invalid
    if (check(email) != "Valid Email"):
        raise InputError ("Invalid email")

    #Error Checking: Raise an AccessError if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
    if token not in users:
        raise AccessError("Token passed is not valid.")

    #Error Checking: Raise an InputError if email is already used
    if email in users:
        raise InputError("Email is already used.")

    users[token] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }