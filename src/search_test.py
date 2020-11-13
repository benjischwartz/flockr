from search import search
from other import clear
import error
import pytest
from channels import channels_create, channels_list
from channel import channel_join
from auth import auth_register
from message import message_send, message_react

# test for Access Error and Invalid Token
def test_access_error():
    clear()
    with pytest.raises(error.AccessError):
        search("invalid@token.com.au","this is the query string")

# test for positive case, single message, single channel
def test_single_channel_single_message():
    clear()
    # register user and create public channel
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    # create a single message in the channel
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    # check one message is matched
    assert len(search(user_one['token'], "this is")['messages']) == 1, "does not return expected number of messages"
    assert len(search(user_one['token'], "this is a message")['messages']) == 1, "does not return expected number of messages"
    assert search(user_one['token'], "is")['messages'][0]['message_id'] == 1 
    assert search(user_one['token'], "is")['messages'][0]['message'] == "this is a message"     

# test where search query matches in channel user NOT part of
# expect this message is not in the return of search()
def test_pattern_match_unavailable_channel():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    user_two = auth_register("second@user.com", "password", "Joe", "Bloggs")
    new_channel = channels_create(user_two['token'],"channel_one", True)
    message_send(user_two['token'], new_channel['channel_id'], "this is a message")
    # return empty dictionary as there is no match
    assert search(user_one['token'], "this is")['messages'] == []

# test expecting multiple string matches in same channel
def test_single_channel_multiple_matches():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    user_two = auth_register("second@user.com", "password", "Jane", "Applebaum")
    new_channel_one = channels_create(user_one['token'],"channel_one", True)
    channel_join(user_two['token'], new_channel_one['channel_id'])
    message_send(user_one['token'], new_channel_one['channel_id'], "this is a message")
    message_send(user_one['token'], new_channel_one['channel_id'], "this is another message")
    message_react(user_one['token'], 1, 1)
    assert len(search(user_one['token'], "is")['messages']) == 2 
    assert search(user_one['token'], "is")['messages'][0]['message_id'] == 1 
    assert search(user_one['token'], "is")['messages'][1]['message_id'] == 2
    assert search(user_one['token'], "is")['messages'][0]['message'] == "this is a message"     
    assert search(user_one['token'], "is")['messages'][1]['message'] == "this is another message"
    assert search(user_one['token'], "is")['messages'][0]['reacts'] == [{
        'react_id' : 1,
        'u_ids': [1],
        'is_this_user_reacted': True
    }]
    assert search(user_two['token'], "is")['messages'][0]['reacts'] == [{
        'react_id' : 1,
        'u_ids': [1],
        'is_this_user_reacted': False
    }]
    

# test expecting multiple string matches in different channels: both public
def test_multiple_channel_multiple_matches():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel_one = channels_create(user_one['token'],"channel_one", True)
    new_channel_two = channels_create(user_one['token'],"channel_two", True)
    message_send(user_one['token'], new_channel_one['channel_id'], "this is a message")
    message_send(user_one['token'], new_channel_two['channel_id'], "this is another message")
    assert len(search(user_one['token'], "is")['messages']) == 2
    assert search(user_one['token'], "is")['messages'][0]['message_id'] == 1 
    assert search(user_one['token'], "is")['messages'][1]['message_id'] == 2
    assert search(user_one['token'], "is")['messages'][0]['message'] == "this is a message"     
    assert search(user_one['token'], "is")['messages'][1]['message'] == "this is another message"
    assert search(user_one['token'], "is")['messages'][0]['message'] == "this is a message"     


# test no matches with query string not found
def test_no_matches():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    assert search(user_one['token'], "robin")['messages'] == []
    

# test query > 1000 characters returns {}
def test_long_query():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    message_long = 'a'*1001
    assert search(user_one['token'], message_long)['messages'] == []
