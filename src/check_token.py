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

