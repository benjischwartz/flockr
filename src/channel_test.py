# test file for the channel functions
import pytest
from auth import auth_register, auth_logout
from channel import channel_invite, channel_details, channel_messages
from channel import channel_leave, channel_join, channel_addowner, channel_removeowner
from channels import channels_create
from message import message_send
from error import InputError, AccessError
from other import clear
from time import time

# tests for channel_invite
# note: since the owner of flockr (the first user registered) has the same 
    # permissions in channel_invite as a regular member of flockr, the first
    # user registered is used for these tests


def test_channel_invite_valid_input():
    '''
    check that when given valid input channel_invite returns an empty dictionary 
    and adds the user as a regular member to the specified channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    assert channel_invite(user_one['token'], channel_one['channel_id'], user_two['u_id']) == {}
    channel_one_details = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_one_details == {
        'name': 'randChannel',
        'owner_members': [
            {
                'u_id': user_one['u_id'],
                'name_first': 'First',
                'name_last': 'User'
            }
        ],
        'all_members': [
            {
                'u_id': user_one['u_id'],
                'name_first': 'First',
                'name_last': 'User'
            },
            {
                'u_id': user_two['u_id'],
                'name_first': 'Second', 
                'name_last': 'User'
            }
        ]
    }


def test_channel_invite_same_public_or_private():
    '''
    check that when given valid input, channel_invite behaves the same whether
    the channel is public or private
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_two = channels_create(user_one['token'], 'randChannel', False)
    result_public =  channel_invite(user_one['token'], channel_one['channel_id'], user_two['u_id'])
    result_private = channel_invite(user_one['token'], channel_two['channel_id'], user_two['u_id'])
    assert result_public == result_private
    channel_one_details = channel_details(user_one['token'], channel_one['channel_id'])
    channel_two_details = channel_details(user_one['token'], channel_two['channel_id'])
    assert channel_one_details == channel_two_details
    

def test_channel_invite_invalid_token():
    '''
    check an accesserror is raised when token does not refer to a valid user
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', False)
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        channel_invite(user_one['token'], channel_one['channel_id'], user_two['u_id'])
                

def test_channel_invite_invalid_channel_id():
    '''
    check an inputerror is raised when channel_id does not refer to a valid channel;
    since the first channel created has an id of 1, 0 is an invalid channel_id
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channels_create(user_one['token'], 'randChannel', True)
    with pytest.raises(InputError):
        channel_invite(user_one['token'], 0, user_two['u_id'])
    

def test_channel_invite_invalid_u_id():
    '''
    check an inputerror is raised when u_id does not refer to a valid user
    since the first user registered has an id of 1, 0 is an invalid channel_id
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    with pytest.raises(InputError):
        channel_invite(user_one['token'], channel_one['channel_id'], 0)

def test_channel_invite_no_channels_exist():
    '''
    check an inputerror is raised when no channel exists;
    any channel_id is invalid
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        channel_invite(user_one['token'], 1, user_two['u_id'])


def test_channel_invite_not_authorised():
    '''
    check that an accesserror has been raised when the user (of the token) is not
    part of the channel and is thus, not authorised to invite 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    userThree = auth_register('thirduser@gmail.com', '876abc!@#', 'Third', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_invite(user_two['token'], channel_one['channel_id'], userThree['u_id'])


def test_channel_invite_self():
    '''
    check that an empty dictionary is returned and no changes are made to the 
    channel members if a user invites themselves    
    '''

    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_one_details_initial = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_invite(user_one['token'], channel_one['channel_id'], user_one['u_id']) == {}
    channel_one_details_after = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_one_details_initial == channel_one_details_after

def test_channel_invite_already_in():
    '''
    check that an empty dictionary is returned and no changes are made to the 
    channel members if a user invites someone already in the channel
    '''
    
    clear()        
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_join(user_two['token'], channel_one['channel_id'])
    channel_one_details_initial = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_invite(user_two['token'], channel_one['channel_id'], user_one['u_id']) == {}
    channel_one_details_after = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_one_details_initial == channel_one_details_after


# tests for channel_details
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_details as a regular member of flockr, the first
        # user registered is used for these tests


def test_channel_details_valid_input_single_user():
    '''
    check that when given valid input channel_details returns a dictionary in the 
    format defined by the spec (and asserted below)
    
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_one_details = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_one_details == {
        'name': 'randChannel', 
        'owner_members' : [
            {
                'u_id' : user_one['u_id'], 
                'name_first': 'First', 
                'name_last' : 'User'
            }
        ],
         'all_members' : [
            {
                'u_id' : user_one['u_id'], 
                'name_first': 'First', 
                'name_last' : 'User'
            }
        ]
     }


