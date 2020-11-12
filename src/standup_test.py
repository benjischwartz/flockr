import pytest
import data
from auth import auth_register, auth_logout
from channel import channel_invite, channel_details, channel_messages
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create, channels_listall
from error import InputError, AccessError
from standup import standup_start, standup_active, standup_send
from other import clear
from message import message_send

def test_standup_start_positive():
    '''
    A positive test case for standup_start function.
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    standup_start(user_one['token'], channel_one['channel_id'], 10)

    assert standup_active(user_one['token'], channel_one['channel_id'])['is_active'] == True

def test_standup_start_invalid_channel():
    ''' 
    check an inputerror is raised if the channel_id is invalid; in this test any 
    channel_id is invalid since no channels exist
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        standup_start(user_one['token'], 0, 10)

def test_standup_start_already_running():
    '''
    check an inputerror is raised if the an active standup is currently
    running in this channel
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    standup_start(user_one['token'], channel_one['channel_id'], 10)
    with pytest.raises(InputError):
        standup_start(user_one['token'], channel_one['channel_id'], 10)

def test_standup_start_invalid_token():
    '''
    check if the token enter is valid raise access error otherwiser
    '''
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'First', 'Last')
    channel_one = channels_create(user['token'], 'userchannel', True)
    auth_logout(user['token'])
    with pytest.raises(AccessError):
        standup_start(user['token'], channel_one['channel_id'], 10)

def test_standup_active_invalid_channel_id():
    '''
    check an inputerror is raised if the channel_id is invalid; in this test any 
    channel_id is invalid since no channels exist
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        standup_active(user_one['token'], 0)

def test_standup_active_invalid_token():
    '''
    check if the token enter is valid raise access error otherwiser
    '''
    clear()
    user_one = auth_register('user@gmail.com', '123abc!@#', 'First', 'Last')
    channel_one = channels_create(user_one['token'], 'userchannel', True)
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        standup_active(user_one['token'], channel_one['channel_id'])

def test_standup_send_invalid_channel_id():
    '''
    check an inputerror is raised if the channel_id is invalid; in this test any 
    channel_id is invalid since no channels exist
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    message = 'hi'
    with pytest.raises(InputError):
        standup_send(user_one['token'], 0, message)

def test_standup_send_message_too_long():
    '''
    check an inputerror is raised if the message is greater than 1000 characters
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message_long = 'a'*1001
    standup_start(user_one['token'], channel_one['channel_id'], 10)
    with pytest.raises(InputError):
        standup_send(user_one['token'], channel_one['channel_id'], message_long)

def test_standup_send_message_no_standup_running():
    '''
    check an inputerror is raised if there's no standup running in the server
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message = 'hi'
    with pytest.raises(InputError):
        standup_send(user_one['token'], channel_one['channel_id'], message)

def test_standup_send_unauthorised_user():
    '''
    check an accesserror os raosed if a person who is not in the channel tries
    to send a message
    '''
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    message = 'hi'
    with pytest.raises(AccessError):
        standup_send(user_two['token'], channel_one['channel_id'], message)
