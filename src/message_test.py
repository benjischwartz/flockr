import pytest
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join, channel_leave
from channels import channels_create
from message import message_send, message_remove, message_edit, message_sendlater, message_react, message_unreact
from error import InputError, AccessError
from other import clear
from time import time


# tests for message_send

def test_message_send_valid_input_multiple_messages():
    '''
    check that message_send returns the correct dictionary and unique message_ids starting
    from 1 and incrementing by 1 for each subsequent message as per the assumption
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 3}


def test_message_send_valid_input_multiple_channels():
    '''
    check that message_send returns the correct dictionary with unique message_ids 
    even if there are multiple channels in flockr
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_two = channels_create(user_one['token'], 'channel_two', True)
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(user_one['token'], channel_two['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 3}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    channel_two_messages = channel_messages(user_one['token'], channel_two['channel_id'],0)
    assert len(channel_one_messages['messages']) == 2
    assert len(channel_two_messages['messages']) == 1

def test_message_send_unique_id_after_remove():
    '''
    check that message_send returns unique message_ids even if a message is 
    removed
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_one = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_two = message_send(user_one['token'], channel_one['channel_id'], 'Hello') 
    message_remove(user_one['token'], message_one['message_id'])
    message_three = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    assert message_three['message_id'] != message_two['message_id']
    
def test_message_send_valid_input_time_created():
    '''
    check that message_send creates a time_created property for the message based
    on when message_send is called
    ''' 
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    prior_send = time()
    for _ in range(3):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    after_send = time()
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    oldest = channel_one_messages['messages'][2]['time_created']
    middle = channel_one_messages['messages'][1]['time_created'] 
    most_recent = channel_one_messages['messages'][0]['time_created'] 
    assert after_send > most_recent > middle > oldest > prior_send
    assert channel_one_messages['start'] == 0
    assert channel_one_messages['end'] == -1

def test_message_send_valid_input_5_chars():
    '''
    check a message of 5 characters is sent successfully
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id': 1}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert len(channel_one_messages['messages']) == 1
    assert channel_one_messages['messages'][0]['message_id'] == 1
    assert channel_one_messages['messages'][0]['u_id'] == user_one['u_id']
    assert channel_one_messages['messages'][0]['message'] == 'Hello'
    assert channel_one_messages['messages'][0]['reacts'] == []
    assert channel_one_messages['messages'][0]['is_pinned'] == False


def test_message_send_valid_input_1000_chars():
    '''
    check a message of 1000 characters is successfully sent
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_long = 'a'*1000
    assert message_send(user_one['token'], channel_one['channel_id'], message_long) == {'message_id': 1}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    assert channel_one_messages['messages'][0]['message_id'] == 1
    assert channel_one_messages['messages'][0]['u_id'] == user_one['u_id']
    assert channel_one_messages['messages'][0]['message'] == message_long
    assert channel_one_messages['messages'][0]['reacts'] == []
    assert channel_one_messages['messages'][0]['is_pinned'] == False


def test_message_send_empty_message():
    '''
    check an inputerror is raised if the the input 'message' is an empty string
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    with pytest.raises(InputError):
         message_send(user_one['token'], channel_one['channel_id'], '')
                 

def test_message_send_1001_characters():
    '''
    check an inputerror is raised if the message is greater than 1000 characters
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one= channels_create(user_one['token'], 'channel_one', True)
    message_long = 'a'*1001
    with pytest.raises(InputError):
        message_send(user_one['token'], channel_one['channel_id'], message_long)


def test_message_send_invalid_token():
    '''
    check an accesserror is raised when the token is not valid
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')


def test_message_send_user_not_in_channel():
    '''
    check an an accesserror is raised if the user is not in channel and tries to 
    send a message
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    with pytest.raises(AccessError):
        message_send(user_two['token'], channel_one['channel_id'], 'Hello')


def test_message_send_invalid_channel_id():
    '''
    check an inputerror is raised if the channel_id is invalid; in this test any 
    channel_id is invalid since no channels exist
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        message_send(user_one['token'], 0, 'Hello')


# tests for message_remove


def test_message_remove_valid_channel_member():
    '''
    check message_remove removes the message if the user calling it is the user 
    who sent the message originally
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    assert message_remove(user_two['token'], rand_message['message_id']) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages == {'messages': [], 'start': 0, 'end': -1}


def test_message_remove_valid_channel_owner():
    '''
    check message_remove removes the message if the user calling it is the 
    owner of the channel 
    '''
    
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    user_three = auth_register('thirduser@gmail.com', '456abc!@#', 'Third', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    channel_join(user_three['token'], channel_one['channel_id'])
    rand_message = message_send(user_three['token'], channel_one['channel_id'], 'Hello')
    assert message_remove(user_two['token'], rand_message['message_id']) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages == {'messages': [], 'start': 0, 'end': -1}


def test_message_remove_valid_flockr_owner():
    '''
    check message_remove removes the message if the user calling it is an owner of
    flockr
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    channel_join(user_one['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    assert message_remove(user_one['token'], rand_message['message_id']) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages == {'messages': [], 'start': 0, 'end': -1}


def test_message_remove_valid_input_multiple_messages_remove_middle():
    '''
    check message_remove removes the correct message if there are multiple 
    messages in the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    for _ in range(3):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    for _ in range(3):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages_init = channel_messages(user_one['token'], channel_one['channel_id'],0)    
    assert message_remove(user_one['token'], rand_message['message_id']) == {}
    channel_one_messages_after = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert len(channel_one_messages_after['messages']) == len(channel_one_messages_init['messages']) - 1
    for k in range(len(channel_one_messages_after['messages'])):
        assert channel_one_messages_after['messages'][k]['message_id'] != rand_message['message_id']

#TODO: Check coz you switched this from accesserror to inputerror
def test_message_remove_invalid_flockr_owner():
    '''
    check an inputerror is raised if an owner of flockr tries to remove a message 
    from a channel they are not a member of
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    with pytest.raises(InputError):
        message_remove(user_one['token'], rand_message['message_id'])
        
#TODO: Check coz you switched this from accesserror to inputerror
def test_message_remove_user_not_part_of_channel():
    '''
    check an inputerror is raised when the user that sent the message has left 
    the channel and is trying to delete the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_two['token'], channel_one['channel_id'])
    with pytest.raises(InputError):
        message_remove(user_two['token'], rand_message['message_id'])
   

def test_message_remove_invalid_token():
    '''
    check an accesserror is raised when token is not valid
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_remove(user_one['token'], rand_message['message_id'])


def test_message_remove_not_authorised_to_remove():
    '''
    check an accesserror is raised when the user trying to delete is neither the 
    user who sent the message, nor the owner of flockr nor a channel owner
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_remove(user_two['token'], message['message_id'])



def test_message_remove_already_deleted():
    '''
    check an inputerror is raised when the message being removed has already been
    deleted i.e message_id is invalid 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    # first delete of the message should be successful
    assert message_remove(user_one['token'], rand_message['message_id']) == {}
    with pytest.raises(InputError):
        message_remove(user_one['token'], rand_message['message_id'])


# tests for message_edit


def test_message_edit_valid_input_channel_member():
    '''
    check message_edits edits the message if the user calling it is the user who
    sent the message originally
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages_init = channel_messages(user_two['token'], channel_one['channel_id'], 0)
    message_edit(user_two['token'], rand_message['message_id'], 'Hello World') == {}
    channel_one_messages_after = channel_messages(user_two['token'], channel_one['channel_id'], 0)
    assert channel_one_messages_after == { 
        'messages': [{
            'message_id': channel_one_messages_init['messages'][0]['message_id'],
            'u_id': channel_one_messages_init['messages'][0]['u_id'],
            'message' : 'Hello World',
            'time_created' : channel_one_messages_init['messages'][0]['time_created'],
            'reacts' : [],
            'is_pinned' : False
        }],
        'start' : 0,
        'end': -1
    }

def test_message_edit_valid_input_channel_owner():
    '''
    check message_edit edits the message if the user calling it is the owner of 
    the channel 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    channel_join(user_one['token'], channel_one['channel_id'])
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages_init = channel_messages(user_two['token'], channel_one['channel_id'], 0)
    assert message_edit(user_two['token'],rand_message['message_id'], 'Hello World') == {}
    channel_one_messages_after = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages_after == { 
        'messages': [{
            'message_id': channel_one_messages_init['messages'][0]['message_id'],
            'u_id': channel_one_messages_init['messages'][0]['u_id'],
            'message' : 'Hello World',
            'time_created' : channel_one_messages_init['messages'][0]['time_created'],
            'reacts' : [],
            'is_pinned' : False
        }],
        'start' : 0,
        'end': -1
    }


def test_message_edit_valid_input_flockr_owner():
    '''
    check message_edit edits the message if the user calling it is an owner of 
    flockr 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    channel_join(user_one['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages_init = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    assert message_edit(user_one['token'],rand_message['message_id'], 'Hello World') == {}
    channel_one_messages_after = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages_after == { 
        'messages': [{
            'message_id': channel_one_messages_init['messages'][0]['message_id'],
            'u_id': channel_one_messages_init['messages'][0]['u_id'],
            'message' : 'Hello World',
            'time_created' : channel_one_messages_init['messages'][0]['time_created'],
            'reacts' : [],
            'is_pinned' : False
        }],
        'start' : 0,
        'end': -1
    }

 
def test_message_edit_valid_input_multiple_messages_edit_middle():
    '''
    check message_edit edits the correct message if there are multiple 
    messages in the channel   
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi2')
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi3')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi4')
    assert message_edit(user_one['token'],rand_message['message_id'], 'Hello World') == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][1]['message'] == 'Hello World'


def test_message_edit_valid_input_empty_string():
    '''
    check message_edit removes a messsage if the input 'message' is an empty
    string
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    assert message_edit(user_one['token'],rand_message['message_id'], '') == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages == {'messages': [], 'start': 0, 'end': -1}
  

def test_message_edit_valid_input_1000_characters():
    '''
    check message_edit successfully edits the message if the message is 1000
    characters long
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages_init = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    message_long = 'a'*1000
    assert message_edit(user_one['token'], rand_message['message_id'], message_long) == {}
    channel_one_messages_after = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages_after == { 
        'messages': [{
            'message_id': channel_one_messages_init['messages'][0]['message_id'],
            'u_id': channel_one_messages_init['messages'][0]['u_id'],
            'message' : message_long,
            'time_created' : channel_one_messages_init['messages'][0]['time_created'],
            'reacts' : [],
            'is_pinned' : False
        }],
        'start': 0,
        'end': -1
    }


def test_message_edit_1001_characters():
    '''
    check an inputerror is raised if the message is greater than 1000 characters
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_long = 'a'*1001
    with pytest.raises(InputError):
        message_edit(user_one['token'], rand_message['message_id'], message_long)

 
def test_message_edit_invalid_message_id_no_messages():
    '''
    check an inputerror is raised if the message_id is invalid (eg. it has been
    deleted)
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_remove(user_one['token'], rand_message['message_id'])
    with pytest.raises(InputError):
        message_edit(user_one['token'], rand_message['message_id'], 'Hello World')


def test_message_edit_invalid_token():
    '''
    check an accesserror is raised when the token is not valid 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_edit(user_one['token'], rand_message['message_id'], 'Hello World')

 
def test_message_edit_not_authorised_to_remove():
    '''
    check an accesserror is raised when the user trying to delete is neither the 
    user who sent the message, nor the owner of flockr nor a channel owner
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_edit(user_two['token'], rand_message['message_id'], 'Hello World')   

#TODO: Check coz you switched this from accesserror to inputerror
def test_message_edit_user_not_part_of_channel():
    '''
    check an inputerror is raised if a user tries to edit a message but they 
    have left the channel and are thus not a member of it anymore
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_two['token'], channel_one['channel_id'])
    with pytest.raises(InputError):
        message_edit(user_two['token'], rand_message['message_id'], 'Hello World')   

#TODO: Check coz you switched this from accesserror to inputerror
def test_message_edit_invalid_flockr_owner():
    '''
    check an accesserror is raised if an owner of flockr tries to edit a message 
    of a channel they are not a member of
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    with pytest.raises(InputError):
        message_edit(user_one['token'],rand_message['message_id'], 'Hello World')



# tests for message_sendlater

def test_message_sendlater_valid_input_multiple_messages():
    '''
    check that message_send returns the correct dictionary and unique message_ids starting
    from 1 and incrementing by 1 for each subsequent message as per the assumption
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() + 3600
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 1}
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 2}
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 3}


def test_message_sendlater_valid_input_multiple_channels():
    '''
    check that message_send returns the correct dictionary with unique message_ids 
    even if there are multiple channels in flockr
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_two = channels_create(user_one['token'], 'channel_two', True)
    sending_time = time() + 3600
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 1}
    assert message_sendlater(user_one['token'], channel_two['channel_id'], 'Hello', sending_time) == {'message_id': 2}
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 3}

