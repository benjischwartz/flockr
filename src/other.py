from data import users, tokens, channel
from check_token import user_id_given_token
from user import user_profile
from error import InputError, AccessError

def clear():
    users.clear()
    tokens.clear()
    channel.clear()

def users_all(token):
    temp = users
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
    
    for token in temp:
        temp[token].pop('password')
        temp[token].pop('permission_id')

    return temp

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }