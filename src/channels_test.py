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
    assert type(channels_list("randtoken")) is dict
    assert type(channels_listall("randtoken")) is dict
    assert type(channels_create("randtoken", "somename", True)) is dict

# check channels_create adds to the total channels
def test_channels_create():
    numChannelsbefore = len(channels_listall("randtoken"))
    channels_create("randtoken", "somename", True)
    numChannelsafter = len(channels_listall("randtoken"))
    if (numChannelsbefore != numChannelsafter - 1):
        raise Exception(f"Error, channel create does not actually add a new channel to total")
    #TODO: test public/private toggle

# check if user can view only appropriate lists they have joined
def test_channels_list_user_view():
    # create user and compare channels_list result with channels_list_all
    assert True


##### try catch exceptions test
try:
    test_channels_create()
except Exception:
    print("Create new Channel function not working/implemented")