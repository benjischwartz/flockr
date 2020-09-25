### this is a prototype for matching tokens with users in the database
## required to be updated when auth.py is completed
## assumes the token is a string of the int which is u_id

from data import users

def is_valid_token(token):
    '''
    returns true or false if u_id is in user database
    '''
    if type(token) is str and token.isnumeric():
        intToken = int(token)
        if token in users:
            return True
    return False

def user_id_given_token(token):
    '''
    returns None if u_id is not found in user database
    otherwise returns the u_id(int)
    '''
    if type(token) is str and token.isnumeric():
        intToken = int(token)
        if token in users:
            return intToken
    return None
