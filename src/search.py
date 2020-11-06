from check_token import user_id_given_token
from error import AccessError
from channels import channels_list
from channel import channel_messages
from data import channel

def search(token, query_string):
    """
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
    Returns:
        (dict): {
            'messages': [
               {
                   'message_id': 1,
                   'u_id': 1,
                   'message': 'Hello world',
                   'time_created': 1582426789,
                   'reacts' : [
                        {
                            'react_id' : 1
                            'u_ids' : [2, 3]
                            'is_this_user_reacted' : False
                        }
                    'is_pinned' : False
           ],
       }
    """
    
    if user_id_given_token(token) == None:
        raise(AccessError) 
    
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

    return {'messages' : result}


