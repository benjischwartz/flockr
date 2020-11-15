import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
from check_token import jwt_given_email
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from check_reset_code import code_given_email, email_given_code

# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_exception_accesserror_inputerror(url):
    '''
    test that when an inputerror and accesserror is raised by a function, the error code of
    the response status is 400
    '''
    requests.delete(f"{url}/clear")
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    channel_details_response = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    #inputerror; since no channels have been create yet
    channel_details_response = channel_details_response.json()
    assert 'code' in channel_details_response
    assert channel_details_response['code'] == 400
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/auth/logout", json= {
        "token" : user_one['token']
        })
    #invalid token because user logged out
    channel_details_response = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    channel_details_response = channel_details_response.json()
    assert 'code' in channel_details_response
    assert channel_details_response['code'] == 400

    
def test_server_auth_register_logout_login(url):
    '''
    test a positive case for auth_register, auth_login and auth_logout
    '''
    requests.delete(f"{url}/clear") 
    user_one_register = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one_register.json()
    user_one_token = jwt_given_email("first@person.com")
    assert user_one == {'u_id' : 1 , 'token' : user_one_token}
    user_one_token = jwt_given_email("first@person.com")
    user_one_register = user_one_register.json()
    user_one_logout = requests.post(f"{url}/auth/logout", json= {
        "token" : user_one_register['token']})
    assert user_one_logout.json() == {"is_success" : True}
    user_one_login = requests.post(f"{url}/auth/login", json= {
        "email" : "first@person.com",
        "password" : "catdog"})
    user_one_login = user_one_login.json()
    user_one_login_token = jwt_given_email("first@person.com")
    assert user_one_login == {'u_id' : 1 , 'token' : user_one_login_token}

def test_server_auth_passwordreset_request_reset(url):
    '''
    test a positive case for auth_passwordreset_request and
    auth_passwordreset_reset
    '''
    requests.delete(f"{url}/clear")
    requests.post(f"{url}/auth/register", json={
        "email" : "flockrrecipient@gmail.com",   # has to be a valid email
        "password" : "catdog",
        "name_first" : "Flockr",
        "name_last" : "Example"})
    request_result = requests.post(f"{url}/auth/passwordreset/request", json={
        "email" : "flockrrecipient@gmail.com"
    })
    assert request_result.json() == {}

    r = requests.post(f"{url}/auth/passwordreset/reset", json={
        "reset_code" : code_given_email("flockrrecipient@gmail.com"),
        "new_password" : "newpassword123"})
    assert r.json() == {}

    # testing successful login
    assert(requests.post(f"{url}/auth/login", json= {
        "email" : "flockrrecipient@gmail.com",
        "password" : "newpassword123"
    }))

 
def test_server_channel_invite_details(url):    
    '''
    test a positive case for channel_invite and channel_details
    '''
    requests.delete(f"{url}/clear")
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Second",
        "name_last" : "Bloggs"
    })
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    r = requests.post(f"{url}/channel/invite", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "u_id" : 2
    })
    assert r.json() == {}
    channel_one_details = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
        })
    assert channel_one_details.json() == {
        "name": "channel_one",
        "owner_members": [
            {
                "u_id": 1,
                "name_first": "First",
                "name_last": "Bloggs",
                'profile_img_url': ''
            }
        ],
        "all_members": [
            {
                "u_id": 1,
                "name_first": "First",
                "name_last": "Bloggs",
                'profile_img_url': ''
            },
            {
                "u_id" : 2,
                "name_first" : "Second",
                "name_last" : "Bloggs",
                'profile_img_url': ''
            }
        ]
    }


def test_server_channel_join_leave(url):
    '''
    test a positive case for channel_join and channel_leave
    '''
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    user_two = user_two.json()
    requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    r = requests.post(f"{url}/channel/join", json = {
        "token" : user_two["token"],
        "channel_id" : 1
    })
    assert r.json() == {}
    channel_one_details = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    channel_one_details = channel_one_details.json()
    assert channel_one_details['all_members'] == [
            {
                "u_id": 1,
                "name_first": "Joe",
                "name_last": "Bloggs",
                'profile_img_url': ''
            },
            {
                "u_id": 2,
                "name_first": "James",
                "name_last": "Lee",
                'profile_img_url': ''
            }
        ]
    r = requests.post(f"{url}/channel/leave", json = {
        "token" : user_two["token"],
        "channel_id" : 1
    })
    assert r.json() == {}
    channel_one_details = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    channel_one_details = channel_one_details.json()
    assert channel_one_details['all_members'] == [{
                "u_id": 1,
                "name_first": "Joe",
                "name_last": "Bloggs",
                'profile_img_url': ''
            }]


