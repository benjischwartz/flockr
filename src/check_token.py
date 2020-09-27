### this is a prototype for matching tokens with users in the database
## required to be updated when auth.py is completed
## assumes the token is a string of the int which is u_id

from data import users

def is_valid_token(token):
    '''
    returns true or false if token, email, is in user database
    '''
    if token in users:
        return True
    return False

def user_id_given_token(token):
    '''
    returns the u_id if the user is in the database
    otherwise returns None if u_id is not found
    '''
    if token in users:
        user_id = users[token]['u_id']
        return user_id
    return None
