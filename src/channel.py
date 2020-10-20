from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token, permission_id_given_token
from auth import auth_register
from channels import channels_create
from other import clear

def channel_invite(token, channel_id, u_id):

    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")
 
    # raise inputerror if the user with u_id 'u_id' is not a valid user
    valid_user = False
    for user in users.keys():
        if u_id == users[user]['u_id']:
            valid_user = True
            break
    if valid_user == False:
        raise InputError("The user you are trying to invite is not a valid user.")
    
    # raise inputerror if the channel is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
        
    # raise accesserror if user with token 'token' is not part of the channel
    token_u_id = user_id_given_token(token)
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError ("User is not authorised to invite to this channel.")
    
    # print message when user with u_id 'u_id' is already part of the channel 
    if u_id in channel[channel_id]['all_members']:
        print("The user you are trying to add is already in the channel.")
        return {}
    
    # add member with u_id as a member of the channel
    channel[channel_id]['all_members'][u_id] = True
    
    return {}

def channel_details(token, channel_id):

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
        raise AccessError ("This user is not authorised to view the details of this channel.")
    
    # create return dictionary   
    chnl_details = {}
    chnl_details['name'] = channel[channel_id]['channel_name']
    chnl_details['owner_members'] = []
    chnl_details['all_members'] = []
    
    # find owners of channel and  their u_id, first name and last name
    for owner_member in channel[channel_id]['owner_members']:
        for user in users.keys():
            if owner_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        owner_dict = { 'u_id' : owner_member, 'name_first' : first_name, 'name_last' : last_name}
        chnl_details['owner_members'].append(owner_dict)
    
    # find all members of channel and  their u_id, first name and last name  
    for any_member in channel[channel_id]['all_members']:
        for user in users.keys():
            if any_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        any_member_dict = { 'u_id' : any_member, 'name_first' : first_name, 'name_last' : last_name}
        chnl_details['all_members'].append(any_member_dict)
    
    return chnl_details
    #### format for return ####
    # {
    #   'name': 'Hayden',
    #   'owner_members': [
    #       {
    #           'u_id': 1,
    #           'name_first': 'Hayden',
    #           'name_last': 'Jacobs',
    #       }
    #   ],
    #   'all_members': [
    #       {
    #           'u_id': 1,
    #           'name_first': 'Hayden',
    #           'name_last': 'Jacobs',
    #       }
    #   ],
    # }


def channel_messages(token, channel_id, start):
    
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
        raise AccessError ("This user is not authorised to view the messages of this channel.")
   
    # raise inputerror if start is greater than the total number of messages
    # in the channel
    total_messages = len(channel[channel_id]['messages'])
    if start > total_messages:
        raise InputError ("Start is greater than the total number of messages in the channel.")
    
    # raise inputerror if start is less than 0 (zero is the most recent message)
    if start < 0:
        raise InputError ("Start is below zero.")
    
    # create return dictionary
    chnl_msgs = {}
    chnl_msgs['messages'] = []
    chnl_msgs['start'] = start
    num_message = 0
    
    # find the details of each message in the channel up to start + 50
    for message in reversed(channel[channel_id]['messages']):
        if num_message >= start and num_message < (start + 50):
            msg_id = message['message_id']
            msg_u_id = message['u_id']
            msg_content = message['message']
            msg_time = message['time_created']
            msg_dict = {'message_id': msg_id, 'u_id' : msg_u_id, 
                'message' : msg_content, 'time_created' : msg_time}
            chnl_msgs['messages'].append(msg_dict)
        num_message += 1
        if num_message == start + 50:
            break
    
    # create and determine the value for end in the return dictionary
    if num_message < start + 50:
        chnl_msgs['end'] = -1
    else:
        chnl_msgs['end'] = num_message
       
    return chnl_msgs
    #### format for return ####
    # {
    # 'messages': [
    #       {
    #           'message_id': 1,
    #           'u_id': 1,
    #           'message': 'Hello world',
    #           'time_created': 1582426789,
    #       }
    #   ],
    #   'start': 0,
    #   'end': 50,
    # }

def channel_leave(token, channel_id):
    
    # raise accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")

    # raise inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
        
    # check for specific user and remove them from the list
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError("Member not in selected channel.")
    else:
        channel[channel_id]['all_members'].pop(token_u_id)
        
    # if the user is an owner, remove them from the list
    if token_u_id in channel[channel_id]['owner_members']:
        channel[channel_id]['owner_members'].pop(token_u_id)
        
    return {}

def channel_join(token, channel_id):
   
    # raise an accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError("Token passed is not valid.")

    # raise an inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
        
    # raise an accesserror if the user is already in the channel
    if token_u_id in channel[channel_id]['all_members']:
        raise AccessError("User is already in the channel.")
        
    # check if channel is public or private
    # if the channel is private only the owner of flockr can join 
    # token_u_id 1 is the owner of flockr
    permission_id = permission_id_given_token(token)
    if channel[channel_id]['is_public'] == False and permission_id != 1:
        raise AccessError("User does not have access to this channel.")
    
    channel[channel_id]['all_members'][token_u_id] = True
    
    return {}

def channel_addowner(token, channel_id, u_id):
    """ Making a user an owner of the channel """
    # raise an inputerror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
        
    # raise an inputerror if the channel_id is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid,")
        
    # raise an input error if the user with user with u_id 'u_id' is already
    # an onwer
    if u_id in channel[channel_id]['owner_members']:
        raise InputError("User is already an owner.")    
    
    # if current token is not an owner of the channel, they can addowner if 
    # they are the owner of flockr (owner of flockr has u_id of 1)
    permission_id = permission_id_given_token(token)
    if permission_id == 1:
        # raise accesserror if owner of Flockr is not a member of the channel
        if token_u_id not in channel[channel_id]['all_members']:
            raise AccessError("Owner of Flockr is not a member of the channel.")
    elif token_u_id not in channel[channel_id]['owner_members']:
        raise AccessError("You are not an owner.")
    
    # adding the user as an owner
    channel[channel_id]['owner_members'][u_id] = True

    # in the case of adding a user who is not a member of the channel
    channel[channel_id]['all_members'][u_id] = True

    return {}

def channel_removeowner(token, channel_id, u_id):
    """ Removing an owner from the channel and making them an ordinary member instead """
    # raise an accesserror if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError("Token passed is not valid.")
    
    # raise an inputerror if channel_id is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
    
    # raise an inputerror if channel_id is invalid
    if u_id not in channel[channel_id]['owner_members']:
        raise InputError("Attempting to remove an owner who is not an owner.")   

    # if current token is not an owner of the channel, they can removeonwer if 
    # they are the owner of flockr (owner of flockr has u_id of 1)
    permission_id = permission_id_given_token(token)
    if permission_id == 1:
        # raise accesserror if owner of Flockr is not a member of the channel
        if token_u_id not in channel[channel_id]['all_members']:
            raise AccessError("Owner of Flockr is not a member of the channel.")
    elif token_u_id not in channel[channel_id]['owner_members']:
        raise AccessError("You are not an owner.")

    # removing owner from the list of owner members
    channel[channel_id]['owner_members'].pop(u_id)

    return {}

