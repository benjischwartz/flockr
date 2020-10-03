# test file for the channel functions

from auth import auth_register, auth_login, auth_logout
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
import pytest
from error import InputError, AccessError
from other import clear

################################################################################
# Tests for channel_invite function
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_invite as a regular member of flockr, the first
        # user registered is used for these tests
    # also note: any function other than channel_invite called in these tests is 
        # assumed to be working correctly
################################################################################

# check that when given valid input channel_invite returns an empty dictionary 
# and only adds the user as a regular member
def test_channel_invite_valid_input():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    assert channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id']) == {}
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details == {'name': 'randChannel', 'owner_members' : [{
        'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}],
         'all_members' :  [{'u_id': userOne['u_id'], 
        'name_first' : 'First', 'name_last': 'User'}, {'u_id': userTwo['u_id'], 
        'name_first' : 'Second', 'name_last': 'User'}]}

# check that when given valid input, channel_invite behaves the same whether
# the channel is public or private
def test_channel_invite_same_public_or_private():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_id2 = channels_create(userOne['token'], 'randChannel', False)
    resultPublic =  channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id'])
    resultPrivate = channel_invite(userOne['token'], randChannel_id2['channel_id'], userTwo['u_id'])
    assert resultPublic == resultPrivate
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    randChannel_details2 = channel_details(userOne['token'], randChannel_id2['channel_id'])
    assert randChannel_details == randChannel_details2
    
# check an AccessError is raised when token does not refer to a valid user
def test_channel_invite_invalid_token():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', False)
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        channel_invite(userOne['token'], randChannel_id['channel_id'], userTwo['u_id'])
                
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_invite_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 0
    if invalidChannel_id == randChannel_id['channel_id']:
        invalidChannel_id = 1
    with pytest.raises(InputError):
        channel_invite(userOne['token'], invalidChannel_id, userTwo['u_id'])
    
# check an InputError is raised when u_id does not refer to a valid user
def test_channel_invite_invalid_u_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidu_id = 0
    if invalidu_id == userOne['u_id']:
        invalidu_id = 1
    with pytest.raises(InputError):
        channel_invite(userOne['token'], randChannel_id['channel_id'], invalidu_id)

# check an InputError is raised when no channel exists
def test_channel_invite_no_channels_exist():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        channel_invite(userOne['token'], 0, userTwo['u_id'])

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

# check that an empty dictionary is returned and no changes are made to the 
# channel members if a user invites themselves
def test_channel_invite_self():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_detailsInitial = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert channel_invite(userOne['token'], randChannel_id['channel_id'], userOne['u_id']) == {}
    randChannel_detailsAfter = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_detailsInitial == randChannel_detailsAfter


# check that an empty dictionary is returned and no changes are made to the 
# channel members if a user invites someone already in the channel

def test_channel_invite_already_in():
    clear()        
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    channel_join(userTwo['token'], randChannel_id['channel_id'])
    randChannel_detailsInitial = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert channel_invite(userTwo['token'], randChannel_id['channel_id'], userOne['u_id']) == {}
    randChannel_detailsAfter = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_detailsInitial == randChannel_detailsAfter

################################################################################
# Tests for channel_details function
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_invite as a regular member of flockr, the first
        # user registered is used for these tests
    # also note: any function other than channel_details called in these tests 
        # is assumed to be working correctly
################################################################################

# check that when given valid input channel_details returns a dictionary in the 
# format defined by the spec (and asserted below)
def test_channel_details_valid_input_():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    assert randChannel_details == {'name': 'randChannel', 'owner_members' : [{
        'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}],
         'all_members' : [{'u_id' : userOne['u_id'], 'name_first': 'First', 'name_last' : 'User'}]
         }
 
# check that when given valid input, channel_details returns the same dictionary
# whether the channel is public or private
def test_channel_invite_same_behaviour_public_or_private():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_id2 = channels_create(userOne['token'], 'randChannel', False)
    randChannel_details = channel_details(userOne['token'], randChannel_id['channel_id'])
    randChannel_details2 = channel_details(userOne['token'], randChannel_id2['channel_id'])
    assert randChannel_details == randChannel_details2
         
# check an AccessError is raised when the token does not refer to a valid user
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
    invalidChannel_id = 0
    if invalidChannel_id == randChannel_id['channel_id']:
        invalidChannel_id = 1
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

################################################################################
# Tests for channel_mesages function
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_invite as a regular member of flockr, the first
        # user registered is used for these tests
    # also note: any function other than channel_messages called in these tests is 
        # assumed to be working correctly
################################################################################

# check that channel_messages returns the correct dictionary given valid input
# with the user calling it being the flockr owner
def test_channel_messages_valid_input():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randMessages = channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
    assert randMessages == {'messages': [], 'start': 0, 'end': -1}

# check that channel_messages returns the same dictionary whether the channel
# is public or private
def test_channel_messages_same_public_or_private():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    randChannel_id2 = channels_create(userOne['token'], 'randChannel', False)
    randMessages = channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
    randMessages2 = channel_messages(userOne['token'], randChannel_id2['channel_id'], 0)
    assert randMessages == randMessages2

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
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        channel_messages(userOne['token'], randChannel_id['channel_id'], 0)
            
# check an InputError is raised when channel_id does not refer to a valid channel
def test_channel_messages_invalid_channel_id():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    randChannel_id = channels_create(userOne['token'], 'randChannel', True)
    invalidChannel_id = 0
    if invalidChannel_id == randChannel_id['channel_id']:
        invalidChannel_id = 1
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
    registerFirst_logout = auth_logout(registerFirst_result['token'])
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
    #Creating Channel
    randChannel_id = channels_create(registerFirst_result['token'], 'Random Channel', True)
    #Registering Secondary User
    registerSecond_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    #First User Adding Secondary User
    channel_addowner(registerFirst_result['token'], randChannel_id['channel_id'], registerSecond_result['u_id'])

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
def test_channel_addowner_invalid_token_after_logout():
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