def test_channel_details_valid_input_multiple_users():
    '''
    check that when given valid input and there are multiple users in Flockr, but 
    only some of them str in the channel, channel_details returns correctly
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    # registering the second user who is in Flockr but not a member of a 
    # the channel
    auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    user_three = auth_register('thirduser@gmail.com', '456abc!@#', 'Third', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_join(user_three['token'], channel_one['channel_id'])
    channel_one_details = channel_details(user_one['token'], channel_one['channel_id'])
    assert channel_one_details == {
        'name': 'randChannel', 
        'owner_members' : [
            {
                'u_id' : user_one['u_id'], 
                'name_first': 'First', 
                'name_last' : 'User'
            }
        ],
        'all_members' : [
            {
                'u_id' : user_one['u_id'], 
                'name_first': 'First', 
                'name_last' : 'User'
            },
            {   
                'u_id' : user_three['u_id'], 
                'name_first': 'Third', 
                'name_last' : 'User'
            }
        ]
     }
 

def test_channel_invite_same_behaviour_public_or_private():
    '''
    check that when given valid input, channel_details returns the same dictionary 
    whether the channel is public or private
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    channel_two = channels_create(user_one['token'], 'randChannel', False)
    channel_one_details = channel_details(user_one['token'], channel_one['channel_id'])
    channel_two_details = channel_details(user_one['token'], channel_two['channel_id'])
    assert channel_one_details == channel_two_details
         

def test_channel_details_invalid_token():
    '''
    check an accesserror is raised when the token does not refer to a valid user
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', False)
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        channel_details(user_one['token'], channel_one['channel_id'])
        

def test_channel_details_invalid_channel_id():
    '''
    check an inputerror is raised when channel_id does not refer to a valid channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channels_create(user_one['token'], 'randChannel', True)
    invalidChannel_id = 0
    with pytest.raises(InputError):
        channel_details(user_one['token'], invalidChannel_id)


def test_channel_details_not_member():
    '''
    check an accesserror is raised when the user is not a member of the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'randChannel', True)
    with pytest.raises(AccessError):
        channel_details(user_two['token'], channel_one['channel_id'])   


# tests for channel_messages
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_messages as a regular member of flockr, the first
        # user registered is used for these tests


def test_channel_messages_valid_input_no_messages():
    '''
    check that channel_messages returns the correct dictionary given valid input
    with the user calling it being the flockr owner
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    assert channel_one_messages == {'messages': [], 'start': 0, 'end': -1}


def test_channel_messages_valid_input_3_messages():
    '''
    check that channel_messages returns the correct return dictionary when there
    are 3 messages 
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    prior_send = time()
    for _ in range(3):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    for j in range(3):
        assert channel_one_messages['messages'][j]['u_id'] == user_one['u_id']
        assert channel_one_messages['messages'][j]['message'] == 'Hello'
    after_send = time()
    oldest = channel_one_messages['messages'][2]['time_created'] 
    middle = channel_one_messages['messages'][1]['time_created'] 
    most_recent = channel_one_messages['messages'][0]['time_created'] 
    assert after_send > most_recent > middle > oldest > prior_send
    assert channel_one_messages['start'] == 0
    assert channel_one_messages['end'] == -1


def test_channel_messages_valid_input_49_messages():
    '''
    check that channel_messages returns the correct return dictionary when there
    are 49 messages
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    for _ in range(49):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    assert len(channel_one_messages['messages']) == 49
    assert channel_one_messages['start'] == 0
    assert channel_one_messages['end'] == -1


def test_channel_message_valid_input_50_messages():
    '''
    check that channel_messages returns the correct return dictionary when there
    are 50 messages
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    for _ in range(50):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    assert len(channel_one_messages['messages']) == 50
    assert channel_one_messages['start'] == 0
    assert channel_one_messages['end'] == 50


def test_channel_message_valid_input_50_messages_start_1():
    '''
    check that channel_messages returns the correct return dictionary when there
    are 50 messages but start is nonzero
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    for _ in range(50):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 1)
    assert len(channel_one_messages['messages']) == 49
    assert channel_one_messages['start'] == 1
    assert channel_one_messages['end'] == -1