def test_server_channel_addowner_removeowner(url):
    '''
    test a positive case for channel_addowner channel_removeowner
    '''
    requests.delete(f"{url}/clear")
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    r = requests.post(f"{url}/channel/addowner", json={
        "token": user_one["token"],
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    # checking the new owner is added
    initial_details = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    assert initial_details.json() == {
        "name": "channel_one", 
        "owner_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs",
                'profile_img_url': ''
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee",
                'profile_img_url': ''
            }
        ],
        "all_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs",
                'profile_img_url': ''
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee",
                'profile_img_url': ''
            }
        ],
    }

    # first user removing the second user
    r = requests.post(f"{url}/channel/removeowner", json={
        "token": user_one["token"],
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    final_details = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    # check removal of owner is successful
    assert final_details.json() == {
        "name": "channel_one", 
        "owner_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs",
                'profile_img_url': ''
            }
        ],
        "all_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs",
                'profile_img_url': ''
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee",
                'profile_img_url': ''
            }
        ],
    }


def test_server_channels_create_list_listall(url):
    '''
    test a positive case for channels_create channels_list and channels_listall
    '''
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    user_two = user_two.json()
    channel_one = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    # test channel has been created
    assert channel_one.json() == {"channel_id" : 1 } 
    channel_two = requests.post(f"{url}/channels/create", json={
        "token" : user_two["token"],
        "name" : "channel_two",
        "is_public" : True
    })
    assert channel_two.json() == {"channel_id" : 2 }
   
    # after creating channels and users, test channels_list and listall
    list_first = requests.get(f"{url}/channels/list", params={
        "token":user_one["token"]
        })
    assert list_first.json() == {
        "channels" : [
            {
                "channel_id" : 1,
                "name" : "channel_one"
            }
        ]
    }
    list_all_first =  requests.get(f"{url}/channels/listall", params={
        "token":user_one["token"]
        })
    assert list_all_first.json() == {
        "channels" : [
            {
                "channel_id" : 1,
                "name" : "channel_one"
            },
            {
                "channel_id" : 2,
                "name" : "channel_two"
            }            
        ]
    }


def test_server_channel_messages_message_send_edit_remove(url):
    '''
    test a positive case for channel_messages, message_send, message_edit
    and message_remove
    '''
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    prior_send = time()
    send_message = requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    assert send_message.json() == {"message_id" : 1}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    after_send = time()
    channel_one_messages = channel_one_messages.json()
    assert len(channel_one_messages["messages"]) == 1
    assert channel_one_messages["messages"][0]["message_id"] == 1
    assert channel_one_messages["messages"][0]["u_id"] == user_one['u_id']
    assert channel_one_messages["messages"][0]["message"] == 'Hello'
    assert channel_one_messages["messages"][0]["reacts"] == []
    assert channel_one_messages["messages"][0]["is_pinned"] == False
    assert prior_send < channel_one_messages["messages"][0]["time_created"] < after_send
    
    edit_message = requests.put(f"{url}/message/edit", json={
        "token" : user_one["token"],
        "message_id" : 1,
        "message" : "Hi world"
    })
    edit_message = edit_message.json()
    assert edit_message == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['message'] == "Hi world" 

    remove_message = requests.delete(f"{url}/message/remove", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message_id" : 1
    })
    remove_message = remove_message.json()
    assert remove_message == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    assert channel_one_messages.json() == {
        'messages' : [],
        'start' : 0,
        'end' : -1
    }

def test_server_message_sendlater(url):
    """
    testing a positive case for message_edit
    """
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    message_one = requests.post(f"{url}/message/sendlater", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello",
        "time_sent" : time() + 3600
    })
    message_one = message_one.json()
    assert message_one == {'message_id' : 1}