def test_message_sendlater_unique_id_with_message_send():
    '''
    check a message of 1000 characters is successfully sent
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    assert message_send(user_one['token'], channel_one['channel_id'], 'Hello') == {'message_id' : 1}
    message_long = 'a'*1000
    sending_time = time() + 3600
    assert message_sendlater(user_one['token'], channel_one['channel_id'], message_long, sending_time) == {'message_id': 2}
 
def test_message_sendlater_unique_id_after_remove():
    '''
    check that message_send returns unique message_ids even if a message is 
    removed
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() + 3600
    message_one = message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time)
    message_two = message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) 
    message_remove(user_one['token'], message_one['message_id'])
    message_three = message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time)
    assert message_three['message_id'] != message_two['message_id']

    
def test_channel_sendlater_valid_input_time_created():
    '''
    check that message_send creates a time_created property for the message based
    on when message_send is called
    ''' 
    
    #TODO: maintenance testing
    # OR could create a function that gives the details of any message regardless of time_created
    pass
    

def test_message_sendlater_valid_input_5_chars():
    '''
    check a message of 5 characters is sent successfully
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() + 3600
    assert message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time) == {'message_id': 1}
    # manual testing done with frontend to check message actually gets sent

def test_message_sendlater_valid_input_1000_chars():
    '''
    check a message of 1000 characters is successfully sent
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_long = 'a'*1000
    sending_time = time() + 3600
    assert message_sendlater(user_one['token'], channel_one['channel_id'], message_long, sending_time) == {'message_id': 1}
    # manual testing done with frontend to check message actually gets sent


