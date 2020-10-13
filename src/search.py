from check_token import user_id_given_token
from error import AccessError

def search(token, query_string):
    """
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
    Return {messages}
    """
    if user_id_given_token(token) == None:
        raise(AccessError) 
    # TODO: change return
    return {}