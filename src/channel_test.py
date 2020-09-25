# test file for the channel functions

from auth import auth_register
from channel import channel_invite, channel_details, channel_messages
from channels import channels_create
import pytest
from error import InputError





# check channel_invite
# This test is meant to check if an inputError is given if the channel_id is 
# invalid; INCOMPLETE
# Note: "result['token'] may not be valid python but my intention was to get
# the token and u_id values that were returned from auth_register 

# Tests for channel_invite function - Kesh
    # function input: token, channel_id, u_id
    # output - dictionary
    
    # check an InputError is raised when channel_id does not refer to a valid channel
    
    # check an InputError is raised when u_id does not refer to a vlid user
    
    # check that an AccessError has been raised when the user is not a member of the channel
    
def test_channel_invite_invalid_channel_id:
    #KESH

    result = auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    randChannel_id = channels_create(result['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    #with pytest.raises(InputError) as e:
        #assert channel_invite(result['token'], invalidChannel_id, result['u_id'])


# Tests for channel_details function - KESH
    # function input: token, channel_id
    # output - dictionary
    
    # check an InputError is raised when channel_id does not refer to a valid channel
    # check that an AccessError has been raised when the user is not a member of the channel
    
    
def test_channel_details():
    

# Tests for channel_messages function - KESH
    # function input: token, channel_id, start
    # output - dictionary
    # check and InputError is raised when start is greater than the total number of messages in the channel
    # check an InputError is raised when channel_id does not refer to a valid channel
    # check that an AccessError has been raised when the user is not a member of the channel
    
def test_channel_messages():
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
    
        
    
