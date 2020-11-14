from data import users, tokens
import jwt

def user_id_given_token(token):
    '''
    returns the u_id if the token is valid, i.e.
    if the user is in database AND is logged in
    otherwise returns None
    '''
    e = email_given_jwt(token)
    if token in tokens:
        if e in users:
            user_id = users[e]['u_id']
            return user_id
    return None


def get_handle(u_id):
    '''
    returns the handle if the u_id is valid
    otherwise returns None
    '''
    for email in users.keys():
        if u_id == users[email]['u_id']:
            return users[email]['handle']
    return

def email_given_user_id(u_id):
    '''
    returns the email if the u_id is valid,
    otherwise returns None
    '''
    for email in users:
        if u_id == users[email]['u_id']:
            return email
    return None

def permission_id_given_token(token):
    """
    returns the permission id given a valid token
    otherwise raises KeyError
    """
    email = email_given_jwt(token)
    return users[email]["permission_id"]

def jwt_given_email(email):
    """
    returns a jwt hashed token given the user's 
    email as the `payload`
    """   
    return jwt.encode({'email': email}, 'secret').decode('utf-8')


def email_given_jwt(token):
    """
    returns user's email given their jwt hashed
    token if valid jwt is given, otherwise returns None
    """
    try:
        decoded_jwt = jwt.decode(token, 'secret', algorithms='HS256')
        return decoded_jwt['email']
    except Exception:
        return None


