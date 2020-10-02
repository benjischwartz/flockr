from data import channel, users, tokens
from error import InputError, AccessError


def channels_list(token):
    # raise ACCESS ERROR if token is invalid
    if is_valid_token(token) == False:
        raise AccessError("Token passed in is not valid")  

    # init empty data structs for return
    returnList = []
    returnDict = dict()
    
    # from data create return structure requests
    for key, value in channel.items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value['channel_name']
        # check channel details to see if member is there
        checkAccessDict = channel[key]['all_members'].keys()
        if  user_id_given_token(token) in checkAccessDict:
            # if token matches with a valid user_id in channel members,
            # add this channel info to list
            returnList.append(eachDict)

    # once channel list is created, package it up for return
    returnDict['channels'] = returnList
    
    # return in format specified
    return returnDict
    #### format for return ####
    # return {
    #     'channels': [
    #     	{
    #     		'channel_id': 1,
    #     		'name': 'My Channel',
    #     	}
    #     ],
    # }

def channels_listall(token):
    # raise ACCESS ERROR if token is invalid
    if is_valid_token(token) == False:
        raise AccessError("Token passed in is not valid")  
        
    returnList = []
    returnDict = dict()
    
    # from data create return structure requestes
    for key, value in channel.items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value
        returnList.append(eachDict)
    # For testing: print(returnList)

    # once channel list is created, package it up for return
    returnDict['channels'] = returnList

    return returnDict
    #### format for return ####
    # return {
    #     'channels': [
    #     	{
    #     		'channel_id': 1,
    #     		'name': 'My Channel',
    #     	}
    #     ],
    # }

def channels_create(token, name, is_public):
    # raise ACCESS ERROR if token is invalid
    if is_valid_token(token) == False:
        raise AccessError("Token passed in is not valid")   
    # Input error if channel name is too long
    if len(name) > 20:
        raise InputError("channel name cannot be greater than 20 characters")

    # get the current number of channels in total
    totalChannels = len(channel)
    newChannel_id = totalChannels + 1
    # if new channel id already a key in database,
    # increment until it is unique
    while newChannel_id in channel:
        newChannel_id += 1
    # create the channel: i.e add channel to the database
    # with token user as owner and member
    channel[newChannel_id] = {
        'channel_name' : name,
            'is_public' : is_public,
            'owner_members': {
                user_id_given_token(token) : True
            },
            'all_members' : {
                user_id_given_token(token) : True
            },
            'messages' : []
            
        }
    
    return {
        'channel_id': newChannel_id
    }
    #### format for return ####
    # return {
    #     'channel_id': newChannel_id
    # }

def is_valid_token(token):
    '''
    returns true or false if token, email, is in user database
    '''
    if token in tokens:
        return True
    return False

def user_id_given_token(token):
    '''
    returns the u_id if the user is in the database
    otherwise returns None if u_id is not found
    '''
    if token in users:
        user_id = users[token]['u_id']
        return user_id
    return None
