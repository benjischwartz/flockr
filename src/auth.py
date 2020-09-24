from data import data
import re
from error import InputError

def auth_login(email, password):
    # check if email is registered
    # login = False
    # for user in data.items():
    #     if user['email'] == email:
    #         if user['password'] == password:
    #             login = True
    #             return {
    #                 'u_id': 1,       ## need to correct this --> this is just email
    #                 'token': '12345', ## for iteration 1, tokens can just be email or id
    #             }
    # return InputError
    return {
        'u_id': 1,       ## need to correct this
        'token': '12345', ## for iteration 1, tokens can just be email or id
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    # Check if valid email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        return InputError
        
    # register a user
    NewUser = {
        'email': email,
        'password':password,
        'email': {
            'name_first' : name_first,
            'name_last' : name_last,
            'u_id' : 1      ## need to correct this
        }
    }
    data['users'] = NewUser
    return {
        'u_id': 1,
        'token': '12345',
    }
