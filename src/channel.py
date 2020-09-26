from data import channel, users


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
    # channel; if not raise an accesserror is raised if the
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
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }
