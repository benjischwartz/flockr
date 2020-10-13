from check_token import user_id_given_token
from error import AccessError
from channels import channels_list
from channel import channel_messages
from data import channel

def search(token, query_string):
    """
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
    Return {messages}
    """
    # TODO: once token func written, change access error condition
    if user_id_given_token(token) == None:
        raise(AccessError) 
    # init results
    result = {}
    result['messages'] = []
    # for each channel user is a member of
    for each in channels_list(token):
        # use Python's in operator: if True, there is pattern match
        if query_string in channel[each]['channel_id']['messages']['message']:
            # if there is match, append to result
            result['messages'].append()
    # return result
    return result

        #### format for return ####
    # {
    # 'messages': [
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
    #   ]
    # }
