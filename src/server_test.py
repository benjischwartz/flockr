import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep, time
import requests
import urllib
from other import clear

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
    # TODO: update token email after hashing done
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}

def test_auth_logout_login(url):
    """
    Testing server auth_login
    """
     
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    r = requests.post(f"{url}/auth/logout", json= {
        "token" : "first@person.com"})
        # TODO: update token after hashing
    assert r.json() == {"is_success" : True}
    r = requests.post(f"{url}/auth/login", json= {
        "email" : "first@person.com",
        "password" : "catdog"})
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    assert r.json() == {"token" : "first@person.com", "u_id" : 1}
        # TODO: update token after hashing

def test_channel_invite(url):    
    """
    Testing channel_invite
    """
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Second",
        "name_last" : "Bloggs"
    })
    requests.post(f"{url}/channels/create", json={
        "token" : userOne["token"],
        "name" : "randChannel",
        "is_public" : True
    })
    r = requests.post(f"{url}/channel/invite", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "u_id" : 2
    })
    assert r.json() == {}
    randChannel_details = requests.get(f"{url}/channel/details", json={
        "token" : userOne["token"],
        "channel_id" : 1
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
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : userOne["token"],
        "name" : "randChannel",
        "is_public" : True
    })
    randChannel_details = requests.get(f"{url}/channel/details", json={
        "token" : userOne["token"],
        "channel_id" : 1
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
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : "first@person.com",
        "name" : "channel_one",
        "is_public" : True
    })
    prior_send = time()
    requests.post(f"{url}/message/send", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    chanMessages = requests.get(f"{url}/channel/messages", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "start" : 0
    })
    after_send = time()
    chanMessages = chanMessages.json()
    assert len(chanMessages["messages"]) == 1
    assert chanMessages["messages"][0]["message_id"] == 1
    assert chanMessages["messages"][0]["u_id"] == userOne['u_id']
    assert chanMessages["messages"][0]["message"] == 'Hello'
    assert prior_send < chanMessages["messages"][0]["time_created"] < after_send
    
