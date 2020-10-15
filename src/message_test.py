import pytest
from auth import auth_register, auth_logout
from channel import channel_messages, channel_join, channel_leave
from channels import channels_create
from message import message_send, message_remove, message_edit
from error import InputError, AccessError
from other import clear


# tests for message_send    

# TODO: check time_created that is returned in channel_messages is a valid time object


# check that message_send returns the correct dictionary and unique message_ids starting
# from 1 and incrementing by 1 for each subsequent message as per the assumption
def test_message_send_valid_input_multiple_messages():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 3}

# check that message_send returns the correct dictionary with unique message_ids 
# even if there are multiple channels in flockr
def test_message_send_valid_input_multiple_channels():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel1 = channels_create(userOne['token'], 'randChannel1', True)
    randChannel2 = channels_create(userOne['token'], 'randChannel2', True)
    assert message_send(userOne['token'], randChannel1['channel_id'], 'Hello') == {'message_id': 1}
    assert message_send(userOne['token'], randChannel2['channel_id'], 'Hello') == {'message_id': 2}
    assert message_send(userOne['token'], randChannel1['channel_id'], 'Hello') == {'message_id': 3}
    chanMessages1 = channel_messages(userOne['token'], randChannel1['channel_id'],0)
    chanMessages2 = channel_messages(userOne['token'], randChannel2['channel_id'],0)
    assert len(chanMessages1['messages']) == 2
    assert len(chanMessages2['messages']) == 1
    
# check a message of 5 characters is successfully sent
def test_message_send_valid_input_5_chars():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    assert message_send(userOne['token'], randChannel['channel_id'], 'Hello') == {'message_id': 1}
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert len(chanMessages['messages']) == 1
    assert chanMessages['messages'][0]['message_id'] == 1
    assert chanMessages['messages'][0]['u_id'] == userOne['u_id']
    assert chanMessages['messages'][0]['message'] == 'Hello'

# check a message of 1000 characters is successfully sent
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
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'], 0)
    assert chanMessages['messages'][0]['message_id'] == 1
    assert chanMessages['messages'][0]['u_id'] == userOne['u_id']
    assert chanMessages['messages'][0]['message'] == message_long

# check an inputerror is raised if the the input 'message' is an empty string
def test_message_send_empty_message():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(InputError):
         message_send(userOne['token'], randChannel['channel_id'], '') == {}
                 
# check an inputerror is raised if the message is greater than 1000 characters
def test_message_send_over_1000_characters():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel= channels_create(userOne['token'], 'randChannel', True)
    # create a message that is 1001 characters long
    message_long = 'a'
    for i in range(1000):
        message_long  += 'a'
        i += 1
    with pytest.raises(InputError):
        message_send(userOne['token'], randChannel['channel_id'], message_long)

# check an accesserror is raised when the token is not valid
def test_message_send_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')

# check an an accesserror is raised if the user is not in channel and tries to 
# send a message
def test_message_send_user_not_in_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        message_send(userTwo['token'], randChannel['channel_id'], 'Hello')

# check an inputerror is raised if the channel_id is invalid; in this test any 
# channel_id is invalid since no channels exist
def test_message_send_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        message_send(userOne['token'], 0, 'Hello')


# tests for message_remove

# check message_remove removes the message if the user calling it is the user 
# who sent the message originally
def test_message_remove_valid_channel_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    assert message_remove(userTwo['token'], randMessage['message_id']) == {}
    chanMessages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert chanMessages == {'messages': [], 'start': 0, 'end': -1}

# check message_remove removes the message if the user calling it is the 
# owner of the channel 
def test_message_remove_valid_channel_owner():
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '456abc!@#', 'Third', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userThree['token'], randChannel['channel_id'])
    randMessage = message_send(userThree['token'], randChannel['channel_id'], 'Hello')
    assert message_remove(userTwo['token'], randMessage['message_id']) == {}
    chanMessages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert chanMessages == {'messages': [], 'start': 0, 'end': -1}

