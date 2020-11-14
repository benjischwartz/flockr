from data import users, channel, highest_ids
from error import InputError, AccessError
from check_token import user_id_given_token, permission_id_given_token
from time import time

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
 
    Parameters:
        token (str): refers to a valid user on flockr who is sending the message
        channel_id (int): identifies the channel the user is sending a message to
        message (str): contains the content of the message being sent
 
    Returns:
        (dict): {'message_id' : _}
    '''

    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError (description="User is not authorised to send a message to this channel.")
    
    # raise an inputerror if message is 0 characters or over 1000 characters in length
    if len(message) == 0: 
        raise InputError (description="This message is too short")
    elif len(message) > 1000:
        raise InputError (description="This message is too long.")
    
    # generate a unique message_id
    if 'highest_message_id' not in highest_ids:
        highest_ids['highest_message_id'] = 1
        message_id = 1
    else: 
        highest_ids['highest_message_id'] += 1
        message_id = highest_ids['highest_message_id']

    # create dictionary to store in data with the information for a message
    message_info = {
        'message_id' : message_id,
        'u_id': token_u_id,
        'message' : message,
        'time_created' : time(),
        'reacts' : [],
        'is_pinned' : False
    }
    
    # append dictionary to messages list of channel with id 'channel_id'
    channel[channel_id]['messages'].append(message_info)
    
    return {
        'message_id': message_id,
    }

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel
 
    Parameters:
        token (str): refers to a valid user on flockr who is sending the message
        message_id (int): identifies the message the user is removing
 
    Returns:
        (dict): {}
    '''
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
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
        raise InputError(description="The message id is not valid.")
             
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise AccessError (description="User is not part of the channel with this message.")
    
    token_permission_id = permission_id_given_token(token)
    # check permissions to remove and if permitted then remove message; if not 
    # raise an accesserror
    if token_u_id == message_u_id or token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
        channel[message_channel]['messages'].pop(message_index)
    else:
        raise AccessError(description="This user is not authorised to remove this message.")
    return {}
    
    
