from auth import auth_login, auth_logout, auth_register
from data import users, tokens, channel
from error import InputError, AccessError


def channel_invite(token, channel_id, u_id):
    # get the u_id of the person with the token
    # token is email in this case so
    token_u_id = users[token]['u_id']
    # check that the user has a token and is valid
        #for emails in users.key():
            # if token == emails:
                # token_u_id = users[token]['u_id'] else etc
    
    # check user with u_id 'u_id' is a valid user; if they aren't raise an inputerror
    valid_user = False
    for user in users.keys():
        if u_id == users[user]['u_id']:
            valid_user = True
            break
    
    if valid_user == False:
        raise InputError ("This user is not a valid user")


    # check channel_id is a valid channel_id; if not raise inputError
    # check user with the token 'token' is actually part of the channel with id
    # 'channel_id'; if they aren't raise an accesserror
    # check user with u_id 'u_id' is not part of the channel with channel_id         
    authorised = False
    already_in = False
    if str(channel_id) in channel.keys():
        for member in channel[channel_id]['all_members'].keys():
            if member == token_u_id:
                authorised = True
            if member == u_id:
                already_in = True
    else:
        raise InputError ("Channel_id passed is not valid")
    
    if authorised == False:
        raise AccessError ("This user is not authorised to invite to this channel")
            
    if already_in:
        pass 

    channel[channel_id]['all_members'] = {u_id : True}
    
    return {
    }

def channel_details(token, channel_id):
    '''
    # get the u_id of the person with the token
    # token is email in this case so
    # check that the person is a valid user - implement later
    token_u_id = users[token]['u_id']
    
    # check that the channel is valid 
    authorised = False
    if channel_id in channel:
        for member in channel[channel_id]['all_members'].keys():
            if member == token_u_id:
                authorised = True
                break
    else:
        raise InputError ("Channel_id passed is not valid")
                
    if authorised == False:
        raise AccessError ("This user is not authorised to view the details of this channel")
                
    chnl_details = {}
    chnl_name = channel[channel_id]['channel_name']
    chnl_details = [name : chnl_name]
    chnl_details = ['owner_members' : []]
    for member in channel[channel_id]['owner_members']:
        
    # create a dictionary called chnl_details
    # find the name
    # Loop: get the u_id of the owners
        # get the first_name and last_name 
        # add that to chnl_details
    # get the u_id of all the members
        # get the first_name and last_name 
        # add that to channel_id
    '''        
    return {
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

def channel_messages(token, channel_id, start):
    return {
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

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    #ETHAN
    #ERROR CHECKING
    if channel_id not in channel:
        #If Channel ID is invalid
        raise InputError("Channel ID is invalid")
    if u_id in channel['owner_members'].keys():
        #If User ID is already an owner of the channel
        raise InputError("User is already an owner")
    
    #If current token is not an owner of the channel
    if channel['owner_members'].has_key(token) == False:
        raise AccessError("You are not an owner")

    #ADDING THE USER TO THE LIST OF OWNERS
    channel['owner_members'][u_id] = True
    return {

    }

def channel_removeowner(token, channel_id, u_id):
    #ETHAN
    #ERROR CHECKING
    if channel_id not in channel:
        #If Channel ID is invalid
        raise InputError("Channel ID is invalid")
    if u_id in channel['owner_members'].keys():
        #If User ID is already an owner of the channel
        raise InputError("User is already an owner")
    
    #If current token is not an owner of the channel
    if channel['owner_members'].has_key(token) == False:
        raise AccessError("You are not an owner")

    #If there are no other owners (ASSUMPTION)
    if (len(channel['owner_members']) <= 1):
        raise Exception("There must be at least one other owner in order to remove an owner")

    #REMOVING OWNER FROM THE LIST OF USERS
    channel['owner_members'].pop(u_id)

    return {

    }
