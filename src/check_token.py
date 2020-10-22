from data import users, tokens

def user_id_given_token(token):
    '''
    returns the u_id if the token is valid, i.e.
    if the user is in database AND is logged in
    otherwise returns None
    '''
    if token in tokens and token in users:
        return users[token]['u_id']
    else:        
        return None


def get_handle(u_id):
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

def permission_id_given_token(email):
    # TODO: update from email to token once token hashing is integrated
    """
    returns the permission id given a valid token
    otherwise raises KeyError
    """
    return users[email]["permission_id"]

