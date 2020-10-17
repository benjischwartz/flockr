# test file for the channels functions
# channels, plural, is a data struct looking at the channels globally
# whereas channel, singular, are user actions within the channel

from channels import channels_listall, channels_list, channels_create
from auth import auth_register
import pytest
from error import InputError, AccessError
from other import clear

# check return values are valid types
# add more to check the dict key values
def test_return_type():
    # clear database and register new dummy users for testing
    clear()
    user_one = auth_register("first@example.com", "password1234", " ", " ")
    user_two = auth_register("second@example.com", "password1234", " ", " ")
    user_three = auth_register("third@example.com", "password1234", " ", " ")
    # check types
    assert(type(channels_list(user_one["token"])) is dict) 
    assert(type(channels_listall(user_two["token"])) is dict)
    assert(type(channels_create(user_three["token"], "somename", True)) is dict)

# check channels create() adds a new channel
# calls channels_listall to check
def test_channels_create_valid():
    # clear database and register new dummy users for testing
    clear()
    userOne = auth_register("first@example.com", "password1234", " ", " ")
    userTwo = auth_register("second@example.com", "password1234", " ", " ")
    # number of channels before
    before = len(channels_listall(userOne['token'])['channels'])
    # test if channel is in channels list_all after
    # create public channel 
    newChannel = channels_create(userOne['token'], "validchannel", True)
    # check if channel id is in channels list
    Found = False
    new_channel_id = newChannel['channel_id']
    allChannelsList = channels_listall(userTwo['token'])['channels']
    for eachChannel in allChannelsList:
        if eachChannel['channel_id'] == new_channel_id:
            Found = True
            break
    # check number of channels has increased by one
    assert len(allChannelsList) - before == 1, "error: in number of channels found"
    assert Found == True, "channel_create has not added the new channel id to database"

# check raises ACCESS ERROR if token is invalid for channel_create
def test_channels_create_invalid_token():
    clear()
    # check string
    with pytest.raises(AccessError):
        channels_create(123, "name", False)
    # Expect this test to fail 
    with pytest.raises(AccessError):
        assert channels_create("invalidtoken", "name", False)

def test_channels_list_invalid_token():
    clear()
    with pytest.raises(AccessError):
        assert channels_list("invalidtoken")


def test_channels_listall_invalid_token():
    clear()
    with pytest.raises(AccessError):
        assert channels_listall("invalidtoken")

# Check if user can view only appropriate lists they are a member of
def test_channels_list_user_view():
    # clear database and register new dummy users for testing
    clear()
    userOne = auth_register("first@example.com", "password1234", " ", " ")
    userTwo = auth_register("second@example.com", "password1234", " ", " ")
    # create channels that has no users
    channels_create(userOne['token'], "validchannel1", True)
    channels_create(userTwo['token'], "validchannel2", True)
    # create user and compare channels_list result with channels_list_all
    assert channels_list(userOne['token']) != channels_listall(userTwo['token']), "users can see all lists, even if not a member"
    assert len(channels_list(userOne['token'])['channels']) == 1, "channel list per user sees unexpected number"
    assert len(channels_listall(userOne['token'])['channels']) == 2,  "channel listall per user sees unexpected number"
    assert len(channels_listall(userTwo['token'])['channels']) == 2, "channel listall per user sees unexpected number"
    
# check channels_create raises input error when name is too long
def test_channels_create_too_long_name():
    # clear database and register new dummy users for testing
    clear()
    userThree = auth_register("third@example.com", "password1234", " ", " ")
    with pytest.raises(InputError):
        channels_create(userThree['token'], "a_string_name_which_is_very_long_and_will_never_pass", True)


