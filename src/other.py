from data import users, tokens, channel, highest_ids, codes, data_store, data_retreive
from check_token import user_id_given_token
from user import user_profile
from error import InputError, AccessError

def clear():
    '''
    Resets the internal data
    of the application to
    it's initial state

    returns {}
    '''
    data_retreive()

    users.clear()
    tokens.clear()
    channel.clear()
    highest_ids.clear()
    codes.clear()

    data_store()
    return {}

def users_all(token):
    '''
    Returns a list of all
    users and their associated details

    returns [{users}]
    '''
    data_retreive()
    final_list = []
    selected_email = ' '
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    for tokens, data in users.items():
        selected_email = tokens
        # Using `.pop()` here was causing data to be deleted from the database
        user = {
            'u_id': data['u_id'],
            'email': selected_email,
            'name_first': data['name_first'],
            'name_last': data['name_last'],
            'handle_str': data['handle'],
            'profile_img_url': data['profile_img_url']
        }
        final_list.append(user)

    # Should return a dictionary, not list
    return {
        'users': final_list
    }

