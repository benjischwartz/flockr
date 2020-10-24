from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token, permission_id_given_token
from auth import auth_register
from channels import channels_create
from other import clear

def channel_invite(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id. 
    Once invited the user is added to the channel immediately
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
        channel_id (int): identifies the channel the user is being added to
        u_id (int): identifies a user on flockr; this user is the invitee
 
    Returns:
        (dict): {}
    '''
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid.")
 
    # raise inputerror if the user with u_id 'u_id' is not a valid user
    valid_user = False
    for user in users.keys():
        if u_id == users[user]['u_id']:
            valid_user = True
            break
    if valid_user == False:
        raise InputError(description="The user you are trying to invite is not a valid user.")
    
    # raise inputerror if the channel is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError (description="User is not authorised to invite to this channel.")
    
    # print message when user with u_id 'u_id' is already part of the channel 
    if u_id in channel[channel_id]['all_members']:
        return {}
    
    # add member with u_id as a member of the channel
    channel[channel_id]['all_members'][u_id] = True
    
    return {}

def channel_details(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of, 
    provide basic details about the channel
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
        channel_id (int): identifies the channel that's details are being returned
 
    Returns:
        (dict): {
            'name': 'Hayden',
            'owner_members': [
               {
                   'u_id': 1,
                   'name_first': 'Hayden',
                   'name_last': 'Jacobs',
               }
           ],
           'all_members': [
               {
                   'u_id': 1,
                   'name_first': 'Hayden',
                   'name_last': 'Jacobs',
               }
           ],
         }

    '''
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid.")

    # raise inputerror if the channel is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
    

    # raise accesserror if user with token 'token' is not part of the channel
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError (description="This user is not authorised to view the details of this channel.")
    
    # create return dictionary   
    details = {}
    details['name'] = channel[channel_id]['channel_name']
    details['owner_members'] = []
    details['all_members'] = []
    
    # find owners of channel and  their u_id, first name and last name
    for owner_member in channel[channel_id]['owner_members']:
        for user in users.keys():
            if owner_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        owner_details = {  'u_id' : owner_member, 
                        'name_first' : first_name, 
                        'name_last' : last_name }
        details['owner_members'].append(owner_details)
    
    # find all members of channel and  their u_id, first name and last name  
    for any_member in channel[channel_id]['all_members']:
        for user in users.keys():
            if any_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        any_member_details = { 'u_id' : any_member, 
                            'name_first' : first_name, 
                            'name_last' : last_name }
        details['all_members'].append(any_member_details)
    
    return details


def channel_messages(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of, 
    returns up to 50 messages between index "start" and "start + 50". 
    Message with index 0 is the most recent message in the channel. This function 
    returns a new index "end" which is the value of "start + 50", or, 
    if this function has returned the least recent messages in the channel, returns -1 
    in "end" to indicate there are no more messages to load after this return.
 
    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        channel_id (int): identifies the channel that's messages are being returned
        start (int): identifies the message index that this function will return from;

    Returns:
        (dict): {
            'messages': [
               {
                   'message_id': 1,
                   'u_id': 1,
                   'message': 'Hello world',
                   'time_created': 1582426789,
               }
           ],
           'start': 0,
           'end': 50,
         }
    '''
        
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid.")

    # raise inputerror if the channel is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
    
    # raise accesserror if user with token 'token' is not part of the channel
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError (description="This user is not authorised to view the messages of this channel.")
   
    # raise inputerror if start is greater than the total number of messages
    # in the channel
    total_messages = len(channel[channel_id]['messages'])
    if start > total_messages:
        raise InputError (description="Start is greater than the total number of messages in the channel.")
    
    # raise inputerror if start is less than 0 (zero is the most recent message)
    if start < 0:
        raise InputError (description="Start is below zero.")
    
    # create return dictionary
    all_messages = {}
    all_messages['messages'] = []
    all_messages['start'] = start
    num_message = 0
    
    # find the details of each message in the channel up to start + 50
    for message in reversed(channel[channel_id]['messages']):
        if num_message >= start and num_message < (start + 50):
            msg_id = message['message_id']
            msg_u_id = message['u_id']
            msg_content = message['message']
            msg_time = message['time_created']
            message_dict = {'message_id': msg_id, 
                            'u_id' : msg_u_id, 
                            'message' : msg_content, 
                            'time_created' : msg_time}
            all_messages['messages'].append(message_dict)
        num_message += 1
        if num_message == start + 50:
            break
    
    # determine and create the value for end in the return dictionary
    if num_message < start + 50:
        all_messages['end'] = -1
    else:
        all_messages['end'] = num_message
       
    return all_messages

def channel_leave(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of, 
    the function removes the current user as a member of the channel.
 
    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        channel_id (int): identifies the channel that the current user is leaving

    Returns:
        (dict): {

        }
    '''

    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid.")

    # raise inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
        
    # check for specific user and remove them from the list
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError(description="Member not in selected channel.")
    else:
        channel[channel_id]['all_members'].pop(token_u_id)
        
    # if the user is an owner, remove them from the list
    if token_u_id in channel[channel_id]['owner_members']:
        channel[channel_id]['owner_members'].pop(token_u_id)
        
    return {}

def channel_join(token, channel_id):
    '''
    Given a Channel with ID channel_id the function adds the current authorised
    user as a member of the channel.
 
    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        channel_id (int): identifies the channel that the current user is joining

    Returns:
        (dict): {

        }
    '''

    # raise an accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid.")

    # raise an inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
        
    # raise an accesserror if the user is already in the channel
    if token_u_id in channel[channel_id]['all_members']:
        raise AccessError(description="User is already in the channel.")
        
    # check if channel is public or private
    # if the channel is private only the owner of flockr can join 
    # token_u_id 1 is the owner of flockr
    permission_id = permission_id_given_token(token)
    if channel[channel_id]['is_public'] == False and permission_id != 1:
        raise AccessError(description="User does not have access to this channel.")
    
    channel[channel_id]['all_members'][token_u_id] = True
    
    return {}

def channel_addowner(token, channel_id, u_id):
    """ 
    Adding a user as an owner of the specified channel. THe user is not required to 
    be an ordinary member before being made an owner of the channel. Only an owner
    of the channel or an owner of Flockr has the permissions to add owners.
        
    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        channel_id (int): identifies the channel that owners are being added to
        u_id (int): identifies the user that is to be added as an owner of the channel
    
    Returns:
        {}
    """
    # raise an inputerror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid.")
        
    # raise an inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid,")
        
    # raise an input error if the user with user with u_id 'u_id' is already
    # an onwer
    if u_id in channel[channel_id]['owner_members']:
        raise InputError(description="User is already an owner.")    
    
    # if current token is not an owner of the channel, they can addowner if 
    # they are the owner of flockr (owner of flockr has u_id of 1)
    permission_id = permission_id_given_token(token)
    if permission_id == 1:
        # raise accesserror if owner of Flockr is not a member of the channel
        if token_u_id not in channel[channel_id]['all_members']:
            raise AccessError(description="Owner of Flockr is not a member of the channel.")
    elif token_u_id not in channel[channel_id]['owner_members']:
        raise AccessError(description="You are not an owner.")
    
    # adding the user as an owner
    channel[channel_id]['owner_members'][u_id] = True

    # in the case of adding a user who is not a member of the channel
    channel[channel_id]['all_members'][u_id] = True

    return {}

def channel_removeowner(token, channel_id, u_id):
    """ 
    Removes an owner of the specified channel. When the owner is removed they become an 
    ordinary member isntead. Only an owner of the channel or an owner of Flockr has the 
    permissions to remove owners.
        
    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        channel_id (int): identifies the channel that owners are being removed from
        u_id (int): identifies the user that is to be removed as an owner of the channel
    
    Returns:
        {}
    """
    # raise an accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid.")
    
    # raise an inputerror if channel_id is invalid
    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")
    
    # raise an inputerror if channel_id is invalid
    if u_id not in channel[channel_id]['owner_members']:
        raise InputError(description="Attempting to remove an owner who is not an owner.")   

    # if current token is not an owner of the channel, they can removeonwer if 
    # they are the owner of flockr (owner of flockr has u_id of 1)
    permission_id = permission_id_given_token(token)
    if permission_id == 1:
        # raise accesserror if owner of Flockr is not a member of the channel
        if token_u_id not in channel[channel_id]['all_members']:
            raise AccessError(description="Owner of Flockr is not a member of the channel.")
    elif token_u_id not in channel[channel_id]['owner_members']:
        raise AccessError(description="You are not an owner.")

    # removing owner from the list of owner members
    channel[channel_id]['owner_members'].pop(u_id)

    return {}

