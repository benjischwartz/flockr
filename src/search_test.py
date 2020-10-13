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
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    user_two = auth_register("second@user.com", "password", "Joe", "Bloggs")
    new_channel = channels_create(user_two['token'],"channel_one", True)
    message_send(user_two['token'], new_channel['channel_id'], "this is a message")
    # return empty dictionary as there is no match
    assert search(user_one['token'], "this is") == []

# test expecting multiple string matches in same channel
def test_single_channel_multiple_matches():
    clear()

# test expecting multiple string matches in different channels
def test_multiple_channel_multiple_matches():
    clear()

# test no matches with query string not found
def test_no_matches():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    assert search(user_one['token'], "robin") == []
    

# test query > 1000 characters returns {}
def test_long_query():
    clear()
    user_one = auth_register("first@user.com", "password", "Jane", "Applebaum")
    new_channel = channels_create(user_one['token'],"channel_one", True)
    message_send(user_one['token'], new_channel['channel_id'], "this is a message")
    assert search(user_one['token'], """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nunc augue, rhoncus id sapien et, tempor pellentesque risus. Nullam ultricies, odio eget auctor eleifend, eros felis gravida ligula, et interdum ex eros sed ipsum. Etiam non metus fermentum, maximus augue vel, ultrices odio. Nunc dignissim odio id nisi suscipit, ac feugiat ligula consectetur. Phasellus blandit ut eros a aliquet. Donec consectetur eu nisl vel sagittis. Vestibulum vehicula et neque eget commodo. Cras a est convallis, posuere erat ac, scelerisque sem.
    Phasellus consectetur venenatis feugiat. Mauris semper vel turpis et tincidunt. Cras ultricies purus eget odio facilisis, a laoreet nisl finibus. Nullam erat sapien, cursus sed enim quis, facilisis pharetra arcu. Fusce vitae laoreet turpis, id varius velit. Morbi volutpat elit ut dui tempor vestibulum. Fusce vel ipsum a mi malesuada maximus. Suspendisse potenti. Sed sodales neque vitae odio fringilla, vitae blandit massa interdum. In eget malesuada mi. Duis accumsan urna felis, vitae porttitor magna interdum sed. Nulla suscipit ante eu libero pretium, elementum condimentum quam finibus. Cras rutrum ullamcorper tincidunt. Mauris commodo dolor nec tortor molestie, ullamcorper blandit lorem ornare. Fusce a elit elit. Cras fermentum, erat sit amet accumsan bibendum, tortor magna rhoncus libero, in lobortis nibh lacus finibus ipsum.
    Vivamus leo libero, placerat et tellus sed, vehicula aliquam arcu. Suspendisse quis euismod urna, non euismod sem. Aliquam lobortis urna nisi, vel molestie risus placerat quis. Proin vestibulum nisi sed interdum cursus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras porta pulvinar mauris. Pellentesque et ex eget tortor facilisis convallis rutrum sed purus. Praesent vel varius urna. Proin hendrerit luctus nisl, ut auctor lacus viverra quis. Integer velit magna, lacinia eu luctus sit amet, porta volutpat ipsum. Sed feugiat arcu quis lacinia rhoncus. Nunc auctor nulla eu nunc vulputate, sed eleifend nibh condimentum. Nam mollis tellus a tellus egestas venenatis. Integer vulputate, massa eget sagittis cursus, tellus ipsum consectetur lacus, lobortis aliquam ex enim in tellus. Aliquam bibendum rutrum purus ut imperdiet. Nam ut placerat felis.
    Nullam id lectus leo. Proin quis finibus purus. Nunc fermentum dignissim vulputate. Cras condimentum nisi a eros sodales convallis. Vestibulum at nisi nisi. Quisque tempus dolor dapibus fringilla scelerisque. In vel risus aliquet, vestibulum lorem non, lobortis justo. Praesent congue velit risus, sed iaculis leo imperdiet non. Suspendisse consectetur at dolor mattis lacinia. Donec eu elit eu turpis aliquam molestie. Sed sagittis enim vitae est iaculis, ut porta arcu venenatis.
    Aliquam sed vehicula dolor. Donec fringilla ultricies suscipit. Integer scelerisque lacinia dui fermentum tempus. Vestibulum bibendum mauris a suscipit vehicula. Donec eget ultrices odio. Cras vitae diam a diam porttitor tristique in laoreet magna. In et lectus eros. Pellentesque sed dolor eu eros porttitor fringilla nec pellentesque nulla. Quisque laoreet sit amet dui vel convallis. Quisque tristique laoreet metus, vel vulputate magna commodo et. Nam tempor arcu vel dolor tempus, vitae fermentum purus rutrum. Mauris tempor venenatis sollicitudin. Ut nulla elit, tincidunt lobortis pharetra finibus, ultricies eu lectus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Ut faucibus elit venenatis scelerisque egestas. Nulla facilisi.
    """) == []
