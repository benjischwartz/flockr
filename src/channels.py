# import data.py from parent folder
from data import channels
from channel import channel_details
from error import InputError


def channels_list(token):
    # init empty data structs for return
    returnList = []
    returnDict = dict()
    
    # from data create return structure requests
    for key, value in channels.items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value
        #TODO restrict view to channels only user has
        # assumption for now: token == u_id
        # call channel_details to check which channels
        # this user is a part of
        checkAccessDict = channel_details(token, key)
        if token in checkAccessDict['all_members']:
            ## TODO match with channel data structure
            # if token matches with a valid id, add to list
            returnList.append(eachDict)

    # once channel list is created, package it up for return
    returnDict['channels'] = returnList
    
    # return in format specified
    return returnDict

    
    ### below return is source suggested format
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
        
    returnList = []
    returnDict = dict()
    
    # from data create return structure requestes
    for key, value in channels.items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value
        returnList.append(eachDict)

    # once channel list is created, package it up for return
    returnDict['channels'] = returnList
    
    # return in format specified
    return returnDict
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    ## Input error if channel name is too long
    if len(name) > 20:
        raise InputError("channel name cannot be greater than 20 characters")


    
    ## get the next channel_id value and add to channels dict
    numChannelsbefore = channels['totalChannels']
    newChannel_id = channels['totalChannels'] + 1
    channels[newChannel_id] = name
    channels['totalChannels'] += 1
    numChannelsafter = channels['totalChannels']
    if (numChannelsbefore != numChannelsafter - 1):
        raise Exception(f"Error, channel create does not actually add a new channel to total")
        return
    ## end testing exceptions
    else: 
        return {
            'channel_id': newChannel_id,
        }

    
    
