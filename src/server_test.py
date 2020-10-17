import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
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
    clear()
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
    clear()
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

def test_channels_create_public(url):
    """
    Testing creating a public channel
    """
    clear()
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
    clear()
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
    clear()
    r = requests.post(f"{url}/auth/register", json={
        "email" : "first@person.com",
        "password" : "catdog",
        "name_first" : "Joe",
        "name_last" : "Bloggs"})
    
    assert r.json() == {"u_id" : 1, "token" : "first@person.com"} # TODO change token when handle has been changed.
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

def test_admin_permissions_change(url):
    """
    Testing changing admin privileges
    user one makes user two admin, then user two removes user one
    Works if test does not throw error
    """
    clear()
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
        "u_id" : 1,
        "permission_id" : 1})
    assert made_admin.json() == {}
    remove_admin = requests.post(f"{url}/admin/userpermission/change", json={
        "token": "second@person.com",
        "u_id" : 2,
        "permission_id" : 2})
    assert remove_admin.json() == {}
     