def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an 
    empty string, the message is deleted.
 
    Parameters:
        token (str): refers to a valid user on flockr who is editing the message
        message_id (int): identifies the message the user is removing
        message (str): contains the edited version of the message
 
    Returns:
        (dict): {}
    '''
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
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
        raise InputError(description="The message id is not valid.")
       
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise AccessError (description="User is not part of the channel with this message.")
    
    # remove message if the message is an empty string or raise an inputerror 
    # if the message is over 1000 characters
    if len(message) == 0: 
        message_remove(token, message_id)
        return {}
    elif len(message) > 1000:
        raise InputError (description="This message is too long.")
    
    token_permission_id = permission_id_given_token(token)
    # check permissions to edit and if permitted then change message; if not 
    # raise an accesserror
    if token_u_id == message_u_id or token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
        channel[message_channel]['messages'][message_index]['message'] = message
    else:
        raise AccessError(description="This user is not authorised to remove this message.")
    
    return {}

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message from authorised_user to the channel specified by channel_id 
    automatically at a specified time in the future
 
    Parameters:
        token (str): refers to a valid user on flockr who is sending the message
        channel_id (int): identifies the channel the user is sending a message to
        message (str): contains the content of the message being sent
        time_sent (int): identifies the time the message is meant to be sent on 
            the specified channel
 
    Returns:
        (dict): {'message_id' : ___ }
    '''

    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the time_sent is a time in the past
    if time_sent < time():
        raise InputError(description="The time you specified is a time in the past and is invalid.")
        
    # raise inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError (description="User is not authorised to send a message to this channel.")
    
    # raise an inputerror if message is 0 characters or over 1000 characters in length
    if len(message) == 0: 
        raise InputError (description="This message is too short")
    elif len(message) > 1000:
        raise InputError (description="This message is too long.")
    
    # generate a unique message_id
    if 'highest_message_id' not in highest_ids:
        highest_ids['highest_message_id'] = 1
        message_id = 1
    else: 
        highest_ids['highest_message_id'] += 1
        message_id = highest_ids['highest_message_id']

    # create dictionary to store in data with the information for a message
    message_info = {
        'message_id' : message_id,
        'u_id': token_u_id,
        'message' : message,
        'time_created' : time_sent,
        'reacts' : [],
        'is_pinned' : False
    }
    
    # append dictionary to messages list of channel with id 'channel_id'
    channel[channel_id]['messages'].append(message_info)
    
    return {
        'message_id': message_id,
    }

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special 
    display treatment by the frontend
    
    Parameters:
        token (str): refers to a valid user on flockr who is sending the message
        channel_id (int): identifies the channel the user is sending a message to
        react_id (int): identifies the type of react the user wants to make
            react_id of 1 is the only valid react for now
    
    Returns:
        (dict): {'message_id' : ___ }
    '''
    
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError(description="The message id is not valid.")
       
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise InputError (description="User is not part of the channel with this message.")
    
    if react_id != 1:
        raise InputError (description="React is invalid")
    
    react_list = channel[message_channel]['messages'][message_index]['reacts']
    if any(token_u_id in d['u_ids'] for d in react_list):
        raise InputError (description='You have already reacted to this message. Unreact first')
    else:
        react_index = next((i for i, item in enumerate(react_list) if item["react_id"] == react_id), None)
        if react_index == None:
            new_react = {'react_id' : react_id, 'u_ids' : [token_u_id]}
            react_list.append(new_react)
        else:
            react_list[react_index]['u_ids'].append(token_u_id)
            
    return {}

def message_unreact(token, message_id, react_id):
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError(description="The message id is not valid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise InputError (description="User is not part of the channel with this message.")
    
    if react_id != 1:
        raise InputError (description="React is invalid")
    
    react_list = channel[message_channel]['messages'][message_index]['reacts']
    react_index = next((i for i, item in enumerate(react_list) if item["react_id"] == react_id), None)
    if react_index == None or token_u_id not in react_list[react_index]['u_ids']:
       raise InputError(description="User has not reacted to with to this message with this react yet. You must react first to unreact.")
    
    u_id_index = react_list[react_index]['u_ids'].index(token_u_id)
    if len(channel[message_channel]['messages'][message_index]['reacts'][react_index]['u_ids']) == 1:
        react_list.pop(react_index)
    else:
        react_list[react_index]['u_ids'].pop(u_id_index)
    
    return {}

def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special 
    display treatment by the frontend
    
    Parameters:
        token (str): refers to a valid user on flockr who is sending the message
        channel_id (int): identifies the channel the user is sending a message to
        react_id (int): identifies the type of react the user wants to make
            react_id of 1 is the only valid react for now
    
    Returns:
        (dict): {'message_id' : ___ }
    '''
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError(description="The message id is not valid.")
      
    if channel[message_channel]['messages'][message_index]['is_pinned']:
        raise InputError (description="This message is already pinned.")

    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise InputError (description="User is not part of the channel with this message.")

    token_permission_id = permission_id_given_token(token)
    #   check permissions to pin and if permitted then pin message; if not 
    #   raise an accesserror
    if token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
       channel[message_channel]['messages'][message_index]['is_pinned'] = True
    else:
       raise AccessError(description="This user is not authorised to edit this message.")

    return {}

def message_unpin(token, message_id):

    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")
    
    # raise inputerror if the message_id is invalid and find the channel and
    # indexation of the message with id 'message_id'
    message_valid = False
    for a_channel in channel:
        message_index = 0
        for a_message in channel[a_channel]['messages']:
            if a_message['message_id'] == message_id:
               message_channel = a_channel
               message_valid = True
               break
            message_index += 1
        if message_valid == True:
            break
    if message_valid == False:
        raise InputError(description="The message id is not valid.")

    # raise InputError if message is already unpinned
    if channel[message_channel]['messages'][message_index]['is_pinned'] is False:
        raise InputError (description="This message is already unpinned.")

    token_permission_id = permission_id_given_token(token)
    # raise accesserror if user with token 'token' is not part of the channel
    # that the message is part of 
    if token_u_id not in channel[message_channel]['all_members']:
        raise InputError (description="User is not part of the channel with this message.")
    
    if token_permission_id == 1 or token_u_id in channel[message_channel]['owner_members']:
       channel[message_channel]['messages'][message_index]['is_pinned'] = False
    else:
       raise AccessError(description="This user is not authorised to edit this message.")

    return {}

