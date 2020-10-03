# test file for the channel functions

from auth import auth_register, auth_login, auth_logout
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear

# Tests for channel_invite function

# check that when given valid input and the channel is public, channel_invite
# behaves according to the spec
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

# check that when given valid input and the channel is private, channel_invite
# behaves according to the spec (the same as if the channel was public)
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

# check an AccessError is raised when token does not refer to a valid user
def test_channel_invite_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    userOne_logout = auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id'])
                
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

# check that an AccessError has been raised when the user (of the token) is not
# part of the channel and is thus, not authorised to invite 
def test_channel_invite_not_authorised():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '876abc!@#', 'Third', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_invite(userTwo['token'], randChannel_id['channel_id'], userThree['u_id'])

# check that no error is raised and nothing is done in the case that the user
# invites themselves
def test_channel_invite_aready_in_self():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    assert channel_invite(userOne['token'], randChannel_id['channel_id'], userOne['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details['all_members'] == [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}]

# check that no error is raised and nothing is done in the case that the user
# invites someone already in the channel
def test_channel_invite_already_in_else():
    clear()        
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id'])
    assert channel_invite(userTwo['token'], randChannel_id['channel_id'], userOne['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details['all_members'] == [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}, {'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}]

# check that when an owner is added they are not added as an owner
def test_channel_invite_flockr_owner():
    clear()        
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userTwo['token'], 'randChannel', True)
    channel_invite(userTwo['token'], randChannel_id['channel_id'], userOne['u_id'])
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details['owner_members'] == [{'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}]

# Tests for channel_details function

# check that when given valid input and the channel is public, channel_details
# behaves according to the spec
def test_channel_details_valid_public_true():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details == {'name': 'randChannel', 'owner_members' : [{
        'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}],
         'all_members' : [{'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}]
         }

# check that when given valid input and the channel is private, channel_details
# behaves according to the spec
def test_channel_details_valid_public_true():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
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
    userOne_logout = auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        channel_details(userOne['token'], randChannel_id['channel_id'])
        
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


# Tests for channel_messages function
# Require updated channels_create for these tests to work

# check that channel_messages returns the correct dictionary given valid input
# with a channel that has no messages and the channel is public   
def test_channel_messages_no_messages_public_true():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randMessages = channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
    assert randMessages == {'messages': [], 'start': 0, 'end': -1}

# check that channel_messages returns the correct dictionary given valid input
# with a channel that has no messages and the channel is private
# channel_messages should behave the same as if the channel was public
def test_channel_messages_no_messages_public_true():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    randMessages = channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
    assert randMessages == {'messages': [], 'start': 0, 'end': -1}


# check an InputError is raised when start is greater than the total number of 
# messages in the channel; in this test there are no messages in the channel
def test_channel_messages_start_too_big():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(InputError):
        channel_messages(userOne['token'], randChannel_id['channel_id'], 1)

# check an InputError is raised when start is greater than the total number of 
# messages in the channel; in this test there are no messages in the channel
def test_channel_messages_start_less_than_0():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    with pytest.raises(InputError):
        channel_messages(userOne['token'], randChannel_id['channel_id'], -1)        

# check an AccessError is raised when token does not refer to a valid user
def test_channel_messages_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    userOne_logout = auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
            
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

################################################################################
# Tests for channel_leave
#checking for validation of token - raises access error
def test_channel_leave_invalid_token():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'First', 'Last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)
    user_logout = auth_logout(user['token'])
    with pytest.raises(AccessError):
        channel_leave(user['token'], userchannel_id['channel_id'])

def test_channel_leave_invalid_user():
    #BRIAN
    clear()
    #check for access error when user isn't in the specified channel
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    
    with pytest.raises(AccessError):
        channel_leave(leaver['token'], userchannel_id['channel_id'])
        
def test_channel_leave_invalid_channel():
    #BRIAN
    #if the Channel id is invalid - input error
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    if userchannel_id['channel_id'] == invalid_id:
        invalid_id = 1
    with pytest.raises(InputError):
        channel_leave(leaver['token'], invalid_id)
        
#------------------------------------------------------------------------------#
#checking for validation of token
def test_channel_join_invalid_token():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'First', 'Last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)
    user_logout = auth_logout(user['token'])
    with pytest.raises(AccessError):
        channel_join(user['token'], userchannel_id['channel_id'])
    
def test_channel_join_invalid_channel():
    #BRIAN
    #if the Channel id is invalid - raises input error
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    if userchannel_id['channel_id'] == invalid_id:
        invalid_id = 1
    with pytest.raises(InputError):
        channel_join(joiner['token'], invalid_id)
        
#checking if a user is trying to join a private channel, throw access error
def test_channel_join_private_no_invite():
    clear()
    #if the channel is private, but no invite is given to the user
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    #joiner_login = auth_login('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)    
    
    with pytest.raises(AccessError):
        channel_join(joiner['token'], userchannel_id['channel_id'])
    
#checking if the user is already in the channel, return access error if it is
def test_channel_join_already_in_channel():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    
    with pytest.raises(AccessError):
        channel_join(user['token'], userchannel_id['channel_id'])
    
    

#################################################################################

#checking if adding another owner from the current owner's token works as expected
def test_channel_addowner_standard_input():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Adding User as Owner
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

# checking whether adding an owner after the user has logged out returns AccessError as expected
def test_channel_addowner_invalid_token_after_logout():
    clear()
    #Registering User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Logging Out
    assert auth_logout(registerFirst_result['token'])["is_success"] == True

    #Adding User as Owner
    with pytest.raises(AccessError):
        assert channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerFirst_result['u_id'])

#checking if an InputError is returned if attempting to add a user as an owner who is already an owner
def test_channel_addowner_already_an_owner():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Secondary User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Make Secondary User an Owner
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])
    #First User (Current Owner) Attempting to Add Secondary User Who Is Also Now an Owner
    with pytest.raises(InputError):
        assert channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

#checking if an InputError is returned if an invalid Channel ID is inputted into the function
def test_channel_addowner_invalid_channel_id():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Registering Secondary User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Attempting to Add Secondary User to an Invalid Channel
    with pytest.raises(InputError):
        assert channel_addowner(registerFirst_result['token'], 'INVALIDID', registerSecond_result['u_id'])

#checking if owner of the flockr who is not the channel owner can add owner 
def test_channel_addowner_owner_flockr():
    clear()
    #Registering First User as the First User is the Owner of the Flockr
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Registering Secondary User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerSecond_result['token'], 'Random Channel', True)
    #Add First User as Regular Member
    channel_join(registerFirst_result['token'], randChannel_id['channel_id'])
    #Registering Third User
    registerThird_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    #First User Adding Second User
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerThird_result['u_id'])

#checking if able to remove an owner who is an owner with authorised token is sucessful 
def test_channel_removeowner_standard_input():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Making Second User an Owner of Channel
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])
    #Removing Second User
    channel_removeowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

