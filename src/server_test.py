import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
import urllib
from other import clear
from check_token import email_given_jwt
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

def test_auth_register(url):
    """
    Testing server auth_register
    """
     
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    print(r.json())
    r = r.json()
    assert email_given_jwt(r['token']) == "first@person.com"
    # assert r.json() == {"u_id" : 1, "token" : "first@person.com"}

def test_auth_logout_login(url):
    """
    Testing server auth_login
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    # assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    r = requests.post(f"{url}/auth/logout", json= {
        "token" : user_one['token']})
        # TODO: update token after hashing
    assert r.json() == {"is_success" : True}
    r = requests.post(f"{url}/auth/login", json= {
        "email" : "first@person.com",
        "password" : "catdog"})
    # assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    # assert r.json() == {"token" : "first@person.com", "u_id" : 1}
        # TODO: update token after hashing

def test_channel_invite(url):    
    """
    Testing channel_invite
    """
     
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
        "name" : "randChannel",
        "is_public" : True
    })
    r = requests.post(f"{url}/channel/invite", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "u_id" : 2
    })
    assert r.json() == {}
    token = user_one['token']
    channel_id = 1
    randChannel_details = requests.get(f"{url}/channel/details?token={token}&channel_id={channel_id}")
    assert randChannel_details.json() == {
        "name": "randChannel",
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
def test_channel_details(url):
    """
    Testing channel_details
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert user_one == { "token": "first@person.com", "u_id" : 1}
    channel_one = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "randChannel",
        "is_public" : True
    })
    assert channel_one.json() == {"channel_id" : 1}
    randChannel_details = requests.get(f"{url}/channel/details", params={
        "token" : user_one["token"],
        "channel_id" : channel_one.json()["channel_id"]
    })
    assert randChannel_details.json() == {    
        "name": "randChannel",
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
    
def test_channel_messages_one_message(url):
    """
    Testing channel_messages with one message
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
    prior_send = time()
    requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    chanMessages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    after_send = time()
    chanMessages = chanMessages.json()
    assert len(chanMessages["messages"]) == 1
    assert chanMessages["messages"][0]["message_id"] == 1
    assert chanMessages["messages"][0]["u_id"] == user_one['u_id']
    assert chanMessages["messages"][0]["message"] == 'Hello'
    assert prior_send < chanMessages["messages"][0]["time_created"] < after_send
    
def test_channels_create_public(url):
    """
    Testing creating a public channel
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    # TODO: update token email after hashing done
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}
    # after register, create channel
    r = requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    assert r.json() == {"channel_id" : 1 }

def test_channels_list_listall(url):
    """
    Create two users to test channels_list and channels_listall
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    # TODO: update token email after hashing done
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    # TODO: update token email after hashing done
    user_two = user_two.json()
    assert user_two == {"u_id" : 2, "token" : "second@person.com"}
    # after register, create channels
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
   
    # after creating channels, test channels_list and listall
    list_first = requests.get(f"{url}/channels/list", params={"token":user_one["token"]})
    assert list_first.json() == {
        "channels" : [
            {
                "channel_id" : 1,
                "name" : "channel_one"
            }
        ]
    }
    list_all_first =  requests.get(f"{url}/channels/listall", params={"token":user_one["token"]})
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

def test_channel_join(url):
    """
    Testing server channel_join
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"} 
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channelname",
        "is_public" : True
    })
    assert channelid.json() == {'channel_id' : 1}
    channelidj = channelid.json()
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    user_two = user_two.json()
    assert user_two == {"u_id" : 2, "token" : "second@person.com"}
    j = requests.post(f"{url}/channel/join", json = {
        "token" : user_two["token"],
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}

def test_channel_leave(url):
    """
    Test for channel_leave function
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}

    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    assert user_two.json() == {"u_id" : 2, "token" : "second@person.com"}
    user_two = user_two.json()
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channelname",
        "is_public" : True
    })
    assert channelid.json() == {'channel_id' : 1}

    channelidj = channelid.json()
    j = requests.post(f"{url}/channel/join", json = {
        "token" : user_two["token"],
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}

    j = requests.post(f"{url}/channel/leave", json = {
        "token" : user_two["token"],
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}


def test_channel_addowner(url):
     
    #Registering First User
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}

    #Creating a Channel with the First User
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channelname",
        "is_public" : True
    })
    assert channelid.json() == {'channel_id' : 1}

    #Registering Second User
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    user_two = user_two.json()
    assert user_two == {"u_id" : 2, "token" : user_two["token"]}
    
    #First User Adding Second User as Owner
    r = requests.post(f"{url}/channel/addowner", json={
        "token": user_one["token"],
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    #Checking the Owners
    r = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    assert r.json() == {
        "name": "channelname", 
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

def test_channel_removeowner(url):
     
    #Registering First User
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}

    #Creating a Channel with the First User
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : user_one["token"],
        "name" : "channelname",
        "is_public" : True
    })
    assert channelid.json() == {'channel_id' : 1}

    #Registering Second User
    r = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    
    #First User Adding Second User as Owner
    r = requests.post(f"{url}/channel/addowner", json={
        "token": user_one["token"],
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}

    #Checking the Owners
    r = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    assert r.json() == {
        "name": "channelname", 
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

    #First User Removing Second User
    r = requests.post(f"{url}/channel/removeowner", json={
        "token": "first@person.com",
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    #Checking Owner Members
    r = requests.get(f"{url}/channel/details", params={
        "token": user_one["token"],
        "channel_id": 1,
    })
    assert r.json() == {
        "name": "channelname", 
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

def test_admin_permissions_change(url):
    """
    Testing changing admin privileges
    user one makes user two admin, then user two removes user one
    Works if test does not throw error
    """
     
    user_one = requests.post(f"{url}/auth/register", json={
    "email" : "first@person.com",
    "password" : "catdog",
    "name_first" : "Joe",
    "name_last" : "Bloggs"})
    # TODO: update token email after hashing done
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    # TODO: update token email after hashing done
    user_two = user_two.json()
    assert user_two == {"u_id" : 2, "token" : "second@person.com"}
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
     
def test_message_send(url):
    """
    Testing message_send 
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
    sendMessage = requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    assert sendMessage.json() == {"message_id" : 1}
    
def test_message_remove(url):
    """
    testing message_remove
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
    r = requests.delete(f"{url}/message/remove", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message_id" : 1
    })
    chanMessages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    },)
    assert chanMessages.json() == {
        'messages' : [],
        'start' : 0,
        'end' : -1
    }

def test_message_edit(url):
    """
    testing message_edit
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
    r = requests.put(f"{url}/message/edit", json={
        "token" : user_one["token"],
        "message_id" : 1,
        "message" : "Hi world"
    })
    chanMessages = requests.get(f"{url}/channel/messages", params={
        "token" : user_one["token"],
        "channel_id" : 1,
        "start" : 0
    })
    chanMessages = chanMessages.json()
    assert chanMessages['messages'][0]['message'] == "Hi world" 
    
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
    sendMessage = requests.post(f"{url}/message/send", json={
        "token" : user_one["token"],
        "channel_id" : 1,
        "message" : "Hello World"
    })
    assert sendMessage.json() == {"message_id" : 1}

    # get variables for input into search
    token = user_one["token"]
    query_str = "Hello"

    searchResult = requests.get(f"{url}/search?token={token}&query_str={query_str}")
    searchResult = searchResult.json()
    assert len(searchResult) == 1
    assert searchResult[0]['message_id'] == 1
    assert searchResult[0]['u_id'] == 1
    assert searchResult[0]['message'] == "Hello World"

def test_user_profile(url):
    
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}

    #variable for looking input
    token = user_one["token"]
    u_id = user_one["u_id"]

    r = requests.get(f"{url}/user/profile?token={token}&u_id={u_id}")
    rj = r.json()
    assert rj == {
        "u_id" : 1,
        "name_first" : "First",
        "name_last" : "Bloggs",
        "handle" : "firstbloggs",
        "email" : "first@person.com"
    }

