from data import users, tokens
import re
from error import InputError
from passlib.hash import sha256_crypt
import jwt

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
def check(email):
    """
    Check if a user's email is valid. Returns True if valid, False if invalid

    Parameters:
        email (str)
    """

    if(re.search(regex,email)):
        return True
    else:
        return False

    
def auth_login(email, password):
    """
    Check if a user logging in has a valid email and password 

    Parameters:
        email(str): user's email used to identify their details
        password(str): user's password which is hashed and checked against stored
        hashed passwords

    Returns:
        {is success: True} if successful
        {is success: False} if token not valid
        InputError if email entered is not valid or registered, or password not valid
    """

    # raise an inputerror if the user is already logged in (token already valid)
    for token in tokens:
        if {'email': email} == jwt.decode(token, 'secret', algorithms='HS256'):
            return { # logging in twice returns same token
                    'u_id': users[email]['u_id'],
                    'token': token,
                }

    # check if email is registered
    for emails in users.keys():
        if email == emails:            
            if sha256_crypt.verify(password, users[email]['password']): # compare hashed passwords
                #validate token
                encoded_jwt = jwt.encode({'email': email}, 'secret').decode('utf-8')
                tokens.append(encoded_jwt)
                return {
                    'u_id': users[email]['u_id'],
                    'token': encoded_jwt, ## token is a JWT where payload is user's email, secret is 'secret'
                }
    raise InputError (description="Email not found or password not valid")
    

def auth_logout(token):
    """
    Logs a user out through invalidating a token

    Parameters:
        token (str): token to be checked in list of valid tokens. If valid, token is removed

    Returns:
        {is_success: True} if a token is successfully invalidated otherwise
        {is_success: False}
    """

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
    """
    Given a user's email, password, first name and last name,
    checks if: given email is valid, first name and last name are of suitable length, 
    password is not less than 6 digits, and generates a unique user_id and handle. 

    Parameters:
        email(str): used to identify the user in the users dict
        password(str): stored as a hashed password for security
        name_first(str): must be between 1 and 50 in length (inclusive)
        name_last(str): must be between 1 and 50 in length (inclusive)

    Returns:
        {
            'u_id': new_u_id
            'token': jwt
        }
    """
    
    # raise an inputerror if email is invalid
    if not check(email):
        raise InputError (description="Invalid email")

    # raise an inputerror if email already registered to a user
    for emails in users.keys():
        if email == emails:
            raise InputError(description="Email already belongs to a user")

    # raise an inputerror if first and last name are not between 1 and 50 
    # inclusive
    if len(name_first) not in range(1, 51) or len(name_last) not in range(1,51):
        raise InputError (description="First and last name must be between 1 and 50 inclusive")
    
    # raise an inputerror if password is not at least 6 letters
    if len(password) < 6:
        raise InputError(description="Password too short")

    # register a user
    # create a unique user_id
    totalUsers = len(users)
    newU_id = totalUsers + 1

    # give first user owner permission_id, member for all else
    permission_id = 2 if newU_id != 1 else 1

    #create a unique handle -> a concatenation of lower-case only
    #first and last name. Cut off at 20 characters. 
    concatenate = name_first.lower() + name_last.lower()
    if len(concatenate) > 20:
        concatenate = concatenate[0:20]

    # if already taken, remove last two letters and add len(users) to make unique
    for key in users.keys():
        if concatenate == users[key]['handle']:
            concatenate = concatenate[0:18]    # trim two digits off the end
            totalUsers = len(users) - 1
            # if totalUsers < 10:
            #     concatenate = concatenate + str(0) + str(totalUsers)
            # else:
                
            concatenate = concatenate + str(totalUsers)


    users[email] = {
            'u_id' : newU_id,
            'name_first' : name_first,
            'name_last' : name_last,
            'password' : sha256_crypt.hash(password),   # hashed password
            'permission_id' : permission_id, 
            'handle' : concatenate,
            'profile_img_url': ''
        }
    
    # validate token
    encoded_jwt = jwt.encode({'email': email}, 'secret').decode('utf-8')
    tokens.append(encoded_jwt)
    

    return {
        'u_id' : newU_id,
        'token' : encoded_jwt,
    }