#checking if InputError returned as expected if attempting to use an invalid Channel ID
def test_channel_removeowner_invalid_channel_id():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Attempting to Remove Secondary User from an Invalid Channel
    with pytest.raises(InputError):
        assert channel_removeowner(registerFirst_result['token'], 'INVALIDID', registerSecond_result['u_id'])

#checking if removing an owner with an invalid user ID
def test_channel_removeowner_invalid_user_id():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Attempting to Remove Secondary User with an Invalid User ID
    with pytest.raises(InputError):
        assert channel_removeowner(registerFirst_result['token'], randChannel_id['channel_id'], "invalidemail@gmail.com")

# checking whether removing an owner after the user has logged out returns AccessError as expected
def test_channel_removeowner_invalid_token_after_logout():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Second User Creating Channel
    randChannelSecond_id = channels_create(registerSecond_result['token'], 'Random Channel 2', True)
    #Making Second User an Owner
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])
    #Logging Out First User
    registerFirst_logout = auth_logout(registerFirst_result['token'])
    #Attempting to Remove Secondary Owner After Logging Out
    with pytest.raises(AccessError):
        assert channel_removeowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

#checking if removing an owner without owner permissions raises an AccessError
def test_channel_removeowner_not_owner_permissions():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Second user attempting to remove First User who is owner
    with pytest.raises(AccessError):
        assert channel_removeowner(registerSecond_result['token'], randChannel_id['channel_id'], registerFirst_result['u_id'])
    
#checking if owner of the flockr who is not the channel owner can remove owner 
def test_channel_removeowner_owner_flockr():
    clear()
    #Registering First User
    registerFirst_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Second User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #Making Second User an Owner of Channel
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])
    #Removing Second User
    channel_removeowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

