# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register 
import pytest
from error import InputError

# checking the successful registration of a user
# checking the successful login of a user
def test_login_return_type():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert type(result) is dict, "registration was successful"
    assert type(auth_login('validemail@gmail.com', '123abc!@#')) is dict, "login was successful!" # Expect to work since we registered


def test_login_return_values():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert result['u_id'] == 'validemail@gmail.com'
    assert result['token'] == 'validemail@gmail.com'

def test_invalid_email_register():
    with pytest.raises(InputError) as e:
        auth_register('invalidemail.com', '123abc!@#', 'Firstname', 'Lastname')

        
# checking the login of an unregistered user
def test_register():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    with pytest.raises(InputError) as e:
        auth_login('didntusethisemail@gmail.com', '123abc!@#') # Expect fail since never registered
 

def test_logout():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert auth_logout(result["token"]) == {'is_success': True}, "logout was successful!"