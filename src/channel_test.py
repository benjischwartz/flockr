# test file for the channel functions

from auth import auth_register, auth_login, auth_logout
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear


################################################################################
# Tests for channel_invite function - Kesh

# check that when given valid input and the channel is public, channel_behaves
# according to the spec
def test_channel_invite_valid_public_true():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    assert channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details['all_members'] == [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}, {'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}]

# check that when given valid input and the channel is private, channel_behaves
# according to the spec and the same as if the channel is public
def test_channel_invite_valid_public_false():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    assert channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details['all_members'] == [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}, {'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}]

#TODO: check that no error is raised and an empty dictionary is returned if 
# valid input is given but the user being invited is already in the channel
# DO we do tests for assumptions??

# check an AccessError is raised when token does not refer to a valid user
def test_channel_invite_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    invalidToken = 'invalidToken'
    if invalidToken == userOne['token']:
        invalidToken = 'invalidToken123'
    if invalidToken == userTwo['token']:
        invalidToken = 'invalidToken123456'
    with pytest.raises(AccessError):
        channel_invite(invalidToken, randChannel_id['channel_id'], userTwo['u_id'])
                
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_invite_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id['channel_id']:
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

# check an InputError is raised when no channel exists
def test_channel_invite_no_channels_exist():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        channel_invite(userOne['token'], 18 , userTwo['u_id'])

# check that an AccessError has been raised when the user (of the token) invites
# someone to a channel that they are not a member of
def test_channel_invite_not_authorised():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '876abc!@#', 'Third', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_invite(userTwo['token'], randChannel_id['channel_id'], userThree['u_id'])


# Tests for channel_details function
def test_channel_details_correct_return():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details == {'name': 'randChannel', 'owner_members' : [{
        'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}],
         'all_members' : [{'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}]
         }

# check an AccessError is raised when token does not refer to a valid user
def test_channel_details_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    invalidToken = 'invalidToken'
    if invalidToken == userOne['token']:
        invalidToken = 'invalidToken123'
    with pytest.raises(AccessError):
        channel_details(invalidToken, randChannel_id['channel_id'])
        
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_details_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id['channel_id']:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_details(userOne['token'], invalidChannel_id)

# check an AccessError is raised when the user is not a member of the channel
def test_channel_details_not_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_details(userTwo['token'], randChannel_id['channel_id'])   

# ------------------------------------------------------------------------------

# Tests for channel_messages function - KESH


#TODO: return type
def test_channel_messages_return_type():
    pass 

#TODO: check InputError is raised when start is greater than the total number of messages in the channel
# is this test possible
def test_channel_messages_start_too_big():
    pass

#TODO: make a test checking that with valid input, channel_messages returns correctly

# check an AccessError is raised when token does not refer to a valid user
def test_channel_details_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    invalidToken = 'invalidToken'
    if invalidToken == userOne['token']:
        invalidToken = 'invalidToken123'
    with pytest.raises(AccessError):
        channel_messages(invalidToken, randChannel_id['channel_id'], 0)
            
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_messages_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id['channel_id']:
        invalidChannel_id = 19
    with pytest.raises(InputError):
        channel_messages(userOne['token'], invalidChannel_id, 0)

# check that an AccessError has been raised when the user is not a member of the channel
def test_channel_messages_not_member():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_messages(userTwo['token'], randChannel_id['channel_id'], 0)

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
        channel_leave(leaver['token'], userchannel_id['channel_id'])
        
#------------------------------------------------------------------------------#
    
def test_channel_join_invalid_channel():
    clear()
    #BRIAN
    #if the Channel id is invalid 
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')
    joiner_login = auth_login('joiner@gmail.com', '123abc!@#')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    if userchannel_id == invalid_id:
        invalid_id = 1
    with pytest.raises(InputError):
        channel_join(joiner['token'], invalid_id)
        
def test_channel_join_private_no_invite():
    clear()
    #if the channel is private, but no invite is given to the user
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')
    #joiner_login = auth_login('joiner@gmail.com', '123abc!@#', 'first', 'last')
    joiner_login = auth_login('joiner@gmail.com', '123abc!@#')
    userchannel_id = channels_create(user['token'], 'userchannel', False)    
    
    with pytest.raises(AccessError):
        channel_join(joiner['token'], userchannel_id['channel_id'])
    
def test_channel_join_already_in_channel():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user_login = auth_login('user@gmail.com', '123abc!@#')  
    userchannel_id = channels_create(joiner['token'], 'userchannel', True)
    
    with pytest.raises(InputError):
        channel_join(joiner['token'], userchannel_id['channel_id'])
    

#################################################################################
def test_channel_addowner():
    #ETHAN
    clear()
    #Registering User
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Register Second User
    register_result_user2 = auth_register('user@gmail.com', '123abc!@#', 'Jane', 'Citizen')
    assert type(register_result_user2) is dict, "Test_Channel_1: User Sucessfully Registered"
    
    #Logging In
    ###
    #login_result = auth_login('randemail@gmail.com','password1234')
    #assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"
    ###
    #user_login = auth_login('user@gmail.com', '123abc!@#')
    randChannel_id = channels_create(register_result_user2['token'], 'randChannel2', True)

    #Check if a Non-Member Can be Made Owner
    #Check if an error is returned as expected
    with pytest.raises(AccessError):
        assert channel_addowner(register_result['token'], randChannel_id['channel_id'], "randemail@gmail.com"), "Test_Channel_3: Correct AccessError Returned as Non-Member Can't Be Owner"
    

    #Add User to Channel (Adding User to Channel 1)

    channel_join(register_result['token'], randChannel_id['channel_id'])

    #Add User as Owner
    channel_addowner(register_result['token'], randChannel_id['channel_id'], "randemail@gmail.com")


    
def test_channel_removeowner():
    #ETHAN
    clear()
    #Registering User 1
    register_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Registering User 2
    register_result_user2 = auth_register('randemailtwo@gmail.com', 'password1234', 'Jane', 'Citizens')
    assert type(register_result) is dict, "Test_Channel_1: User Sucessfully Registered"

    #Logging In
    #login_result = auth_login('randemail@gmail.com','password1234')
    #assert type(login_result) is dict, "Test_Channel_2: User Sucessfully Logged In"

    #user_login = auth_login('user@gmail.com', '123abc!@#')
    randChannel_id = channels_create(register_result['token'], 'randChannel3', True)

    #Add User to Channel (Adding User to Channel 1)
    channel_join(register_result_user2['token'], randChannel_id['channel_id'])
    # "Test_Channel_3: Check if User Sucessfully Added to Channel"
  
        
        

    #Remove Owner that is not an Owner
    #Check if Error Message Returned as Expected
    with pytest.raises(AccessError):
        assert channel_removeowner(register_result['token'], randChannel_id['channel_id'], "user@gmail.com"), "Test_Channel_4: Correct AccessError Returned as Non-Member Can't Be Owner"

    #Add User as Owner
    channel_addowner(register_result['token'], randChannel_id['channel_id'], "randemail@gmail.com")

    #Remove Owner that is an Owner
    with pytest.raises(Exception):
        assert channel_removeowner(register_result['token'], randChannel_id['channel_id'], "randemail@gmail.com"), "Thre should be an error as no other owners."
  
    
