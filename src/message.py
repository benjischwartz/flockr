from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token
from time import time

def message_send(token, channel_id, message):
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")
    
    # raise inputerror if the channel is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    token_u_id = user_id_given_token(token)
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError ("User is not authorised to invite to this channel.")
    
    # raise an inputerror if message is 0 characters or over 1000 characters in length
    if len(message) == 0: 
        raise InputError ("This message is too short")
    elif len(message) > 1000:
        raise InputError ("This message is too long.")
    
    # generate a unique message_id
    total_messages = 0
    for each_channel in channel:
         total_messages += len(channel[each_channel]['messages']) 
    message_id = total_messages + 1
    
    # create dictionary to store in data with the information for a message
    message_info = {
        'message_id' : message_id,
        'u_id': token_u_id,
        'message_content' : message,
        'time_created' : time()
    }
    
    # append dictionary to messages list of channel with id 'channel_id'
    channel[channel_id]['messages'].append(message_info)
    
    
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
