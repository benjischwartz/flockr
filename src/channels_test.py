# test file for the channels functions
# channels, plural, is a data struct looking at the channels globally
# whereas channel, singular, are user actions within the channel

from channels import channels_listall, channels_list, channels_create
from auth import auth_register
import pytest
from error import InputError, AccessError
from other import clear

# Not a lot of value from checking return types, better to check the actual
# data, implicitly verifying the return type at the same time.
# check return values are valid types
# add more to check the dict key values
def test_return_type():
    # clear database and register new dummy users for testing
    clear()
    # As discussed, names not wrong per se but better to use more emblematic data
    # This would also (slighly) improve readability
    userOne = auth_register("first@example.com", "password1234", " ", " ")
    userTwo = auth_register("second@example.com", "password1234", " ", " ")
    userThree = auth_register("third@example.com", "password1234", " ", " ")
    # check types
    assert(type(channels_list("first@example.com")) is dict) 
    assert(type(channels_listall("second@example.com")) is dict)
    assert(type(channels_create("third@example.com", "somename", True)) is dict)

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
    assert channels_listall == {
        ...
    }

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
    emptyChannel = channels_create(userOne['token'], "validchannel1", True)
    userChannel = channels_create(userTwo['token'], "validchannel2", True)
    assert channels_list(userOne['token']) == {
        ...
    }
    
# check channels_create raises input error when name is too long
def test_channels_create_too_long_name():
    # clear database and register new dummy users for testing
    clear()
    userThree = auth_register("third@example.com", "password1234", " ", " ")
    with pytest.raises(InputError):
        channels_create(userThree['token'], "a_string_name_which_is_very_long_and_will_never_pass", True)

