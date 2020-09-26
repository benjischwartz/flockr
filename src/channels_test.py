# test file for the channels functions
# channels, plural, is a data struct looking at the channels globally
# whereas channel, singular, are user actions within the channel

from channels import channels_listall, channels_list, channels_create
import pytest
from error import InputError

# check return values are valid types
# add more to check the dict key values
def test_return_type():
    assert(type(channels_list("validtoken")) is dict) 
    assert(type(channels_listall("validtoken")) is dict)
    assert(type(channels_create("validtoken", "somename", True)) is dict)

# check channels create() adds a new channel
# calls channels_listall to check
def test_channels_create_valid():
    # test if channel is in channels list_all after
    # create public channel 
    newChannel = channels_create("validtoken", "validchannel", True)
    # check if channel id is in channels list
    # TODO??? check if channel id didn't aleady exist: i.e unique keys?
    Found = False
    new_channel_id = newChannel['channel_id']
    allChannelsList = channels_listall("validtoken")['channels']
    for eachChannel in allChannelsList:
        if eachChannel['channel_id'] == new_channel_id:
            Found = True
            break
    # TODO: test only user when channel created is the user identified by the token
    assert Found == True, "channel_create has not added the new channel id to database"

# check raises ACCESS ERROR if token is invalid for channel_create
def test_channels_create_invalid_token():
    # check string
    with pytest.raises(AccessError, m=r"Token passed in is not valid"):
        channels_create("7897", "name", False)
    # Expect this test to fail 
    with pytest.raises(AccessError, m=r"Token passed in is not valid"):
        channels_create("invalidtoken", "name", False)


# Check if user can view only appropriate lists they are a member of
def test_channels_list_user_view():
    # create channels that has no users
    emptyChannel = channels_create("adminToken", "validchannel", True)
    userChannel = channels_create("thisUser", "validchannel", True)
    # create user and compare channels_list result with channels_list_all
    assert channels_list("thisUser") != channels_listall(result_login["adminToken"]), "users can see all lists, even if not a member"
   
# check channels_create raises input error when name is too long
def test_channels_create_too_long_name():
    with pytest.raises(InputError, match=r"channel name cannot be greater than 20 characters"):
        channels_create("something", "a_string_name_which_is_very_long_and_will_never_pass", True)