def test_channel_messages_valid_input_100_messages_start_25():
    '''
    check that channel_messages returns the correct return dictionary when there
    are 100 messages and start is 25
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    for _ in range(100):
        message_send(user_one['token'], channel_one['channel_id'], 'Hello')
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 25)
    assert len(channel_one_messages['messages']) == 50
    assert channel_one_messages['start'] == 25
    assert channel_one_messages['end'] == 75

def test_channel_messages_unlimited_pagination():
    """
    checking return values for `start` and `end` when calling 
    channel_messages for numbers not multiples of 50.
    """
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')   
    randChannel = channels_create(userOne['token'], 'randChannel', True)
    for _ in range(149):
        message_send(userOne['token'], randChannel['channel_id'], 'Hello')
    messages = channel_messages(userOne['token'], randChannel['channel_id'], 0)
    assert(messages['start'] == 0)
    assert(messages['end'] == 50)       
    messages2 = channel_messages(userOne['token'], randChannel['channel_id'], 50)
    assert(messages2['start'] == 50)
    assert(messages2['end'] == 100)     
    messages3 = channel_messages(userOne['token'], randChannel['channel_id'], 100)
    assert(messages3['start'] == 100)
    assert(messages3['end'] == -1)      
    assert(len(messages3['messages']) == 49)
    # an error should be raised when start is beyond 149 messages
    with pytest.raises(InputError):     
        channel_messages(userOne['token'], randChannel['channel_id'], 150)  

def test_channel_messages_same_public_or_private():
    '''
    check that channel_messages returns the same dictionary whether the channel
    is public or private
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    channel_two = channels_create(user_one['token'], 'channel_one', False)
    channel_one_messages = channel_messages(user_one['token'], channel_one['channel_id'], 0)
    channel_two_messages = channel_messages(user_one['token'], channel_two['channel_id'], 0)
    assert channel_one_messages == channel_two_messages


def test_channel_messages_start_too_big():
    '''
    check an inputerror is raised when start is greater than the total number of 
    messages in the channel; in this test there are no messages in the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    with pytest.raises(InputError):
        channel_messages(user_one['token'], channel_one['channel_id'], 1)


def test_channel_messages_start_less_than_0():
    '''
    check an inputerror is raised when start is greater than the total number of 
    messages in the channel; in this test there are no messages in the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    with pytest.raises(InputError):
        channel_messages(user_one['token'], channel_one['channel_id'], -1)        

def test_channel_messages_invalid_token():
    '''
    check an accesserror is raised when token does not refer to a valid user
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', False)
    auth_logout(user_one['token'])
    with pytest.raises(AccessError):
        channel_messages(user_one['token'], channel_one['channel_id'], 0)
            
def test_channel_messages_invalid_channel_id():
    '''
    check an inputerror is raised when channel_id does not refer to a valid channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    channels_create(user_one['token'], 'channel_one', True)
    invalidChannel_id = 0
    with pytest.raises(InputError):
        channel_messages(user_one['token'], invalidChannel_id, 0)

def test_channel_messages_not_member():
    '''
    check that an accesserror has been raised when the user is not a member of the channel
    '''
    
    clear()
    user_one = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_two = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    channel_one = channels_create(user_one['token'], 'channel_one', True)
    with pytest.raises(AccessError):
        channel_messages(user_two['token'], channel_one['channel_id'], 0)

# tests for channel_leave
# note: since the owner of flockr (the first user registered) has the same 
        # permissions in channel_leave as a regular member of flockr, the first
        # user registered is used for these tests

# checking for validation of token - raises accesserror
def test_channel_leave_invalid_token():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'First', 'Last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    auth_logout(user['token'])
    with pytest.raises(AccessError):
        channel_leave(user['token'], userchannel_id['channel_id'])

# check for accesserror when user isn't in the specified channel
def test_channel_leave_invalid_user():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)    
    with pytest.raises(AccessError):
        channel_leave(leaver['token'], userchannel_id['channel_id'])

# check if inputerror is raised if the channel_id is invalid 
def test_channel_leave_invalid_channel():

    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    with pytest.raises(InputError):
        channel_leave(leaver['token'], invalid_id)

