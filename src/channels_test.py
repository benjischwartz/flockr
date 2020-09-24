# test file for the channels functions
# channels, plural, is a data struct looking at the channels globally
# whereas channel, singular, are user actions within the channel
# TODO change asserts to exceptions --> meaningful errors

from channels import channels_listall, channels_list, channels_create
import pytest
from error import InputError

# check return values are valid types
# add more to check the dict key values
def test_return_type():
    assert(type(channels_list("randtoken")) is dict) 
    assert(type(channels_listall("randtoken")) is dict)
    assert(type(channels_create("randtoken", "somename", True)) is dict)

# TODO: check if user can view only appropriate lists they have joined
def test_channels_list_user_view():
    # create user and compare channels_list result with channels_list_all
    assert False, "not implemented: channels_list restict only to users within each channel"


# check channels_create adds to the total channel
##### pre-implement should raise exception
def test_channels_create_too_long_name():
    with pytest.raises(InputError, match=r"channel name cannot be greater than 20 characters"):
        channels_create("something", "a_string_name_which_is_very_long_and_will_never_pass", True)
    
#TODO: check type of channel: public/private is value
def test_channels_create_private_public():
    assert False, "not implemented: distinction between public and private channels for channels_create"