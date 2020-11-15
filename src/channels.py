from data import channel, users, tokens
from data_persistence import data_store
from error import InputError, AccessError
from check_token import user_id_given_token



def channels_list(token):
    '''
    Returns the channel ids and names of channel the user is a part of.
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
 
    Returns:
        (dict): {}
    '''
    # raise an accesserror if token is invalid
    if user_id_given_token(token) == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")  

    # create empty data structs for return
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
    '''
    Returns the channel ids and names of all channels, whether the user is a member or not.
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
 
    Returns:
        (dict): {}
    '''
    
    # raise an accesserror if token is invalid
    if user_id_given_token(token) == None:
        raise AccessError(description="Token passed in is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")  
        
    returnList = []
    returnDict = dict()
    
    # from data create return structure requestes
    for key, value in channel.items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value['channel_name']
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
    '''
    Creates a new channel, whether public or private according to input.
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
        name (str): the name of the channel itself; does not need to be uniques
        is_public (bool): True if the channel is public, otherwise False if private 
 
    Returns:
        (dict): {}
    '''

    # raise an accesserror if token is invalid
    if user_id_given_token(token) == None:
        raise AccessError(description="Token passed in is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")   
    
    # raise an inputerror if channel name is too long
    if len(name) > 20:
        raise InputError(description="Channel name cannot be greater than 20 characters.")

    # get the current number of channels in total
    totalChannels = len(channel)
    newChannel_id = totalChannels + 1
    
    ### Uncomment only if we add the ability to delete a channel later ###
    # # if new channel id already a key in database,
    # # increment until it is unique
    # while newChannel_id in channel:
    #     newChannel_id += 1
        
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
    
    data_store()
    return {
        'channel_id': newChannel_id
    }
    #### format for return ####
    # return {
    #     'channel_id': newChannel_id
    # }

