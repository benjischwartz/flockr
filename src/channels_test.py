# test file for the channels functions
# channels, plural, is a data struct looking at the channels globally
# whereas channel, singular, are user actions within the channel
# TODO change asserts to exceptions --> meaningful errors

import channels
import pytest
from error import InputError

# check return values are valid types
# add more to check the dict key values
def test_return_type():
    assert type(channels.channels_list("randtoken")) is dict
    assert type(channels.channels_listall("randtoken")) is dict
    assert type(channels.channels_create("randtoken", "somename", True)) is dict

# check channels_create adds to the total channels
def test_channels_create():
    numChannelsbefore = len(channels.channels_listall("randtoken"))
    channels.channels_create("randtoken", "somename", True)
    numChannelsafter = len(channels.channels_listall("randtoken"))
    assert(numChannelsbefore == numChannelsafter - 1)
    #TODO: test public/private toggle

# check if user can view only appropriate lists they have joined
def test_channels_list_user_view():
    # create user and compare channels_list result with channels_list_all
    assert True