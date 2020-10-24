from data import users, tokens, channel
from check_token import user_id_given_token
from user import user_profile
from error import InputError, AccessError

def clear():
    """ Resets the internal data of the application to it's initial state """
    users.clear()
    tokens.clear()
    channel.clear()
    return {}

def users_all(token):
    """ returns a list with details of every user """
    finallist = []
    selected_email = ' '
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid.")
    
    for tokens, data in users.items():
        selected_email = tokens
        data.pop('password')
        data.pop('permission_id')
        data['email'] = selected_email
        finallist.append(data)

    return finallist

