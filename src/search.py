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
    result = []

    # for email in users:
    #     if 'handle' in users[email].keys():
    #         if handle_str == users[email]['handle']:
    #             raise InputError("handle is already being used by another user.")

    # users[token]['handle'] = handle_str
    # for each channel user is a member of
    for each in channels_list(token)['channels']:
        # use Python's in operator: if True, there is pattern match
        channel_id = each['channel_id']
        messages = channel[channel_id]['messages']
        for message in messages:
            # if there is match, append to result
            if query_string in message.get('message_content', None) != None:
                result.append(message) 
            else:
                pass
    # return result
    return result

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

