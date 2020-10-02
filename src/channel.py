from auth import auth_login, auth_logout, auth_register
from data import users, tokens, channel
from error import InputError, AccessError
from check_token import is_valid_token, user_id_given_token


def channel_invite(token, channel_id, u_id):

    # raise an exception if the token is invalid
    valid_token = is_valid_token(token)
    if valid_token == False:
        raise AccessError("Token passed in is not valid")
 
    # raise an exception if the user with u_id 'u_id' is not a valid user
    valid_user = False
    for user in users.keys():
        if u_id == users[user]['u_id']:
            valid_user = True
            break
    if valid_user == False:
        raise InputError("This user is not a valid user.")
    
    # raise an exception if the channel is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid.")
        
    # raise exception if user with token 'token' is not part of the channel
    token_u_id = users[token]['u_id']
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError ("This user is not authorised to invite to this channel.")
    
    # print message when user with u_id 'u_id' is already part of the channel 
    if u_id in channel[channel_id]['all_members']:
        print("The user you are trying to add is already in the channel")
        return {}
    
    channel[channel_id]['all_members'][u_id] = True
    
    return {}

def channel_details(token, channel_id):

    # raise an exception if the token is invalid
    valid_token = is_valid_token(token)
    if valid_token == False:
        raise AccessError("Token passed in is not valid")

    # raise an exception if the channel is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid")
    

    # raise exception if user with token 'token' is not part of the channel
    token_u_id = users[token]['u_id']
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError ("This user is not authorised to view the details of this channel")
        
    chnl_details = {}
    chnl_details['name'] = channel[channel_id]['channel_name']
    chnl_details['owner_members'] = []
    chnl_details['all_members'] = []
    
    for owner_member in channel[channel_id]['owner_members']:
        for user in users.keys():
            if owner_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        owner_dict = { 'u_id' : owner_member, 'name_first' : first_name, 'name_last' : last_name}
        chnl_details['owner_members'].append(owner_dict)
        
    for any_member in channel[channel_id]['all_members']:
        for user in users.keys():
            if any_member == users[user]['u_id']:
                first_name = users[user]['name_first']
                last_name = users[user]['name_last']
        any_member_dict = { 'u_id' : any_member, 'name_first' : first_name, 'name_last' : last_name}
        chnl_details['all_members'].append(any_member_dict)
    
    return chnl_details


def channel_messages(token, channel_id, start):
    # raise an exception if the token is invalid
    valid_token = is_valid_token(token)
    if valid_token == False:
        raise AccessError("Token passed in is not valid")

    # raise an exception if the channel is invalid
    if channel_id not in channel:
        raise InputError("Channel ID is invalid")
    
    # raise exception if user with token 'token' is not part of the channel
    token_u_id = users[token]['u_id']
    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError ("This user is not authorised to view the messages of this channel")
   
    # raise an exception if start is greater than the total number of messages
    # in the channel
    total_messages = len(channel[channel_id]['messages'])
    if start > total_messages:
        raise InputError ("Start is greater than the total number of messages in the channel")
    
    if start < 0:
        raise InputError ("Start is below zero")
    
    chnl_msgs = {}
    chnl_msgs['messages'] = []
    chnl_msgs['start'] = start
    num_message = 0
    for message in reversed(channel[channel_id]['messages']):
        if num_message >= start and num_message < (start + 50):
            msg_id = message['message_id']
            msg_u_id = message['u_id']
            msg_content = message['message_content']
            msg_time = message['time_created']
            msg_dict = {'message_id': msg_id, 'u_id' : msg_u_id, 
                'message' : msg_content, 'time_created' : msg_time}
            chnl_msgs['messages'].append(msg_dict)
        num_message += 1
        if num_message == start + 50:
            break
    
    if num_message < start + 50:
        chnl_msgs['end'] = -1
    else:
        chnl_msgs['end'] = num_message
       
    return chnl_msgs

if __name__ == '__main__':
    print(channel_messages('benji.schwartz@gmail.com',8, 0))
    num = 3
    for num in range(3,100):
        msg_id = num
        msg_dict_new = {'message_id': msg_id, 'u_id' : 1, 'message_content' : 'Hello', 'time_created': '7:00pm'}
        channel[8]['messages'].append(msg_dict_new)
        num += 1
    print(channel_messages('benji.schwartz@gmail.com',8, 0))
    print(channel_messages('benji.schwartz@gmail.com',8, 60))
    print(channel_messages('benji.schwartz@gmail.com',8, 40))
    print(channel_messages('benji.schwartz@gmail.com',8, 99))

def channel_leave(token, channel_id):

    valid_token = is_valid_token(token)
    if valid_token == False:
        raise AccessError("Token passed in is not valid")
    token_u_id = users[token]['u_id']
    # If the channel doesn't exist
    if channel_id not in channel:
        raise InputError("Channel ID is invalid")
    #check for specific person and remove him from the list
    for member in channel[channel_id]['all_members']:
        if member == token_u_id:
            channel[channel_id]['owner_members'].pop(token_u_id)
            return
    
    raise AccessError("Member not in selected Channel")

def channel_join(token, channel_id):

    valid_token = is_valid_token(token)
    if valid_token == False:
        raise AccessError("Token passed in is not valid")
    token_u_id = users[token]['u_id']
    #If the channel doesn't exist
    if channel_id not in channel:
        raise InputError("Channel ID is invalid")
        
    #If member already in channel
    if token_u_id in channel[channel_id]['all_members']:
        raise InputError("User is already in the channel")
    
    if channel[channel_id]['is_public'] == False:
        raise AccessError("User does not have access to this channel")
    
    channel[channel_id]['owner_members'][token_u_id] = True

def channel_addowner(token, channel_id, u_id):
    #ETHAN
    #ERROR CHECKING
    if channel_id not in channel:
        #If Channel ID is invalid
        raise InputError("Channel ID is invalid")
    if u_id in channel[channel_id]['owner_members']:
        #If User ID is already an owner of the channel
        raise InputError("User is already an owner")    
    
    
    #If current token is not an owner of the channel
    if user_id_given_token(token) not in channel[channel_id]['owner_members']:
        raise AccessError("You are not an owner")

    #ADDING THE USER TO THE LIST OF OWNERS
    channel[channel_id]['owner_members'][u_id] = True
    return {

    }

def channel_removeowner(token, channel_id, u_id):
    #ETHAN
    #ERROR CHECKING
    if channel_id not in channel:
        #If Channel ID is invalid
        raise InputError("Channel ID is invalid")
    if u_id in channel[channel_id]['owner_members']:
        #If User ID is already an owner of the channel
        raise InputError("User is already an owner")
    
    #If current token is not an owner of the channel
    if token not in channel[channel_id]['owner_members']:
        raise AccessError("You are not an owner")

    #If there are no other owners (ASSUMPTION)
    if (len(channel[channel_id]['owner_members']) <= 1):
        raise Exception("There must be at least one other owner in order to remove an owner")

    #REMOVING OWNER FROM THE LIST OF USERS
    channel[channel_id]['owner_members'].pop(u_id)

    return {

    }

