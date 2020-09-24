# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register 
import pytest
from error import InputError

# checking the successful registration of a user
# checking the successful login of a user
def test_login():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert type(result) is dict, "registration was successful"
    assert type(auth_login('validemail@gmail.com', '123abc!@#')) is dict, "login was successful!" # Expect to work since we registered

# checking the login of an unregistered user
def test_register():
    # result = auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    # if type(auth_login) != dict:
    #     pytest.raises(InputError) ("Login failed, register first")
    # with pytest.raises(InputError) as e:
    #     assert auth_login('didntusethis@gmail.com', '123abcd!@#') # Expect fail since never registered
    pass

def test_logout():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert auth_logout(result["token"]) == {'is_success': True}, "logout was successful!"