from search import search
from other import clear
import error
import pytest
from channels import channels_create, channels_list
from auth import auth_register

# test for Access Error and Invalid Token
def test_access_error():
    clear()
    with pytest.raises(error.AccessError):
        search("invalid@token.com.au","this is the query string")

# test for positive case, single message, single channel
def test_single_channel_single_message():
    clear()
    # TODO - register user and create channel
    # create a single message in the channel
    # TODO - call channels_list to get list of every channel user is part of
    # TODO - Loop through every element each channel

# test where search query matches in channel user NOT part of
# expect this message is not in the return of search()
def test_pattern_match_unavailable_channel():
    clear()

# test expecting multiple string matches in same channel
def test_single_channel_multiple_matches():
    clear()

# test expecting multiple string matches in different channels
def test_multiple_channel_multiple_matches():
    clear()

# test no matches
def test_no_matches():
    clear()

# test query > 1000 characters. raise input error???