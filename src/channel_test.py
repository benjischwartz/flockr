# test file for the channel functions

from auth import auth_register
from channel import channel_invite, channel_details, channel_messages
from channels import channels_create
import pytest
from error import InputError

# Tests for channel_invite function - Kesh
    # function input: token, channel_id, u_id
    # output - dictionary
    # token is the authorised user, u_id is for the person being invited,
    # CASE 1 : the user invites themselve?? what should happen 
    # instead of using functions, could create dictionaries with the return types
    # that auth_register and channel_create are meant to give??
    # CASE 2 : the authorised user invites someone that is already part of the channel

def test_channel_invite_return_type():

# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_invite_invalid_channel_id():
    # userOne and userTwo are dictionaries containing u_id and token
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    
    # randchannel_id is a dictionary mapping channel_id to a number
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    # create a channel_id and then make sure it isn't valid
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_invite(userOne['token'], invalidChannel_id, userTwo['u_id'])
        
    # Notes: maybe it isn't necessary to create a randChannel_id since all 
    # channel_ids are invalid if no channel has been created yet
    # or that could be a separate test where if there is no channel, it should 
    # return an error
        # NVM, we want userOne to be a member of a channel so that they can
        # actually be invite a new user for this test
        # If there is no channel in the system currently, then channel_invite
        # should return AccessError (potential test?)

# check an InputError is raised when u_id does not refer to a valid user
def test_channel_invite_invalid_u_id():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randu_id = 18
    if randu_id == userOne['u_id']:
        randu_id = 19
    with pytest.raises(InputError):
        channel_invite(userOne['token'], randChannel_id['channel_id'], randu_id)

# check that an AccessError has been raised when the user is not a member of the channel
def test_channel_invite_not_a_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    # no channels exist
    with pytest.raises(AccessError):
        channel_invite(userOne['token'], 18 , randu_id)


#TODO: A test where there is an AccessError where channels exist but the token person 
# isnt in that channel and asks it to invite? is it necessary?    
    
# Tests for channel_details function - KESH
    # function input: token, channel_id
    # output - dictionary
    
    # check an InputError is raised when channel_id does not refer to a valid channel
    # check that an AccessError has been raised when the user is not a member of the channel
    
    
def test_channel_details():
    pass 

# Tests for channel_messages function - KESH
    # function input: token, channel_id, start
    # output - dictionary
    # check and InputError is raised when start is greater than the total number of messages in the channel
    # check an InputError is raised when channel_id does not refer to a valid channel
    # check that an AccessError has been raised when the user is not a member of the channel
    
def test_channel_messages():
    pass 
    #KESH
def test_channel_leave():
    #BRIAN
def test_channel_join():
    #BRIAN
    
def test_channel_addowner():
    #ETHAN

    #Registering User
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Logging In
    login_result = auth_login('randemail@gmail.com','password1234')
    assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"

    #Check if a Non-Member Can be Made Owner
    channel_addowner(login_result['token'], 1, "randemail@gmail.com")
    #TODO:Check if an error is returned as expected

    #Add User to Channel (Adding User to Channel 1)
    channel_join(login_result['token'], 1)
    #TODO:Check if Successfully Joined

    #Add User as Owner
    channel_addowner(login_result['token'], 1, "randemail@gmail.com")
    #TODO:Check if Owner Successfully Added


    
def test_channel_removeowner():
    #ETHAN
    
    #Registering User
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Logging In
    login_result = auth_login('randemail@gmail.com','password1234')
    assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"

    #Add User to Channel (Adding User to Channel 1)
    channel_join(login_result['token'], 1)
    #TODO:Check if Successfully Joined

    #Remove Owner that is not an Owner
    channel_removeowner(login_result['token'], 1, "randemail@gmail.com")
    #TODO:Check if Error Message Returned as Expected

    #Add User as Owner
    channel_addowner(login_result['token'], 1, "randemail@gmail.com")
    #TODO:Check if Owner Successfully Added

    #Remove Owner that is an Owner
    channel_removeowner(login_result['token'], 1, "randemail@gmail.com")
    #TODO:Check if Owner Sucessfully Removed
    
        
    
