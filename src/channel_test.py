# test file for the channel functions

from auth import auth_register
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear


################################################################################
# Tests for channel_invite function - Kesh
    # function input: token, channel_id, u_id
    # output - dictionary
    # token is the authorised user, u_id is for the person being invited,
    # CASE 3: channels_create --> is_public is False?? What is meant to happen
        # create tests for channel_invite, channel_details

'''
# check that when given valid input, randChannel_id does add the person and 
# returns the correct output
def test_channel_invite_correct_return():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    assert channel_invite(userOne['token'], randChannel_id, userTwo['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id)
    assert randChannel_details['all_members'] == [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}, {'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}

'''
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_invite_invalid_channel_id():
    clear()
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
    

# check an InputError is raised when u_id does not refer to a valid user
def test_channel_invite_invalid_u_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randu_id = 18
    if randu_id == userOne['u_id']:
        randu_id = 19
    with pytest.raises(InputError):
        channel_invite(userOne['token'], randChannel_id['channel_id'], randu_id)


#TODO: BAD TEST---> CHECK IF this test is meaningul
def test_channel_invite_no_channels_exist():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        channel_invite(userOne['token'], 18 , userTwo['u_id'])

# check that an AccessError has been raised when a user who is not a member of the channel
# invites someone not in the channel    
def test_channel_invite_not_a_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '876abc!@#', 'Third', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_invite(userTwo['token'], randChannel_id , userThree['u_id'])
    assert channel_invite(userTwo['token'], randChannel_id , userThree['u_id']) == 'Hello'

#TODO:  add yourself/ someone in the channel already

'''
#-------------------------------------------------------------------------------        
# Tests for channel_details function - KESH
    # function input: token, channel_id
    # output - dictionary
    
    
def test_channel_details_correct_return():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_details = channel_details(userOne['token'], randChannel_id)
    assert randChannel_details = {
    #TODO:  Finish this 

# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_details_invalid_channel_id():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_details(userOne['token'], invalidChannel_id)

# check an AccessError is raised when the user is not a member of the channel
def test_channel_details_not_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_details(userTwo['token'], randChannel_id)   

# ------------------------------------------------------------------------------
# Tests for channel_messages function - KESH
    # function input: token, channel_id, start
    # output - dictionary
    # WTH is start for these functions


#TODO: return type
def test_channel_messages_return_type():
    pass 

#TODO: check InputError is raised when start is greater than the total number of messages in the channel
# is this test possible
def test_channel_messages_start_too_big():
    pass

# TODO: make a test checking that with valid input, channel_messages returns correctly
    
# TODO:check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_messages_invalid_channel_id():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_messages(userOne['token'], invalidChannel_id, 0)
        # let start = 0 for 0 messages?

# TODO: check that an AccessError has been raised when the user is not a member of the channel
def test_channel_messages_not_member():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_messages(userTwo['token'], randChannel_id, 0)
'''
#################################################################################
#channel_leave (token, channel_id)
def test_channel_leave_invalid_user():
    #BRIAN
    #check for access error when user isn't in the specified channel
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')
    leaver_login = auth_login('leaver@gmail.com', '123abc!@#')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    
    with pytest.raises(AccessError):
        channel_leave(leaver['token'], userchannel_id)
        
#------------------------------------------------------------------------------#
    
def test_channel_join_invalid_channel():
    #BRIAN
    #if the Channel id is invalid 
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')
    joiner_login = auth_login('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    if userchannel_id == invalid_id:
        invalid_id = 1
    with pytest.raises(InputError):
        channel_join(joiner['token'], invalid_id)
        
def test_channel_join_private_no_invite():
    #if the channel is private, but no invite is given to the user
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')
    joiner_login = auth_login('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)    
    
    with pytest.raises(AccessError):
        channel_join(joiner['token'], userchannel_id)
    
def test_channel_join_already_in_channel():
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')  
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    
    with pytest.raises(InputError):
    channel_join(joiner['token'], userchannel_id)
    

#################################################################################
def test_channel_addowner():
    #ETHAN

    #Registering User
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Logging In
    login_result = auth_login('randemail@gmail.com','password1234')
    assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"

    #Check if a Non-Member Can be Made Owner
    #Check if an error is returned as expected
    with pytest.raises(AccessError):
        assert channel_addowner(login_result['token'], 1, "randemail@gmail.com"), "Test_Channel_3: Correct AccessError Returned as Non-Member Can't Be Owner"
    

    #Add User to Channel (Adding User to Channel 1)
    try:
        channel_join(login_result['token'], 1)
    except:
        #Check if Successfully Joined
        assert False, "Test_Channel_4: Check if User Sucessfully Added to Channel"

    #Add User as Owner
    try:
        channel_addowner(login_result['token'], 1, "randemail@gmail.com")
    except:
        #Check if Owner Successfully Added
        assert False, "Test_Channel_5: Check if Member User Sucessfully Added as Owner"


    
def test_channel_removeowner():
    #ETHAN
    
    #Registering User
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Logging In
    login_result = auth_login('randemail@gmail.com','password1234')
    assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"

    #Add User to Channel (Adding User to Channel 1)
    try:
        channel_join(login_result['token'], 1)
    except:
        #Check if Successfully Joined
        assert False, "Test_Channel_3: Check if User Sucessfully Added to Channel"

    #Remove Owner that is not an Owner
    #Check if Error Message Returned as Expected
    with pytest.raises(AccessError):
        assert channel_removeowner(login_result['token'], 1, "randemail@gmail.com"), "Test_Channel_4: Correct AccessError Returned as Non-Member Can't Be Owner"

    #Add User as Owner
    try:
        channel_addowner(login_result['token'], 1, "randemail@gmail.com")
    except:
        #Check if Owner Successfully Added
        assert False, "Test_Channel_5: Check if User Sucessfully Added to Channel"

    #Remove Owner that is an Owner
    try:
        channel_removeowner(login_result['token'], 1, "randemail@gmail.com")
    except:
        #Check if Owner Sucessfully Removed
        assert False, "Test_Channel_6: Check if User Sucessfully Removed From Channel"
  
    
