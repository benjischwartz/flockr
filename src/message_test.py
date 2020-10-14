import pytest
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join, channel_leave
from channels import channels_create
from message import message_send, message_remove, message_edit
from error import InputError, AccessError
from other import clear


# tests for message_send
# valid input tests
    # a member of the channel sending a message
    
    # 1000 characters - should add the message in - check 
# invalid tests
    # accesserror if token is invalid - check
    # inputerror for message too long - check
    # ASSUMPTION raise an inputerror for message of 0 charachters - empty string
        # (case won't be tested according to forum)
    # accesserror if user not in the channel - check 
    # ASSUMPTION: inputerror if the channel_id is invalid     


# raise an inputerror if time_created that is returned in messages is a valid time object

def test_message_send_valid_multiple_messages():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 3}


def test_message_send_valid_multiple_channels():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel1 = channels_create(userOne['token'], 'randChannel1', True)
    randChannel2 = channels_create(userOne['token'], 'randChannel2', True)
    assert message_send(userOne['token'], randChannel1['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(userOne['token'], randChannel2['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(userOne['token'], randChannel1['channel_id'], 'Hello') == {'message_id': 3}

def test_message_send_valid_input_5_chars():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    # TODO: add channel_messages
    all_messages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert len(all_messages['messages']) == 1

def test_message_send_valid_input_1000_chars():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    # create a message that is 1000 characters long
    message_long = 'a'
    for i in range(999):
        message_long  += 'a'
        i += 1
    assert message_send(userOne['token'], randChannel['channel_id'], message_long) == {'message_id': 1}
    # TODO: add channel_messages
    
# TEST MAYBE UNNECESSART FOR MESSAGE_SEND
def test_message_send_valid_channel_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    assert message_send(userTwo['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    # TODO: add channel_messages

# TEST MAYBE UNNECESSARY FOR MESSAGE_SEND
def test_message_send_owner_of_flockr():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userOne['token'], randChannel['channel_id'])
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    # TODO: add channel_messages

# check an accesserror is raised when token is not valid
def test_message_send_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')

# raise an inputerror if the the input 'message' is an empty string
def test_message_send_empty_message():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(InputError):
         message_send(userOne['token'], randChannel['channel_id'], '') == {}
                 
# raise an inputerror if the message is greater than 1000 characters
def test_message_send_over_1000_characters():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel= channels_create(userOne['token'], 'randChannel', True)
    # create a message that is 1001 characters lon
    message_long = 'a'
    for i in range(1000):
        message_long  += 'a'
        i += 1
    with pytest.raises(InputError):
        message_send(userOne['token'], randChannel['channel_id'], message_long)

# raise an accesserror if user is not in channel and tries to send a message
def test_message_send_user_not_in_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        message_send(userTwo['token'], randChannel['channel_id'], 'Hello')


# ASSUMPTION: inputerror if the channel_id is invalid; in this test any number
# is invalid since no channels exist?
def test_message_send_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        message_send(userOne['token'], 0, 'Hello')

# tests for message_remove


# valid tests
    # user who created deletes
    # channel owner (not flockr owner)
    # owner of flockr deletes 
        # assumption is that the owner of flockr still needs to be part of the channel (but they can be a member only)
# inputerror
    # message_id doesnt exist (already deleted)
    # no messages were even created
# accesserror 
    # a normal member (not the member that sent the channel, nor owner of flockr or a channel_owner) tries to delete the message
    # token is invalid
    # ASSUMPTION accesserror: someone not in the channel at all is trying to delete a message eg. they sent the message but left the channel 
    # ASSUMPTION owner of flockr tries to delete but they arent a member of the channel

# assumption: must be a member of the channel to use message_remove
    # relevant to the owner of flockr removing (can't remove if not in channel)
    # relevant to the original person who sent the message (if they left the channel 
    # they cannot remove the message)


# check message_remove works if the user calling it is the user who sent the 
# message originally and is also just a regular member of flockr and the channel
def test_message_remove_valid_channel_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    message = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    all_messages_init = channel_messages(userTwo['token'], randChannel['channel_id'],0)    
    assert len(all_messages_init['messages']) == 1
    message_remove(userTwo['token'],message['message_id'])
    all_messages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert all_messages == {'messages': [], 'start': 0, 'end': -1}

# check message remove works if the user calling it is the owner of the channel
# (and is also not the owener of flockr and not the person who sent the message originally)
def test_message_remove_valid_channel_owner():
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '456abc!@#', 'Third', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userThree['token'], randChannel['channel_id'])
    message = message_send(userThree['token'], randChannel['channel_id'], 'Hello')
    all_messages_init = channel_messages(userTwo['token'], randChannel['channel_id'],0)    
    assert len(all_messages_init['messages']) == 1
    message_remove(userTwo['token'],message['message_id'])
    all_messages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert all_messages == {'messages': [], 'start': 0, 'end': -1}

# check message remove works if the user calling it is the owner of Flockr
# (and not the owner of the channel and not the person who sent the message originally)
def test_message_remove_valid_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userOne['token'], randChannel['channel_id'])
    message = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    all_messages_init = channel_messages(userTwo['token'], randChannel['channel_id'],0)    
    assert len(all_messages_init['messages']) == 1
    message_remove(userOne['token'],message['message_id'])
    all_messages_after = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert all_messages_after == {'messages': [], 'start': 0, 'end': -1}


# raise an accesserror if the owner of flockr tries to delete a message but they 
# are not a member of the channel 
def test_message_remove_invalid_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    message = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    all_messages_init = channel_messages(userTwo['token'], randChannel['channel_id'],0)    
    with pytest.raises(AccessError):
        message_remove(userOne['token'],message['message_id'])

# check an accesserror is raised when the user that sent the message has left 
# the channel and is trying to delete the channel
def test_message_remove_user_not_part_of_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    message = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    channel_leave(userTwo['token'], randChannel['channel_id'])
    with pytest.raises(AccessError):
        message_remove(userTwo['token'],message['message_id'])
   
# check an accesserror is raised when token is not valid
def test_message_remove_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    message = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_remove(userOne['token'], message['message_id'])

# raise an accesserror when the user trying to delete is neither the user who
# sent the message, nor the owner of flockr nor a channel owner
def test_message_remove_not_authorised_to_remove():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    message = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_remove(userTwo['token'], message['message_id'])

# check an inputerror is raised if there are no messages i.e message id is invalid
def test_message_remove_no_messages():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    with pytest.raises(InputError):
        message_remove(userOne['token'], 0)

# check an inputerror is raised when the message being removed has already been
# deleted
def test_message_remove_already_deleted():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    message = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    #first delete of the message should be successful
    assert message_remove(userOne['token'], message['message_id']) == {}
    with pytest.raises(InputError):
        message_remove(userOne['token'], message['message_id'])


# tests for message_edit
# Forum question: does time update when a message is edited; Assumption- NO

#  valid input tests
    # user who created the message 
    # channel owner (not flockr owner)
    # owner of flockr deletes 
        # assumption is that the owner of flockr still needs to be part of the channel (but they can be a member only)
    # if an empty string is given the message is deleted

# accesserror
    # a normal member (not the member that sent the channel, nor owner of flockr or a channel_owner) tries to delete the message
    # token is invalid

# inputerror (assumption)
    # greater than 1000 characters

