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


