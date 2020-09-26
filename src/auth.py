from data import users
import re
from error import InputError

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check(email):
    if(re.search(regex,email)):
        return("Valid Email")
    else:
        return("Invalid Email")

    
def auth_login(email, password):
    # check if email is registered
    login = False
    for user in users.keys():
        if user == email:            
            if users[user]['password'] == password:
                print("Login successful")
                return {
                    'u_id': email,  ## need to correct this
                    'token': email, ## for iteration 1, tokens can just be email or id
                }
    raise InputError ("Email not found or password not valid")
    

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    
    # Check if valid email
    if (check(email) != "Valid Email"):
        raise InputError ("Invalid email")
        
    # register a user
    users[email] = {
            'name_first' : name_first,
            'name_last' : name_last,
            'email' : email,
            'password' : password
        }
    return {
        'u_id' : email,
        'token' : email,
    }