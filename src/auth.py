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

    # raise an inputerror if the user is already logged in (token already valid)
    for token in tokens:
        if email == token:
            return { # logging in twice returns same token
                    'u_id': users[email]['u_id'],
                    'token': email,
                }

    # check if email is registered
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
    
    # raise an inputerror if email is invalid
    if (check(email) != "Valid Email"):
        raise InputError ("Invalid email")

    # raise an inputerror if email already registered to a user
    else:
        for emails in users.keys():
            if email == emails:
                raise InputError("Email already belongs to a user")

    # raise an inputerror if first and last name are not between 1 and 50 
    # inclusive
    if len(name_first) not in range(1, 51) or len(name_last) not in range(1,51):
        raise InputError ("First and last name must be between 1 and 50 inclusive")
    
    # raise an inputerror if password is not at least 6 letters
    if len(password) < 6:
        raise InputError("Password too short")

    # register a user
    # create a unique user_id
    totalUsers = len(users)
    newU_id = totalUsers + 1

    #create a unique handle -> a concatenation of lower-case only
    #first and last name. Cut off at 20 characters. 
    concatenate = name_first.lower() + name_last.lower()
    if len(concatenate) > 20:
        concatenate = concatenate[0:20]

    #if already taken, remove last two letters and add len(users) to make unique
    for email in users.keys():
        if concatenate == users[email]['handle']:
            concatenate = concatenate[0:18]    # trim two digits off the end
            totalUsers = len(users)
            if totalUsers < 10:
                concatenate = concatenate + str(0) + str(totalUsers)
            else:
                concatenate = concatenate + str(totalUsers)
             
    users[email] = {
            'u_id' : newU_id,
            'name_first' : name_first,
            'name_last' : name_last,
            'password' : password,
            'handle' : concatenate,
        }
    print(users[email]['handle'])
    
    # validate token
    tokens.append(email)

    return {
        'u_id' : newU_id,
        'token' : email,
    }

def get_handle(u_id):
    for email in users.keys():
        if u_id == users['u_id']:
            return users[email]['handle']

    return 
