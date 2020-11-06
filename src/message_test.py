import pytest
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join, channel_leave
from channels import channels_create
from message import message_send, message_remove, message_edit
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
    
def test_channel_send_valid_input_time_created():
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
    prior_send = time()
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
    prior_send = time()
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


def test_message_remove_invalid_flockr_owner():
    '''
    check an accesserror is raised if an owner of flockr tries to remove a message 
    from a channel they are not a member of
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_two['token'], 'channel_one', True)
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_remove(user_one['token'], rand_message['message_id'])
        

def test_message_remove_user_not_part_of_channel():
    '''
    check an accesserror is raised when the user that sent the message has left 
    the channel and is trying to delete the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_two['token'], channel_one['channel_id'])
    with pytest.raises(AccessError):
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


def test_message_edit_user_not_part_of_channel():
    '''
    check an accesserror is raised if a user tries to edit a message but they 
    have left the channel and are thus not a member of it anymore
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    rand_message = message_send(user_two['token'], channel_one['channel_id'], 'Hello')
    channel_leave(user_two['token'], channel_one['channel_id'])
    with pytest.raises(AccessError):
        message_edit(user_two['token'], rand_message['message_id'], 'Hello World')   

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
    with pytest.raises(AccessError):
        message_edit(user_one['token'],rand_message['message_id'], 'Hello World')


