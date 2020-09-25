# test file for the channel functions

from auth import auth_register
from channel import channel_invite, channel_details, channel_messages
from channels import channels_create
import pytest
from error import InputError


################################################################################
# Tests for channel_invite function - Kesh
    # function input: token, channel_id, u_id
    # output - dictionary
    # token is the authorised user, u_id is for the person being invited,
    # CASE 1 : the user invites themselves?? what should happen 
    # CASE 2 : the authorised user invites someone that is already part of the channel
    # CASE 3: channels_create --> is_public is False?? What is meant to happen
        # create tests for channel_invite, channel_details

# TODO: make a test checking that with valid input, channel_invite BEHAVES correctly
    # since the user is immediately add once invited, then we can check the channel_details or smth
    # to see if they have been added (see Cece tests with for loop)
   
#TODO: return type
def test_channel_invite_return_type():
    pass

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
        # actually be invite a new user for this test (assume channel creator
        # automatically joins the channel they created)
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


# BAD TEST---> CHECK IF this test is meaningul
def test_channel_invite_no_channels_exist():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        channel_invite(userOne['token'], 18 , randu_id)


#TODO: If we assume that adding someone already in the channel causes problems eg. userOne is 
# in the channel since they created it; then this test needs to be changed by 
# adding a third user
# check that an AccessError has been raised when the user is not a member of the channel    
def test_channel_invite_not_a_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_invite(userTwo['token'], randchannel_id , userTwo['u_id'])

#-------------------------------------------------------------------------------        
# Tests for channel_details function - KESH
    # function input: token, channel_id
    # output - dictionary
    
    
def test_channel_details_return_type():
    pass 

# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_details_invalid_channel_id():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_details(userOne['token'], invalidChannel_id)

# check and AccessError is raised when the user is not a member of the channel
def test_channel_details_not_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_details(userTwo['token'], randChannel_id)

# TODO: make a test checking that with valid input, channel_details returns correctly
# could use channel_join/channel_invite to add a person and see if channel_details updates???    

# ------------------------------------------------------------------------------
# Tests for channel_messages function - KESH
    # function input: token, channel_id, start
    # output - dictionary
    # WTH is start for these functions


#TODO: return type
def test_channel_messages_return_type():
    pass 

# check InputError is raised when start is greater than the total number of messages in the channel
# is this test possible
def test_channel_messages_start_too big():
    pass

# TODO: make a test checking that with valid input, channel_messages returns correctly
    
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_messages_invalid_channel_id():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_messages(userOne['token'], invalidChannel_id, 0)
        # let start = 0 for 0 messages?

# check that an AccessError has been raised when the user is not a member of the channel
def test_channel_messages_not_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_messages(userTwo['token'], randChannel_id, 0)

#################################################################################
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
    
        
    
