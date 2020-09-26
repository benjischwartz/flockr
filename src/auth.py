from data import users
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
    # for u_id in users.keys():
    #     print(u_id, users[u_id])

    return {
        'u_id': 1,       ## need to correct this
        'token': '12345', ## for iteration 1, tokens can just be email or id
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    # # Check if valid email
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # if not re.search(regex, email):
    #     raise LoginError ("Email entered is not valid")
        
    # # register a user
    # users[email] = {
    #         'name_first' : name_first,
    #         'name_last' : name_last,
    #         'email' : email,
    #         'password' : password
    #     }
    return {
        'u_id' : email,
        'token' : email,
    }

auth_register(benji.schwartz2013gmail.com, Yolo1400, Benji, Schwartz)
auth_login(benji.schwartz2013gmail.com, Yolo1400)

print(data.users)