def test_channel_leave_normal_case():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)   
    channel_join(leaver['token'], userchannel_id['channel_id'])
    channel_leave(leaver['token'], userchannel_id['channel_id'])    
    randChannel_details = channel_details(user['token'], userchannel_id['channel_id'])
    assert(randChannel_details['all_members'] == [
    {
        'u_id' : user['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    }
    ])
# if the person removed is a owner,check whether the function actually removed him
def test_channel_leave_normal_case_owner():
    clear()
    leaver = auth_register('leaver@gmail.com', '123abc!@#', 'first', 'last') 
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)
    channel_join(leaver['token'], userchannel_id['channel_id'])
    channel_addowner(leaver['token'], userchannel_id['channel_id'], leaver['u_id'])
    channel_leave(leaver['token'], userchannel_id['channel_id'])
    randChannel_details = channel_details(user['token'], userchannel_id['channel_id'])
    assert(randChannel_details['owner_members'] == [
    {
        'u_id' : user['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    }
    ]) 

# tests for channel_join
# note: the owner of flockr (the first user registered) has special permissions
    # to join a private channel
    # user_one is always the owner of flockr.
    # first user to join flockr is always the owner of flockr
        
#checking for validation of token
def test_channel_join_invalid_token():
    clear()
    auth_register('user_one@gmail.com', '123abc!@#', 'First', 'Last')
    user_two = auth_register('user_two@gmail.com', '123abc!@#', 'First', 'Last')
    userchannel_id = channels_create(user_two['token'], 'userchannel', True)
    auth_logout(user_two['token'])
    with pytest.raises(AccessError):
        channel_join(user_two['token'], userchannel_id['channel_id'])

# check if the channel_id is invalid an inputerror is raised
def test_channel_join_invalid_channel():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    channels_create(user['token'], 'userchannel', True)
    invalid_id = 0
    with pytest.raises(InputError):
        channel_join(joiner['token'], invalid_id)
        
#checking if a user is trying to join a private channel, an accesserror is raised
def test_channel_join_private_no_invite():
    clear()
    #if the channel is private, but no invite is given to the user
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)        
    with pytest.raises(AccessError):
        channel_join(joiner['token'], userchannel_id['channel_id'])
    
#checking if the user is already in the channel, raise accesserror if they are
def test_channel_join_already_in_channel():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)   
    with pytest.raises(AccessError):
        channel_join(user['token'], userchannel_id['channel_id'])

# check if channel_join behaves correctly given valid input        
def test_channel_join_normal_case():
    clear()
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', True)   
    channel_join(joiner['token'], userchannel_id['channel_id'])    
    randChannel_details = channel_details(user['token'], userchannel_id['channel_id'])
    assert(randChannel_details['all_members'] == [
    {
        'u_id' : user['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    },
    {
        'u_id' : joiner['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    }
    ])
    
def test_channel_join_private_owner():
    clear()
    #if the channel is private, but no invite is given to the user
    #joiner is the owner in this case
    joiner = auth_register('joiner@gmail.com', '123abc!@#', 'first', 'last')
    user = auth_register('user@gmail.com', '123abc!@#', 'first', 'last')
    userchannel_id = channels_create(user['token'], 'userchannel', False)
    channel_join(joiner['token'], userchannel_id['channel_id'])        
    randChannel_details = channel_details(user['token'], userchannel_id['channel_id'])
    assert(randChannel_details['all_members'] == [
    {
        'u_id' : user['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    },
    {
        'u_id' : joiner['u_id'],
        'name_first' : 'first',
        'name_last' : 'last'
    }
    ])


# Tests for channel_addowner function
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions as the owner of a channel (if they are also a regular member)
        # the first user is registered but not used for any tests except where the
        # owner of flockr functionality is tested


def test_channel_addowner_standard_input():
    """ checking if adding another owner from the current owner's token works as expected. """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # adding user as owner
    channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])


def test_channel_addowner_invalid_token_after_logout():
    """ checking whether adding an owner after the user has logged out raises an accesserror as expected """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # logging out
    assert(auth_logout(register_second_result['token'])["is_success"] is True)

    # adding user as owner
    with pytest.raises(AccessError):
        assert channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_second_result['u_id'])


def test_channel_addowner_already_an_owner():
    """ checking if an inputerror is raised if attempting to add a user as an owner who is already an owner """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # make secondary user an owner
    channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])
    # first User (current owner) attempting to add secondary user who is also now an owner
    with pytest.raises(InputError):
        assert channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])