def test_server_message_react_unreact(url):
    """
    testing a positive case for message_react and message_unreact
    """
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    first_react = requests.post(f"{url}/message/react", json={
        "token" : user_one["token"],
        "message_id" : 1,
        "react_id" : 1
    })
    first_react = first_react.json()
    assert first_react == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['reacts'] == [{
        "react_id" : 1,
        "u_ids" : [1],
        "is_this_user_reacted": True
    }]
    first_unreact = requests.post(f"{url}/message/unreact", json={
        "token" : user_one["token"],
        "message_id" : 1,
        "react_id" : 1
    })
    first_unreact = first_unreact.json()
    assert first_unreact == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['reacts'] == []

def test_server_message_pin_unpin(url):
    """
    testing a positive case for message_pin and message_unpin
    """
    requests.delete(f"{url}/clear") 
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    first_pin = requests.post(f"{url}/message/pin", json={
        "token" : user_one["token"],
        "message_id" : 1
    })
    first_pin = first_pin.json()
    assert first_pin == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['is_pinned'] is True
    first_unpin = requests.post(f"{url}/message/unpin", json={
        "token" : user_one["token"],
        "message_id" : 1
    })
    first_unpin = first_unpin.json()
    assert first_unpin == {}
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['is_pinned'] is False
    
def test_server_user_profile_all_profile(url):
    """
    testing a positive case for user_profile, user_profile_setname, user_profile_setemail,
    user_profile_sethandle, user_profile_uploadphoto
    """
    requests.delete(f"{url}/clear")     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    token = user_one["token"]
    u_id = user_one["u_id"]
    user_one_profile = requests.get(f"{url}/user/profile?token={token}&u_id={u_id}")
    user_one_profile = user_one_profile.json()
    assert user_one_profile == { "user" : 
        {
            "u_id" : 1,
            "name_first" : "First",
            "name_last" : "Bloggs",
            "handle_str" : "firstbloggs",
            "email" : "first@person.com",
            "profile_img_url" : ''
        }
    }
    name_change = requests.put(f"{url}/user/profile/setname", json={
        "token" : user_one["token"],
        "name_first" : "New First",
        "name_last": "New Last"
    })
    assert(name_change.json() == {})
    user_one_profile = requests.get(f"{url}/user/profile", params={
        "token": user_one["token"],
        "u_id": 1
    })
    assert user_one_profile.json() == { "user" : 
        {
            "u_id": 1,
            "email": "first@person.com",
            "name_first": "New First",
            "name_last": "New Last",
            "handle_str": "firstbloggs",
            "profile_img_url" : ''
        }
    }
    email_change = requests.put(f"{url}/user/profile/setemail", json={
        "token" : user_one["token"],
        "email": "newemail@person.com"
    })
    assert email_change.json() == {}
    user_one = requests.post(f"{url}/auth/logout", json={
        "token": user_one["token"]
    })
    user_one = requests.post(f"{url}/auth/login", json={
        "email" : "newemail@person.com",
        "password" : "catdog"
    })
    user_one = user_one.json()
    user_one_profile = requests.get(f"{url}/user/profile", params={
        "token": user_one["token"],
        "u_id": 1
    })
    assert user_one_profile.json() == { 'user' : 
        {
            "u_id": 1,
            "email": "newemail@person.com",
            "name_first": "New First",
            "name_last": "New Last",
            "handle_str": "firstbloggs",
            "profile_img_url" : ''
        }
    }
    new_handle = requests.put(f"{url}/user/profile/sethandle", json={
        "token" : user_one["token"],
        "handle": "newfirst"
    })
    assert new_handle.json() == {}
    user_one_profile = requests.get(f"{url}/user/profile", params={
        "token": user_one["token"],
        "u_id": 1
    })
    assert user_one_profile.json() == { "user" : 
        {
            "u_id": 1,
            "name_first": "New First",
            "name_last": "New Last",
            "handle_str": "newfirst",
            "email": "newemail@person.com",
            "profile_img_url" : ''
        }
    }
    result = requests.post(f"{url}/user/profile/uploadphoto", json={
        "token" : user_one['token'],
        "img_url" : "https://newsroom.unsw.edu.au/sites/default/files/styles/full_width/public/thumbnails/image/04_scientia_1.jpg",
        "x_start" : 0,
        "y_start" : 0,
        "x_end" : 400,
        "y_end" : 300
    })
    assert(result.json() == {})
    
    user_one_profile = requests.get(f"{url}/user/profile", params={
        "token": user_one["token"],
        "u_id": 1
    })
    user_one_profile = user_one_profile.json()
    profile_img_url = user_one_profile['user']['profile_img_url']
    image = requests.get(profile_img_url)
    
    assert(image.status_code == 200)

