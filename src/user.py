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
    validid = 0
    selected_data = {}
    selected_email = ' '
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")

    for tokens, data in users.items():
        if data['u_id'] == u_id:
            validid = 1
            selected_data = data
            selected_email = tokens

    if validid == 0:
        raise InputError("Invalid ID.")
    else:
        selected_data.pop('password')
        selected_data.pop('permission_id')
        selected_data['email'] = selected_email

    return selected_data

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

    #Error Checking: Raise an InputError if email is already used
    if email in users:
        raise InputError("Email is already used.")

    users[email] = users.pop(token)

    return {
    }

def user_profile_sethandle(token, handle_str):
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")

    if ((len(handle_str) < 3) or (len(handle_str) > 20)):
        raise InputError("handle has to be in between 3 and 20 letters inclusive.")
    
    #for tokens, data in users.items():

    for email in users:
        if users[email]['handle'] == handle_str:
            raise InputError("handle is already being used by another user.")

    users[token]['handle'] = handle_str
    
    return {
    }
    