def test_message_sendlater_invalid_time():
    '''
    check an inputerror is raised if the time send is a time in the past
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() - 3600
    with pytest.raises(InputError):
         message_sendlater(user_one['token'], channel_one['channel_id'], '', sending_time)
         
def test_message_sendlater_empty_message():
    '''
    check an inputerror is raised if the the input 'message' is an empty string
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() + 3600
    with pytest.raises(InputError):
         message_sendlater(user_one['token'], channel_one['channel_id'], '', sending_time)
                 

def test_message_sendlater_1001_characters():
    '''
    check an inputerror is raised if the message is greater than 1000 characters
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one= channels_create(user_one['token'], 'channel_one', True)
    message_long = 'a'*1001
    sending_time = time() + 3600
    with pytest.raises(InputError):
        message_sendlater(user_one['token'], channel_one['channel_id'], message_long, sending_time)


def test_message_sendlater_invalid_token():
    '''
    check an accesserror is raised when the token is not valid
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    auth_logout(user_one['token'])
    sending_time = time() + 3600
    with pytest.raises(AccessError):
        message_sendlater(user_one['token'], channel_one['channel_id'], 'Hello', sending_time)


def test_message_sendlater_user_not_in_channel():
    '''
    check an an accesserror is raised if the user is not in channel and tries to 
    send a message
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    sending_time = time() + 3600
    with pytest.raises(AccessError):
        message_sendlater(user_two['token'], channel_one['channel_id'], 'Hello', sending_time)


def test_message_sendlater_invalid_channel_id():
    '''
    check an inputerror is raised if the channel_id is invalid; in this test any 
    channel_id is invalid since no channels exist
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    sending_time = time() + 3600
    with pytest.raises(InputError):
        message_sendlater(user_one['token'], 0, 'Hello', sending_time)
        
