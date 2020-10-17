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
    # TODO: update from email to token once token hashing is integrated
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
    return jwt.encode({'email': email}, 'secret')

def email_given_jwt(token):
    """
    returns user's email given their jwt hashed
    token
    """
    decoded_jwt = jwt.decode(token, 'secret')
    return decoded_jwt['email']