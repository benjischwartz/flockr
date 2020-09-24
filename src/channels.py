def channels_list(token):
    #TODO check token given is a valid string
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
