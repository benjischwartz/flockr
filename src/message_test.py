import pytest
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join, 
from channels import channels_create
from error import InputError, AccessError
from other import clear


# tests for message_send
# valid input tests
    # a member of the channel sending a message
    # 0 charachters - empty string
        # Assumption: just return empty dictionary (no message is sent; dont raise an inputerror)?
    # 1000 characters - should add the message in
# invalid tests
    # accesserror if token is invalid - check
    # inputerror for message too long - check
    # accesserror if user not in the channel - check 
    # ASSUMPTION: inputerror if the channel_id is invalid     


# check if time_created that is returned in messages is a valid time object

# check an accesserror is raised when token is not valid
def test_message_send_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')
        
# raise an inputerror if the message is greater than 1000 characters
def test_message_send_over_1000_characters():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel= channels_create(userOne['token'], 'randChannel', True)
    # create a message that is 1001 characters lon
    message_long = 'a'
    for i in range(1001)
        message_long  += 'a'
        i += 1
    with pytest.raises(InputError)
        message_send(userOne['token'], randChannel['channel_id'], message_long)

# raise an accesserror if user is not in channel and tries to send a message
def test_message_send_user_not_in_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        message_send(userTwo['token'], randChannel['channel_id'], 'Hello')


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
# ASSUMPTION?? MESSAGE_IDs must be completely unique; 2 channels cannot have messages with the same message_id; check channels_create and auth_register for how to do this
# raise an accesserror if the user is not the member that sent to the channel, 
# the owner of flockr or the channel_owner

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
        message_remove(userOne['token'], message['message_id'])

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