def test_user_profile_setname(url):
     
    #Register First User
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert user_one == {"u_id" : 1, "token" : "first@person.com"}
    #First User Changes Name
    nameChange = requests.put(f"{url}/user/profile/setname", json={
        "token" : user_one["token"],
        "name_first" : "New First",
        "name_last": "New Last"
    })
    assert(nameChange.json() == {})
    '''
    userProfile = requests.get(f"{url}/user/profile", params={
        "token": "first@person.com",
        "u_id": 1
    })
    assert(userProfile.json() == {
        "user_id": 1,
        "email": "first@person.com",
        "name_first": "New First",
        "name_last": "New Last",
        "handle": "firstbloggs"
    })
    '''

def test_user_profile_setemail(url):
     
    #Register First User
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert(user_one == {"u_id" : 1, "token" : "first@person.com"})
    #First User Changes Name
    nameChange = requests.put(f"{url}/user/profile/setemail", json={
        "token" : user_one["token"],
        "email": "newemail@person.com"
    })
    assert(nameChange.json() == {})
    '''
    userProfile = requests.get(f"{url}/user/profile", params={
        "token": "first@person.com",
        "u_id": 1
    })
    assert(userProfile.json() == {
        "user_id": 1,
        "email": "newemail@person.com",
        "name_first": "First",
        "name_last": "Bloggs",
        "handle": "firstbloggs"
    })
    '''

def test_user_profile_sethandle(url):
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert(user_one == {"u_id" : 1, "token" : "first@person.com"})    

    newhandle = requests.put(f"{url}/user/profile/sethandle", json={
        "token" : user_one["token"],
        "handle": "newfirst"
    })
    assert(newhandle.json() == {})

    '''
    userProfile = requests.get(f"{url}/user/profile", params={
        "token": "first@person.com",
        "u_id": 1
    })
    assert(userProfile.json() == {
        "user_id": 1,
        "name_first": "First",
        "name_last": "Bloggs",
        "handle": "firstbloggs"
        "email": "newemail@person.com",
    })
    '''

def test_users_all(url):
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert(user_one == {"u_id" : 1, "token" : "first@person.com"})    

    #variable for looking input
    token = user_one["token"]

    r = requests.get(f"{url}/users/all?token={token}")
    rj = r.json()
    assert(rj == {
        "first@person.com" : {
            'handle': 'firstbloggs',
            "u_id" : 1,
            "name_first" : "First",
            "name_last" : "Bloggs"
        }
    })


def test_clear(url):
    user_one = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    user_one = user_one.json()
    assert(user_one == {"u_id" : 1, "token" : "first@person.com"})

    requests.post(f"{url}/channels/create", json={
        "token" : user_one["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    list_all_first =  requests.get(f"{url}/channels/listall", params={"token":"first@person.com"})
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

    rj = r.json()
    assert(rj == {
        "second@person.com" : {
            "handle" : "marybrown",
            "u_id" : 1,
            "name_first" : "Mary",
            "name_last" : "Brown"
            #"handle" : rj['u_id']
        }
    })

    list_all_first =  requests.get(f"{url}/channels/listall", params={"token":user_two["token"]})
    assert list_all_first.json() == {
        "channels" : []
    }        
