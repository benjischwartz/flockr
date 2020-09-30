from data import users, tokens
import re
from error import InputError

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
def check(email):
    if(re.search(regex,email)):
        return("Valid Email")
    else:
        return("Invalid Email")

    
def auth_login(email, password):
    # check if email is registered
    login = False
    for emails in users.keys():
        if email == emails:            
            if users[email]['password'] == password:
                #validate token
                tokens.append(email)
                return {
                    'u_id': users[email]['u_id'],
                    'token': email, ## for iteration 1, tokens can just be email or id
                }
    raise InputError ("Email not found or password not valid")
    

def auth_logout(token):
    for valid_token in tokens:
        if token == valid_token:
            # remove from tokens dict
            tokens.remove(token)
            return {
                'is_success': True,
            }

    # not a valid token
    return {
        'is_success': False,
    }

def auth_register(email, password, name_first, name_last):
    
    # Check if valid email
    if (check(email) != "Valid Email"):
        raise InputError ("Invalid email")

    # Check if email already registered to a user
    else:
        for emails in users.keys():
            if email == emails:
                raise InputError("Email already belongs to a user")

    # Check if first and last name are between 1 and 50 inclusive
    if len(name_first) not in range(1, 50) or len(name_last) not in range(1,50):
        raise InputError ("First and last name must be between 1 and 50 inclusive")
    
    #Check that password is at least 6 letters
    if len(password) < 6:
        raise InputError("Password too short")

    # register a user
    # create a unique user_id
    totalUsers = len(users)
    newU_id = totalUsers + 1

    # Potential TODO:
    # For loop checking if id is in dictionary

    users[email] = {
            'u_id' : newU_id,
            'name_first' : name_first,
            'name_last' : name_last,
            'password' : password
        }
    
    # validate token
    tokens.append(email)

    return {
        'u_id' : newU_id,
        'token' : email,
    }

# TODO: figure out how to successfully logout and invalidate token