def test_channels_create_public(url):
    """
    Testing creating a public channel
    """
     
    r = requests.post(f"{url}/auth/register", json={
    "email" : "first@person.com",
    "password" : "catdog",
    "name_first" : "Joe",
    "name_last" : "Bloggs"})
    # TODO: update token email after hashing done
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    # after register, create channel
    r = requests.post(f"{url}/channels/create", json={
        "token" : "first@person.com",
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
    assert user_one.json() == {"u_id" : 1, "token" : "first@person.com"}
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    # TODO: update token email after hashing done
    assert user_two.json() == {"u_id" : 2, "token" : "second@person.com"}
    # after register, create channels
    channel_one = requests.post(f"{url}/channels/create", json={
        "token" : "first@person.com",
        "name" : "channel_one",
        "is_public" : True
    })
    assert channel_one.json() == {"channel_id" : 1 } 
    channel_two = requests.post(f"{url}/channels/create", json={
        "token" : "second@person.com",
        "name" : "channel_two",
        "is_public" : True
    })
    assert channel_two.json() == {"channel_id" : 2 } 
    # after creating channels, test channels_list and listall
    list_first = requests.get(f"{url}/channels/list", json={"token":"first@person.com"})
    assert list_first.json() == {
        "channels" : [
            {
                "channel_id" : 1,
                "name" : "channel_one"
            }
        ]
    }
    list_all_first =  requests.get(f"{url}/channels/listall", json={"token":"first@person.com"})
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
     
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}
    # TODO: update token email after hashing done
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : "first@person.com",
        "name" : "channelname",
        "is_public" : True
    })
    r = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    assert channelid.json() == {'channel_id' : 1}
    channelidj = channelid.json()
    j = requests.post(f"{url}/channel/join", json = {
        "token" : "second@person.com",
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}

def test_channel_leave(url):
    """
    Test for channel_leave function
    """
     
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}

    r = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "James",
        "name_last" : "Lee"})
    assert r.json() == {"u_id" : 2, "token" : "second@person.com"}

    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : "first@person.com",
        "name" : "channelname",
        "is_public" : True
    })
    assert channelid.json() == {'channel_id' : 1}

    channelidj = channelid.json()
    j = requests.post(f"{url}/channel/join", json = {
        "token" : "second@person.com",
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}

    j = requests.post(f"{url}/channel/leave", json = {
        "token" : "second@person.com",
        "channel_id" : channelidj["channel_id"]
    })
    assert j.json() == {}


def test_channel_addowner(url):
     
    #Registering First User
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}

    #Creating a Channel with the First User
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : "first@person.com",
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
        "token": "first@person.com",
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}
    #Checking the Owners
    r = requests.get(f"{url}/channel/details", json={
        "token": "first@person.com",
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
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"}

    #Creating a Channel with the First User
    channelid = requests.post(f"{url}/channels/create", json = {
        "token" : "first@person.com",
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
        "token": "first@person.com",
        "channel_id": 1,
        "u_id": 2,
    })
    assert r.json() == {}

    #Checking the Owners
    r = requests.get(f"{url}/channel/details", json={
        "token": "first@person.com",
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
    r = requests.get(f"{url}/channel/details", json={
        "token": "first@person.com",
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
    assert user_one.json() == {"u_id" : 1, "token" : "first@person.com"}
    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    # TODO: update token email after hashing done
    assert user_two.json() == {"u_id" : 2, "token" : "second@person.com"}
    made_admin = requests.post(f"{url}/admin/userpermission/change", json={
        "token": "first@person.com",
        "u_id" : 2,
        "permission_id" : 1})
    assert made_admin.json() == {}
    remove_admin = requests.post(f"{url}/admin/userpermission/change", json={
        "token": "second@person.com",
        "u_id" : 1,
        "permission_id" : 2})
    assert remove_admin.json() == {}
     
def test_message_send(url):
    """
    Testing message_send 
    """
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : userOne["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    prior_send = time()
    sendMessage = requests.post(f"{url}/message/send", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    assert sendMessage.json() == {"message_id" : 1}
    
def test_message_remove(url):
    """
    testing message_remove
    """
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : userOne["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/message/send", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    r = requests.delete(f"{url}/message/remove", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "message_id" : 1
    })
    chanMessages = requests.get(f"{url}/channel/messages", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "start" : 0
    })
    assert chanMessages.json() == {
        'messages' : [],
        'start' : 0,
        'end' : -1
    }

def test_message_edit(url):
    """
    testing message_edit
    """
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : userOne["token"],
        "name" : "channel_one",
        "is_public" : True
    })
    requests.post(f"{url}/message/send", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "message" : "Hello"
    })
    r = requests.put(f"{url}/message/edit", json={
        "token" : userOne["token"],
        "message_id" : 1,
        "message" : "Hi world"
    })
    chanMessages = requests.get(f"{url}/channel/messages", json={
        "token" : userOne["token"],
        "channel_id" : 1,
        "start" : 0
    })
    chanMessages = chanMessages.json()
    assert chanMessages['messages'][0]['message'] == "Hi world" 
    
def test_search_single_message(url):
     
    userOne = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    userOne = userOne.json()
    requests.post(f"{url}/channels/create", json={
        "token" : "first@person.com",
        "name" : "channel_one",
        "is_public" : True
    })
    sendMessage = requests.post(f"{url}/message/send", json={
        "token" : "first@person.com",
        "channel_id" : 1,
        "message" : "Hello World"
    })
    assert sendMessage.json() == {"message_id" : 1}

    # get variables for input into search
    token = "first@person.com"
    query_str = "Hello"

    searchResult = requests.get(f"{url}/search?token={token}&query_str={query_str}")
    searchResult = searchResult.json()
    assert len(searchResult) == 1
    assert searchResult[0]['message_id'] == 1
    assert searchResult[0]['u_id'] == 1
    assert searchResult[0]['message'] == "Hello World"

def test_user_profile_setname(url):
     
    #Register First User
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    assert(r.json() == {"u_id" : 1, "token" : "first@person.com"})
    #First User Changes Name
    nameChange = requests.put(f"{url}/user/profile/setname", json={
        "token" : "first@person.com",
        "name_first" : "New First",
        "name_last": "New Last"
    })
    assert(nameChange.json() == {})
    '''
    userProfile = requests.get(f"{url}/user/profile", json={
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
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    assert(r.json() == {"u_id" : 1, "token" : "first@person.com"})
    #First User Changes Name
    nameChange = requests.put(f"{url}/user/profile/setemail", json={
        "token" : "first@person.com",
        "email": "newemail@person.com"
    })
    assert(nameChange.json() == {})
    '''
    userProfile = requests.get(f"{url}/user/profile", json={
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

def test_users_all(url):
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    assert(r.json() == {"u_id" : 1, "token" : "first@person.com"})    

    #set variable for looking input
    token = "first@person.com"

    r = requests.get(f"{url}/users/all?token={token}")
    rj = r.json()
    assert(rj == {
        "first@person.com" : {
            "u_id" : "1",
            "name_first" : "First",
            "name_last" : "Bloggs"
            #"handle" : rj['handle']
        }
    })

def test_users_all(url):
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    assert(r.json() == {"u_id" : 1, "token" : "first@person.com"})    

    #variable for looking input
    token = "first@person.com"

    r = requests.get(f"{url}/users/all/?token={token}")
    rj = r.json()
    assert(rj == {
        "first@person.com" : {
            "u_id" : "1",
            "name_first" : "First",
            "name_last" : "Bloggs"
            #"handle" : rj['u_id']
        }
    })


def test_clear(url):
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "First",
        "name_last" : "Bloggs"
    })
    assert(r.json() == {"u_id" : 1, "token" : "first@person.com"})

    clear = requests.delete(f"{url}/clear")
    assert(clear.json() == {})

    user_two = requests.post(f"{url}/auth/register", json={
        "email" : "second@person.com",
        "password" : "catdog",
        "name_first" : "Mary",
        "name_last" : "Brown"})
    
    token = "second@person.com"

    r = requests.get(f"{url}/users/all/?token={token}")

    rj = r.json
    assert(rj == {
        "second@person.com" : {
            "u_id" : "1",
            "name_first" : "Mary",
            "name_last" : "Brown"
            #"handle" : rj['u_id']
        }
    })