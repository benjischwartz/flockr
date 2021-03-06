from data import users, tokens, codes
import re
from error import InputError
from passlib.hash import sha256_crypt
import jwt
from check_token import email_given_jwt
from check_reset_code import email_given_code
from data_persistence import data_store

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
        if email == email_given_jwt(token):
            data_store()
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
                data_store()
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
            data_store()
            return {
                'is_success': True,
            }

    data_store()
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
    
    data_store()
    return {
        'u_id' : newU_id,
        'token' : encoded_jwt,
    }

def auth_passwordreset_request(email):
    """
    Given an email address, if the user is a registered user, send's them an email containing 
    a specific secret code, that when entered in auth_passwordreset_reset, shows that the user 
    trying to reset the password is the one who got sent this email.
    """
    # create a hashed code with jwt.encode(), using the user's email as the payload, 
    # and 'reset' as the secret
    for emails in users.keys():
        if email == emails:
            code = jwt.encode({'email': email}, 'reset').decode('utf-8')
            codes[email] = code
            data_store()
            return {}
    raise InputError (description="Supplied email not valid")



def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a reset code for a user, set that user's new password to the password provided.
    """
    email = email_given_code(reset_code)
    if email is not None:
        # raise an InputError if password is not at least 6 letters, 
        # or if new password is the same as old password
        if len(new_password) < 6:
            raise InputError(description="Password too short")

        elif sha256_crypt.verify(new_password, users[email]['password']):
            raise InputError(description="New password same as old password")

        # reset password
        users[email]['password'] = sha256_crypt.hash(new_password)

        # remove code from codes dictionary
        del codes[email]
        data_store()
        return {}
    
    raise InputError (description="Reset code is not valid")
