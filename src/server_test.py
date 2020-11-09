import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
import urllib
from other import clear
from check_token import jwt_given_email
from flask_mail import Mail, Message
from check_reset_code import code_given_email, email_given_code
import data
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

def test_exception_accesserror(url):
    '''
    test that when an accesserror is raised by a function, the error code of
    the response status is 400
    this test uses an invalid token passed to channel_details to raise the 
    accesserror
    '''
    
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/auth/logout", json= {
        "token" : user_one['token']
        })
    channel_details_response = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    channel_details_response = channel_details_response.json()
    assert 'code' in channel_details_response
    assert channel_details_response['code'] == 400

def test_exception_inputerror(url):
    '''
    test that when an inputerror is raised by a function, the error code of
    the response status is 400
    this test uses an invalid channel_id passed to channel_details to raise an 
    inputerror; since no channels have been created, any channel_id is invalid
    '''
    
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
    channel_details_response = channel_details_response.json()
    assert 'code' in channel_details_response
    assert channel_details_response['code'] == 400

    
def test_server_auth_register(url):
    '''
    test a positive case for auth_register
    '''
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    user_one_token = jwt_given_email("first@person.com")
    assert user_one == {'u_id' : 1 , 'token' : user_one_token}
    
def test_server_auth_logout_login(url):
    '''
    test a positive case for auth_login and auth_logout
    '''
     
    user_one_register = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
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
        "code" : code_given_email("flockrrecipient@gmail.com"),
        "new_password" : "newpassword123"})
    assert r.json() == {}

    # testing successful login
    assert(requests.post(f"{url}/auth/login", json= {
        "email" : "flockrrecipient@gmail.com",
        "password" : "newpassword123"
    }))

    #TODO: test that there is an outgoing email.

 
def test_server_channel_invite(url):    
    '''
    test a positive case for channel_invite
    '''
     
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
                "name_last": "Bloggs"
            }
        ],
        "all_members": [
            {
                "u_id": 1,
                "name_first": "First",
                "name_last": "Bloggs"
            },
            {
                "u_id" : 2,
                "name_first" : "Second",
                "name_last" : "Bloggs"
            }
        ]
    }
    
def test_server_channel_details(url):
    '''
    test a positive case for channel_details
    '''
     
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
                "name_last": "Bloggs"
            }
        ],
        "all_members": [
            {
                "u_id": 1,
                "name_first": "First",
                "name_last": "Bloggs"
            }
        ]
    }
    
def test_server_channel_messages(url):
    '''
    test a positive case for channel_messages
    '''
     
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
    requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
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
    assert prior_send < channel_one_messages["messages"][0]["time_created"] < after_send


def test_server_channel_join(url):
    '''
    test a positive case for channel_join
    '''
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Second",
        "name_last" : "Bloggs"})
    user_two = user_two.json()
    j = requests.post(f"{url}/channel/join", json = {
        "token" : user_two["token"],
        "channel_id" : 1
    })
    assert j.json() == {}
    channel_one_details = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : 1
    })
    channel_one_details = channel_one_details.json()
    assert channel_one_details['all_members'] == [
            {
                "u_id": 1,
                "name_first": "First",
                "name_last": "Bloggs"
            },
            {
                "u_id": 2,
                "name_first": "Second",
                "name_last": "Bloggs"
            }
        ]
        
    

def test_server_channel_leave(url):
    '''
    test a positive case for channel_leave
    '''
     
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
                "name_last": "Bloggs"
            }]
        

def test_server_channel_addowner(url):
    '''
    test a positive case for channel_addowner
    '''
    
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
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    user_two = user_two.json()
    r = requests.post(f"{url}/channel/addowner", json={
        "token": user_one["token"],
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    channel_one_details = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    channel_one_details = channel_one_details.json()
    assert channel_one_details == {
        "name": "channel_one", 
        "owner_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs"
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee"
            }
        ],
        "all_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs"
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee"
            }
        ],
    }

def test_server_channel_removeowner(url):
    '''
    test a positive case for channel_removeowner
    '''

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
    # checking the owners of the channel prior to removeowner
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
                "name_last" : "Bloggs"
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee"
            }
        ],
        "all_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs"
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee"
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
    assert final_details.json() == {
        "name": "channel_one", 
        "owner_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs"
            }
        ],
        "all_members": [
            {
                "u_id": 1, 
                "name_first" : "Joe",
                "name_last" : "Bloggs"
            },
            {
                "u_id": 2, 
                "name_first" : "James",
                "name_last" : "Lee"
            }
        ],
    }

def test_server_channels_create_public(url):
    '''
    test a positive case for channels_create creatubg a public channel
    '''

    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    r = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    assert r.json() == {"channel_id" : 1 }

def test_server_channels_list_listall(url):
    '''
    test a positive case for channels_list and channels_listall
    '''
     
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

     
def test_server_message_send(url):
    """
    Testing a positive case for message_send 
    """
     
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
        "message" : "Hello"
    })
    assert send_message.json() == {"message_id" : 1}
    
def test_server_message_remove(url):
    """
    testing a positive case for message_remove
    """
     
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
    requests.delete(f"{url}/message/remove", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message_id" : 1
    })
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    },)
    assert channel_one_messages.json() == {
        'messages' : [],
        'start' : 0,
        'end' : -1
    }

def test_server_message_edit(url):
    """
    testing a positive case for message_edit
    """
     
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
    requests.put(f"{url}/message/edit", json={
        "token" : user_one["token"],
        "message_id" : 1,
        "message" : "Hi world"
    })
    channel_one_messages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    channel_one_messages = channel_one_messages.json()
    assert channel_one_messages['messages'][0]['message'] == "Hi world" 

def test_server_user_profile(url):
    """
    testing a positive case for user_profile
    """
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
            "email" : "first@person.com"
        }
    }

def test_server_user_profile_setname(url):
    """
    testing a positive case for user_profile_setname
    """     

    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()

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
            "handle_str": "firstbloggs"
        }
    }


def test_server_user_profile_setemail(url):
    """
    testing a positive case for user_profile_setemail
    """    
  
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    
    email_change = requests.put(f"{url}/user/profile/setemail", json={
        "token" : user_one["token"],
        "email": "newemail@person.com"
    })
    assert email_change.json() == {}

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
            "name_first": "First",
            "name_last": "Bloggs",
            "handle_str": "firstbloggs"
        }
    }

def test_user_profile_sethandle(url):
    """
    testing a positive case for user_profile_sethandle
    """ 
    
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
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
            "name_first": "First",
            "name_last": "Bloggs",
            "handle_str": "newfirst",
            "email": "first@person.com"
        }
    }
   
def test_users_all(url):
    """
    testing a positive case for users_all
    """ 
    
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
            "email" : "first@person.com"
        }]
    }

def test_admin_permissions_change(url):
    """
    testing a positive case for changing admin privileges
    user one makes user two admin, then user two removes user one
    works if test does not throw error
    """
     
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

def test_search_single_message(url):
     
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
    
def test_clear(url):
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
            "email" : "second@person.com"
        }]
    }

    list_all_first =  requests.get(f"{url}/channels/listall", params={
        "token":user_two["token"]
        })
    assert list_all_first.json() == {
        "channels" : []
    }        