# check message_remove removes the message if the user calling it is an owner of
# flockr
def test_message_remove_valid_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userOne['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    assert message_remove(userOne['token'], randMessage['message_id']) == {}
    chanMessages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert chanMessages == {'messages': [], 'start': 0, 'end': -1}

# check message_remove removes the correct message if there are multiple 
# messages in the channel
def test_message_remove_valid_input_multiple_messages_remove_middle():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    for i in range(3):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    for j in range(3):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    chanMessages_init = channel_messages(userOne['token'], randChannel['channel_id'],0)    
    assert message_remove(userOne['token'], randMessage['message_id']) == {}
    chanMessages_after = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert len(chanMessages_after['messages']) == len(chanMessages_init['messages']) - 1
    for k in range(len(chanMessages_after['messages'])):
        assert chanMessages_after['messages'][k]['message_id'] != randMessage['message_id']

# check an accesserror is raised if an owner of flockr tries to remove a message 
# from a channel they are not a member of
def test_message_remove_invalid_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    all_messages_init = channel_messages(userTwo['token'], randChannel['channel_id'],0)    
    with pytest.raises(AccessError):
        message_remove(userOne['token'], randMessage['message_id'])
        
# check an accesserror is raised when the user that sent the message has left 
# the channel and is trying to delete the channel
def test_message_remove_user_not_part_of_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    channel_leave(userTwo['token'], randChannel['channel_id'])
    with pytest.raises(AccessError):
        message_remove(userTwo['token'], randMessage['message_id'])
   
# check an accesserror is raised when token is not valid
def test_message_remove_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_remove(userOne['token'], randMessage['message_id'])

# check an accesserror is raised when the user trying to delete is neither the 
# user who sent the message, nor the owner of flockr nor a channel owner
def test_message_remove_not_authorised_to_remove():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    message = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_remove(userTwo['token'], message['message_id'])

# check an inputerror is raised when the message being removed has already been
# deleted i.e message_d is invalid
def test_message_remove_already_deleted():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    # first delete of the message should be successful
    assert message_remove(userOne['token'], randMessage['message_id']) == {}
    with pytest.raises(InputError):
        message_remove(userOne['token'], randMessage['message_id'])


# tests for message_edit

# check message_edits edits the message if the user calling it is the user who
# sent the message originally
def test_message_edit_valid_input_channel_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    message_edit(userTwo['token'], randMessage['message_id'], 'Hello World') == {}
    chanMessages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert chanMessages['messages'][0]['message'] == 'Hello World'

# check message_edit edits the message if the user calling it is the owner of 
# the channel 
def test_message_edit_valid_input_channel_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userOne['token'], randChannel['channel_id'])
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    assert message_edit(userTwo['token'],randMessage['message_id'], 'Hello World') == {}
    chanMessages = channel_messages(userTwo['token'], randChannel['channel_id'],0)
    assert chanMessages['messages'][0]['message'] == 'Hello World'

# check message_edit edits the message if the user calling it is an owner of 
# flockr 
def test_message_edit_valid_input_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    channel_join(userOne['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    assert message_edit(userOne['token'],randMessage['message_id'], 'Hello World') == {}
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert chanMessages['messages'][0]['message'] == 'Hello World'

# check message_edit edits the correct message if there are multiple 
# messages in the channel    
def test_message_edit_valid_input_multiple_messages_edit_middle():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    message_send(userOne['token'], randChannel['channel_id'], 'Hi')
    message_send(userOne['token'], randChannel['channel_id'], 'Hi2')
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hi3')
    message_send(userOne['token'], randChannel['channel_id'], 'Hi4')
    assert message_edit(userOne['token'],randMessage['message_id'], 'Hello World') == {}
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert chanMessages['messages'][1]['message'] == 'Hello World'

# check message_edit removes a messsage if the input 'message' is an empty
# string
def test_message_edit_valid_input_empty_string():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    assert message_edit(userOne['token'],randMessage['message_id'], '') == {}
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert chanMessages == {'messages': [], 'start': 0, 'end': -1}

# check message_edit successfully edits the message if the message is 1000
# characters long
def test_message_edit_valid_input_1000_characters():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    # create a message that is 1000 characters long
    message_long = 'a'
    for i in range(999):
        message_long  += 'a'
        i += 1
    assert message_edit(userOne['token'], randMessage['message_id'], message_long) == {}
    chanMessages = channel_messages(userOne['token'], randChannel['channel_id'],0)
    assert chanMessages['messages'][0]['message'] == message_long

# check an inputerror is raised if the message is greater than 1000 characters
def test_message_edit_over_1000_characters():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    # create a message that is 1001 characters long
    message_long = 'a'
    for i in range(1001):
        message_long  += 'a'
        i += 1
    with pytest.raises(InputError):
        message_edit(userOne['token'], randMessage['message_id'], message_long)

# check an inputerror is raised if the message_id is invalid (eg. it has been
# deleted)
def test_message_edit_invalid_message_id_no_messages():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    message_remove(userOne['token'], randMessage['message_id'])
    with pytest.raises(InputError):
        message_edit(userOne['token'], randMessage['message_id'], 'Hello World')

# check an accesserror is raised when the token is not valid 
def test_message_edit_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', False)
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        message_edit(userOne['token'], randMessage['message_id'], 'Hello World')

# check an accesserror is raised when the user trying to delete is neither the 
# user who sent the message, nor the owner of flockr nor a channel owner
def test_message_edit_not_authorised_to_remove():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    randMessage = message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_edit(userTwo['token'], randMessage['message_id'], 'Hello World')   

# check an accesserror is raised if a user tries to edit a message but they 
# have left the channel and are thus not a member of it anymore
def test_message_edit_user_not_part_of_channel():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel['channel_id'])
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    channel_leave(userTwo['token'], randChannel['channel_id'])
    with pytest.raises(AccessError):
        message_edit(userTwo['token'], randMessage['message_id'], 'Hello World')   

# check an accesserror is raised if an owner of flockr tries to edit a message 
# of a channel they are not a member of
def test_message_edit_invalid_flockr_owner():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel = channels_create(userTwo['token'], 'randChannel', True)
    randMessage = message_send(userTwo['token'], randChannel['channel_id'], 'Hello')
    with pytest.raises(AccessError):
        message_edit(userOne['token'],randMessage['message_id'], 'Hello World')