def test_channel_addowner_invalid_channel_id():
    """ checking if an inputerror is raised if an invalid Channel ID is inputted into the function """
    clear()
    # registering rirst user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # attempting to add second user to an invalid channel
    with pytest.raises(InputError):
        assert channel_addowner(register_second_result['token'], 'INVALIDID', register_third_result['u_id'])


def test_channel_addowner_owner_flockr():
    """ checking if owner of the flockr who is not the channel owner can add owner """
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # add first user as regular member
    channel_join(register_first_result['token'], randChannel_id['channel_id'])
    # first user adding third user
    channel_addowner(register_first_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])

def test_channel_addowner_owner_flockr_not_member():
    """ checking if AccessError is returned as expected if the owner of flockr is not a member of the channel"""
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # first user adding third user
    with pytest.raises(AccessError):
        assert channel_addowner(register_first_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])

def test_channel_addowner_not_owner():
    """ checking if AccessError is returned as expected if member is not an owner"""
    clear()
    # registering first user as the first user is the owner of the flockr
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering forth user
    register_forth_result = auth_register('randemail4@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # first user adding third user
    with pytest.raises(AccessError):
        assert channel_addowner(register_third_result['token'], randChannel_id['channel_id'], register_forth_result['u_id'])

# Tests for channel_removeowner function
    # note: since the owner of flockr (the first user registered) has the same 
        # permissions as the owner of a channel (if they are also a regular member)
        # the first user is registered but not used for any tests except where the
        # owner of flockr functionality is tested


def test_channel_removeowner_standard_input():
    """ checking if able to remove an owner who is an owner with authorised token is sucessful """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second User
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # making third user an owner of Channel
    channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])
    # removing third user
    channel_removeowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])


def test_channel_removeowner_invalid_channel_id():
    """ checking if inputerror is raised as expected if attempting to use an invalid Channel ID """
    clear()
    # registering rirst user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # attempting to remove secondary user from an invalid channel
    with pytest.raises(InputError):
        assert channel_removeowner(register_second_result['token'], 'INVALIDID', register_third_result['u_id'])


def test_channel_removeowner_invalid_user_id():
    """ checking if removing an owner with an invalid user ID raises an inputerror """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # registering third user
    auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # attempting to remove secondary user with an invalid user ID
    with pytest.raises(InputError):
        assert channel_removeowner(register_second_result['token'], randChannel_id['channel_id'], "invalidemail@gmail.com")


def test_channel_removeowner_invalid_token_after_logout():
    """ checking whether removing an owner after the user has logged out raises an accesserror as expected """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # second user creating channel
    channels_create(register_third_result['token'], 'Random Channel 2', True)
    # making third user an owner
    channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])
    # logging out second user
    auth_logout(register_second_result['token'])
    # attempting to remove third owner after logging out
    with pytest.raises(AccessError):
        assert channel_removeowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])


def test_channel_removeowner_not_owner_permissions():
    """ checking if removing an owner without owner permissions raises an accesserror """
    clear()
    # registering first user
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # third user attempting to remove second user who is owner
    with pytest.raises(AccessError):
        assert channel_removeowner(register_third_result['token'], randChannel_id['channel_id'], register_second_result['u_id'])
    

def test_channel_removeowner_owner_flockr():
    """ checking if owner of the flockr who is not the channel owner can remove owner """
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # add first user as regular member
    channel_join(register_first_result['token'], randChannel_id['channel_id'])
    # first user removing second user
    channel_removeowner(register_first_result['token'], randChannel_id['channel_id'], register_second_result['u_id'])

def test_channel_removeowner_owner_flockr_not_member():
    """ checking if AccessError is returned as expected if the owner of flockr is not a member of the channel"""
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('randemail2@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering third user
    register_third_result = auth_register('randemail3@gmail.com', 'password1234', 'Jane', 'Citizen')
    # creating channel
    randChannel_id = channels_create(register_second_result['token'], 'Random Channel', True)
    # second user adding third user
    channel_addowner(register_second_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])
    with pytest.raises(AccessError):
        assert channel_removeowner(register_first_result['token'], randChannel_id['channel_id'], register_third_result['u_id'])
