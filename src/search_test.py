from search import search
from other import clear
import error
import pytest
from channels import channels_create, channels_list
from auth import auth_register
from message import message_send

# test for Access Error and Invalid Token
def test_access_error():
    clear()
    with pytest.raises(error.AccessError):
        search("invalid@token.com.au","this is the query string")

# test for positive case, single message, single channel
def test_single_channel_single_message():
    clear()
    # register user and create public channel
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    # create a single message in the channel
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    # check one message is matched
    assert len(search(user_one['token'], "this is")) == 1, "does not return expected number of messages"
    assert len(search(user_one['token'], "this is a message")) == 1, "does not return expected number of messages"

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