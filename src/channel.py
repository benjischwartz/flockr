from data import channel, users
import error


def channel_invite(token, channel_id, u_id):
    
    # check channel_id is a valid channel_id; if not raise inputError
    
    # check user with the token 'token' is actually part of the channel with id
    # 'channel_id'; if they aren't raise an accesserror
    
    # check user with u_id 'u_id' is a valid user? (is this necessary)
    # check user with u_id 'u_id' is not part of the channel with channel_id
        #if they are, raise inputerror or just do nothing
        
    # find channel[channel_id][all_members] and add u_id 
    
    return {
    }

def channel_details(token, channel_id):

    # check that the person is a valid user??? 
    # check that the channel is valid 
        # for chan in channel
        # if chan == channel_id ??(might be better way to do this)'
    # check the channel with channel_id and see if the user is part of 
    # channel; if not raise an accesserror
    
    # create a dictionary called chnl_details
    # find the name
    # Loop: get the u_id of the owners
        # get the first_name and last_name 
        # add that to chnl_details
    # get the u_id of all the members
        # get the first_name and last_name 
        # add that to channel_id
        
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
    if channel.has_key(channel_id) == False:
        #If Channel ID is invalid
        raise error.InputError("Channel ID is invalid")
    if u_id in channel['owner_members'].keys():
        #If User ID is already an owner of the channel
        raise error.InputError("User is already an owner")
    
    #If current token is not an owner of the channel
    if channel['owner_members'].has_key(token) == False:
        raise error.AccessError("You are not an owner")

    #ADDING THE USER TO THE LIST OF OWNERS
    channel['owner_members'][u_id] = True
    return {

    }

def channel_removeowner(token, channel_id, u_id):
    #ETHAN
    #ERROR CHECKING
    if channel.has_key(channel_id) == False:
        #If Channel ID is invalid
        raise error.InputError("Channel ID is invalid")
    if u_id in channel['owner_members'].keys():
        #If User ID is already an owner of the channel
        raise error.InputError("User is already an owner")
    
    #If current token is not an owner of the channel
    if channel['owner_members'].has_key(token) == False:
        raise error.AccessError("You are not an owner")

    #If there are no other owners (ASSUMPTION)
    if (len(channel['owner_members']) <= 1):
        raise Exception("There must be at least one other owner in order to remove an owner")

    #REMOVING OWNER FROM THE LIST OF USERS
    channel['owner_members'].pop(u_id)

    return {

    }
