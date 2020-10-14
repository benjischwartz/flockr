from data import users, channel
from check_token import user_id_given_token
from user import user_profile
from error import InputError, AccessError

def users_all(token):
    temp = users
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
    
    for token in temp:
        temp[token].pop('password')

    return temp