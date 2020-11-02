from check_token import user_id_given_token
from error import AccessError
from channels import channels_list
from channel import channel_messages
from data import channel

def search(token, query_string):
    '''
    Returns the messages in the channel the user is a part of, which 
    contain the query string
 
    Parameters:
        token (str): refers to a valid user on flockr; this user is the inviter
        query_string (str): the pattern string which is being searched for
 
    Returns:
        (list): {messages}
    '''
    if user_id_given_token(token) == None:
        raise(AccessError) 
    # init results
    result = []

    # for each channel user is a member of
    for each in channels_list(token)['channels']:
        # use Python's in operator: if True, there is pattern match
        channel_id = each['channel_id']
        messages = channel[channel_id]['messages']
        for message in messages:
            # if there is match, append to result
            if query_string in message.get('message', None) != None:
                result.append(message) 
    # return result
    return {'messages' : result}

        #### format for return ####
    # 
    # [
#       {
#           'message_id': 1,
#           'u_id': 1,
#           'message': 'Hello world',
#           'time_created': 1582426789,
#       },
#       {
#           'message_id': 2,
#           'u_id': 1,
#           'message': 'Hello again',
#           'time_created': 1582426799,
#       }
    # ]
    # 

