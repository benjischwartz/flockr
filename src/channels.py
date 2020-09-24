# import data.py from parent folder
import data

def channels_list(token):
    
    returnList = []
    returnDict = dict()
    
    # from data create return structure requestes
    for key, value in data.data['channels'].items():
        eachDict = dict()
        eachDict['channel_id'] = key
        eachDict['name'] = value
        returnList.append(eachDict)

    # once channel list is created, package it up for return
    returnDict['channels'] = returnList
    
    # return in format specified
    return returnDict

    #TODO when requirement is released, check token given is a valid string
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
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    ## start testing exceptions
    numChannelsbefore = len(channels_listall("randtoken"))
    ## do something to actually create channel
    numChannelsafter = len(channels_listall("randtoken"))
    if (numChannelsbefore != numChannelsafter - 1):
        raise Exception(f"Error, channel create does not actually add a new channel to total")
    ## end testing exceptions
    return {
        'channel_id': 1,
    }