# tests for message_react

def test_message_react_valid_input_user_reacted_true():
    '''
    check that a message has been reacted to successfully given a react_id of 1
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_react(user_one['token'], 1, 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['reacts'][0] == {
        'react_id' : 1,
        'u_ids' : [1],
        'is_this_user_reacted' : True
    }
        

def test_message_react_valid_input_user_reacted_false():
    '''
    check that when a channel message has multiple users, only the user who 
    reacts is added to the list ['u_ids']
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '123abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_react(user_one['token'], 1, 1) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['reacts'][0] == {
        'react_id' : 1,
        'u_ids' : [1],
        'is_this_user_reacted' : False
    }
        


def test_message_react_valid_input_multiple_of_one_react():
    '''
    check that a message can be reacted to multiple times if the reacts are 
    done by different users
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '123abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_react(user_one['token'], 1, 1) == {}
    assert message_react(user_two['token'], 1, 1) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'], 0)
    assert channel_one_messages['messages'][0]['reacts'][0] == {
        'react_id' : 1,
        'u_ids' : [1, 2],
        'is_this_user_reacted' : True
    }
        

def test_message_react_valid_input_multiple_messages_react_middle():
    '''
    check message_react only adds a react to the specified message if there are 
    multiple messages in the channel   
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi2')
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi3')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi4')
    assert message_react(user_one['token'],rand_message['message_id'], 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['reacts'] == []
    assert channel_one_messages['messages'][2]['reacts'] == []
    assert channel_one_messages['messages'][1]['reacts'][0] == {
        'react_id' : 1,
        'u_ids' : [1],
        'is_this_user_reacted' : True
    }
                
        
def test_message_react_invalid_react_id():
    '''
    check an inputerror is raised when the react_id is invalid; valid react_ids
    are 1. 
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    with pytest.raises(InputError): 
        message_react(user_one['token'], 1, 1000)

def test_message_react_already_reacted():
    '''
    check that channel_messages raises an inputerror if the user has already
    reacted to the message 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_react(user_one['token'], 1, 1) == {}
    with pytest.raises(InputError): 
        message_react(user_one['token'], 1, 1)
        
        
def test_message_react_invalid_message_id():
    '''
    check an inputerror is raised if the message_id is invalid (eg. it has been
    deleted)
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_remove(user_one['token'], rand_message['message_id'])
    with pytest.raises(InputError):
        message_react(user_one['token'], rand_message['message_id'], 1)


def test_message_react_user_not_part_of_channel():
    '''
    check an inputerror is raised if a user tries to react to a message but they 
    have left the channel and are thus not a member of it anymore
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_one['token'], channel_one['channel_id'])
    with pytest.raises(InputError):
        message_react(user_one['token'], rand_message['message_id'], 1)   