def test_server_users_all(url):
    """
    testing a positive case for users_all
    """ 
    requests.delete(f"{url}/clear")     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    
    token = user_one["token"]
    users_list = requests.get(f"{url}/users/all?token={token}")
    users_list = users_list.json()
    assert users_list == {"users" : 
        [{
            "handle_str": "firstbloggs",
            "u_id" : 1,
            "name_first" : "First",
            "name_last" : "Bloggs",
            "email" : "first@person.com",
            "profile_img_url" : ''
        }]
    }

def test_server_admin_permissions_change(url):
    """
    testing a positive case for changing admin privileges
    user one makes user two admin, then user two removes user one
    works if test does not throw error
    """
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
    "email" : "first@person.com",
    "password" : "catdog",
    "name_first" : "Joe",
    "name_last" : "Bloggs"})
    user_one = user_one.json()
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    user_two = user_two.json()
    made_admin = requests.post(f"{url}/admin/userpermission/change", json={
        "token": user_one["token"],
        "u_id" : 2,
        "permission_id" : 1})
    assert made_admin.json() == {}
    remove_admin = requests.post(f"{url}/admin/userpermission/change", json={
        "token": user_two["token"],
        "u_id" : 1,
        "permission_id" : 2})
    assert remove_admin.json() == {}

def test_server_search_single_message(url):
    """
    testing a positive case for search 
    """
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    send_message = requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello World"
    })
    assert send_message.json() == {"message_id" : 1}

    # get variables for input into search
    token = user_one["token"]
    query_str = "Hello"

    search_result = requests.get(f"{url}/search?token={token}&query_str={query_str}")
    search_result = search_result.json()
    assert search_result['messages'][0]['message_id'] == 1
    assert search_result['messages'][0]['u_id'] == 1
    assert search_result['messages'][0]['message'] == "Hello World"
    assert search_result['messages'][0]['reacts'] == []
    assert search_result['messages'][0]['is_pinned'] == False

def test_server_standup_start(url):
    """
    testing a positive case for standup_start 
    """
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    time_before = int((datetime.now() + timedelta(seconds=10)).timestamp())
    message_standup = requests.post(f"{url}/standup/start", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "length" : 10
    })
    message_standup = message_standup.json()
    time_after = int((datetime.now() + timedelta(seconds=10)).timestamp())
    assert time_before <= message_standup['time_finish'] <= time_after

def test_server_standup_active(url):
    """
    testing a positive case for standup_active 
    """
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    channel_one = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    channel_one = channel_one.json()

    channel_one_messages = requests.get(f"{url}/standup/active", params={
        "token" : user_one["token"],
        "channel_id" : channel_one["channel_id"]
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages == {
        'is_active' : False,
        'time_finish' : None
    }

def test_server_standup_send(url):
    """
    testing a positive case for standup_send 
    """
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    channel_one = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    channel_one = channel_one.json()
    requests.post(f"{url}/standup/start", json={
        "token" : user_one["token"],
        "channel_id" : channel_one["channel_id"],
        "length" : 10
    })
    message_one = requests.post(f"{url}/standup/send", json={
        "token" : user_one["token"], 
        "channel_id" : channel_one["channel_id"],
        "message" : "hello"
    })

    message_one = message_one.json()
    assert message_one == {}
    
def test_server_clear(url):
    requests.delete(f"{url}/clear")      
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    list_all_first =  requests.get(f"{url}/channels/listall", params={
        "token": user_one["token"]
        })
    assert list_all_first.json() == {
        "channels" : [
            {
                "channel_id" : 1,
                "name" : "channel_one"
            }
        ]
    }    

    clear = requests.delete(f"{url}/clear")
    assert(clear.json() == {})

    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    user_two = user_two.json()
    token = user_two["token"]

    r = requests.get(f"{url}/users/all?token={token}")

    r = r.json()
    assert r == { "users" : 
        [{
            "handle_str" : "marybrown",
            "u_id" : 1,
            "name_first" : "Mary",
            "name_last" : "Brown",
            "email" : "second@person.com",
            "profile_img_url" : ''
        }]
    }

    list_all_first =  requests.get(f"{url}/channels/listall", params={
        "token":user_two["token"]
        })
    assert list_all_first.json() == {
        "channels" : []
    }        
