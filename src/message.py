from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token, permission_id_given_token
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
        'message' : message,
        'time_created' : time()
    }
    
    # append dictionary to messages list of channel with id 'channel_id'
    channel[channel_id]['messages'].append(message_info)
    
    
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_u_id = a_message['u_id']
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError("The message id is not valid.")
             
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise AccessError ("User is not part of the channel with this message.")
    
    token_permission_id = permission_id_given_token(token)
    # check permissions to remove and if permitted then remove message; if not 
    # raise an accesserror
    if token_u_id == message_u_id or token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
        channel[message_channel]['messages'].pop(message_index)
    else:
        raise AccessError("This user is not authorised to remove this message.")
    return {}
    
    
def message_edit(token, message_id, message):
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_u_id = a_message['u_id']
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError("The message id is not valid.")
       
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise AccessError ("User is not part of the channel with this message.")
    
    # remove message if the message is an empty string or raise an inputerror 
    # if the message is too long
    if len(message) == 0: 
        message_remove(token, message_id)
        return {}
    elif len(message) > 1000:
        raise InputError ("This message is too long.")
    
    token_permission_id = permission_id_given_token(token)
    # check permissions to edit and if permitted then change message; if not 
    # raise and accesserror
    if token_u_id == message_u_id or token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
        channel[message_channel]['messages'][message_index]['message_content'] = message
    else:
        raise AccessError("This user is not authorised to remove this message.")
    
    return {}