def test_message_react_invalid_token():
    '''
    check an accesserror is raised when the token is not valid 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_react(user_one['token'], rand_message['message_id'], 1)


# tests for message_unreact


# reacts exist but reacts of the specified react_id (only if you implement more react_ids)

def test_message_unreact_valid_input_one_react():
    '''
    check that message_unreact successfully unreacts a message with one react
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_react(user_one['token'], 1, 1)
    assert message_unreact(user_one['token'], 1, 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['reacts'] == []
        

def test_message_unreact_valid_input_multiple_reacts_same_react_id():
    '''
    check that when a message has multiple reacts of the same react_id, 
    the correct user react gets removed
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '123abc!@#', 'Second', 'User')
    user_three = auth_register('thirduser@gmail.com', '123abc!@#', 'Third', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    channel_join(user_three['token'], channel_one['channel_id'])
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_react(user_one['token'], 1, 1)
    message_react(user_two['token'], 1, 1)
    message_react(user_three['token'], 1, 1)
    assert message_unreact(user_two['token'], 1, 1) == {}
    channel_one_messages = channel_messages(user_two['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['reacts'][0] == {
        'react_id' : 1,
        'u_ids' : [1, 3],
        'is_this_user_reacted' : False
    }
        


def test_message_unreact_valid_input_multiple_messages_react_middle():
    '''
    check message_react is able to unreact the correct message if there are 
    multiple messages in the channel   
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi2')
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi3')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi4')
    message_react(user_one['token'],rand_message['message_id'], 1)
    assert message_unreact(user_one['token'],rand_message['message_id'], 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][1]['reacts'] == []
                
        
def test_message_unreact_invalid_react_id():
    '''
    check an inputerror is raised when the react_id is invalid; valid react_ids
    are 1. 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_react(user_one['token'], 1, 1)
    with pytest.raises(InputError): 
        message_unreact(user_one['token'], rand_message['message_id'], 1000)


def test_message_unreact_no_reacts():
    '''
    check an inputerror is raised if there are no reacts on the message 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    with pytest.raises(InputError): 
        message_unreact(user_one['token'], rand_message['message_id'], 1)
        
def test_message_unreact_user_not_reacted():
    '''
    check an inputerror is raised if there are reactions for the message of the 
    appropriate react_id but the user who is trying to unreact, did not react
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '123abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_react(user_one['token'], 1, 1)
    with pytest.raises(InputError):
        message_unreact(user_two['token'], rand_message['message_id'], 1)
       
def test_message_unreact_invalid_message_id():
    '''
    check an inputerror is raised if the message_id is invalid (eg. it has been
    deleted)
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_remove(user_one['token'], rand_message['message_id'])
    with pytest.raises(InputError):
        message_unreact(user_one['token'], rand_message['message_id'], 1)


def test_message_unreact_user_not_part_of_channel():
    '''
    check an inputerror is raised if a user tries to unreact to a message but they 
    have left the channel and are thus not a member of it anymore
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_react(user_one['token'], rand_message['message_id'], 1)   
    channel_leave(user_one['token'], channel_one['channel_id'])
    with pytest.raises(InputError):
        message_unreact(user_one['token'], rand_message['message_id'], 1)   

def test_message_unreact_invalid_token():
    '''
    check an accesserror is raised when the token is not valid 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_react(user_one['token'], rand_message['message_id'], 1)   
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_unreact(user_one['token'], rand_message['message_id'], 1)


# tests for message_pin
def test_message_pin_valid_input_true():
    '''
    check that a message has been pinned successfully
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_pin(user_one['token'], 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['is_pinned'] is True
    
def test_message_pin_already_pinned():
    '''
    check that pinning a message that is already pinned raises an access error
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    assert message_pin(user_one['token'], 1) == {}
    with pytest.raises(InputError):
        message_pin(user_one['token'], 1)

def test_message_pin_multiple_messages():
    '''
    check message_pin only pints the specified message if there are 
    multiple messages in the channel   
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi2')
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hi3')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi4')
    assert message_pin(user_one['token'],rand_message['message_id']) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['is_pinned'] is False
    assert channel_one_messages['messages'][2]['is_pinned'] is False
    assert channel_one_messages['messages'][1]['is_pinned'] is True
        
        
def test_message_pin_invalid_message_id():
    '''
    check an inputerror is raised if the message_id is invalid (eg. it has been
    deleted)
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    message_remove(user_one['token'], rand_message['message_id'])
    with pytest.raises(InputError):
        message_pin(user_one['token'], rand_message['message_id'])


def test_message_react_user_not_part_of_channel():
    '''
    check an inputerror is raised if a user tries to react to a message but they 
    have left the channel and are thus not a member of it anymore
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_one['token'], channel_one['channel_id'])
    with pytest.raises(InputError):
        message_pin(user_one['token'], rand_message['message_id'])   

def test_message_react_invalid_token():
    '''
    check an accesserror is raised when the token is not valid 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    rand_message = message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        message_pin(user_one['token'], rand_message['message_id'])

# tests for message_unpin

def test_message_unpin_valid_input():
    '''
    check that message_unpin successfully unpins a message
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_pin(user_one['token'], 1)
    assert message_unpin(user_one['token'], 1) == {}
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)
    assert channel_one_messages['messages'][0]['is_pinned'] is False
        

def test_message_unpin_twice():
    '''
    check that unpinning a message that is unpinned
    raises an InputError
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_pin(user_one['token'], 1)
    message_unpin(user_one['token'], 1)
    with pytest.raises(InputError):
        message_unpin(user_one['token'], 1)
        


def test_message_unpin_valid_input_multiple_messages():
    '''
    check message_react is able to unpin the correct message if there are 
    multiple messages in the channel   
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')

    channel_one = channels_create(user_one['token'], 'channel_one', True)

    message_send(user_one['token'], channel_one['channel_id'], 'Hi')
    message_send(user_one['token'], channel_one['channel_id'], 'Hi2')


    rand_message1 = message_send(user_one['token'], channel_one['channel_id'], 'Hi3')
    rand_message2 = message_send(user_one['token'], channel_one['channel_id'], 'Hi4')

    message_pin(user_one['token'],rand_message1['message_id'])
    message_pin(user_one['token'],rand_message2['message_id'])

    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'],0)

    # assert channel_one_messages['messages'][1]['is_pinned'] is True
    # assert channel_one_messages['messages'][2]['is_pinned'] is True

    # assert message_unpin(user_one['token'],rand_message1['message_id']) == {}

    # assert channel_one_messages['messages'][1]['is_pinned'] is False
    # assert channel_one_messages['messages'][2]['is_pinned'] is False




