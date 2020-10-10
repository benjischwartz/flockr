# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register 
import pytest
from error import InputError
from other import clear

# checking the successful registration of a user
# checking the successful login of a user
def register_return_values():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    # Would be better to assert that the user has indeed been registered
    details = user_profile(result['token'], result['u_id'])
    assert details['email'] == 'validemail@gmail.com'
    assert details['name_first'] == 'hello'
    assert details['name_last'] == 'goodbye'
    # No need to clear at the end if you are clearing at the start of each test
    clear()

def test_register_multiple():
    clear()
    result1 = auth_register('validemail@gmail.com', '123abc!@#', 'first', 'person')
    result2 = auth_register('validemail2@gmail.com', '123abc!@#', 'second', 'person')
    assert result1['u_id'] != result2['u_id']
    # Tests shouldn't have knowledge of the tokens themselves, instead test the tokens are unique
    assert result1['token'] != result2['token']

def test_register_multiple_fail_login():
    clear()
    result1 = auth_register('validemailperson@gmail.com', '123abc!@#', 'first', 'person')
    result2 = auth_register('validemailperson2@gmail.com', '345def#$%', 'second', 'person')

    # checking an error is raised when trying to log-in (since already logged-in)
    with pytest.raises(InputError) as e:
        auth_login('validemailperson3@gmail.com', '123abc!@#')
        auth_login('validemailperson4@gmail.com', '345def#$%')
        auth_login('validemailperson5@gmail.com', '456ghi$%^') # expect fail since did not register first
    clear()

# Checking the invalid login of someone already logged in
def test_already_logged_in():
    clear()
    reg_result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    # Not clear what is 'invalid' about the login here
    assert type(reg_result) == dict
    assert type(auth_login('validemail@gmail.com', '123abc!@#')) is dict
    clear()

def test_register_logout_login():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    assert(auth_logout('validemail@gmail.com')) == {'is_success': True}
    login_result = auth_login('validemail@gmail.com', '123abc!@#')
    assert type(login_result) is dict


# Checking the registration of users with invalid firstname, lastname, and password
def test_invalid_email_register():
    clear()
    with pytest.raises(InputError) as e:
        auth_register('invalidemail.com', '123abc!@#', 'Firstname', 'Lastname')

def test_invalid_first_name():
    clear()
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', '123abc!@#', '', 'Nofirstname')

def test_invalid_last_name():
    clear()
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', '123abc!@#', 'Nolastname', '')

def test_invalid_password():
    clear()
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', 'five!', 'Bob', 'Thebuilder')


# checking the login of an unregistered user
def test_register():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    with pytest.raises(InputError) as e:
        auth_login('didntusethisemail@gmail.com', '123abc!@#') # Expect fail since never registered
 
# checking the registration of a user that is already registered
def test_already_registered():
    clear()
    auth_register('validemail1@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    with pytest.raises(InputError) as e:
        auth_register('validemail1@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    clear()

def test_logout():
    clear()
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert auth_logout(result["token"]) == {'is_success': True}, "logout was unsuccessful"
    # Also test side effect - has the token been invalidated?
    clear()

# Not clear what this test is actually testing
def test_logout_invalidate_token():
    clear()
    result1 = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    result2 = auth_logout('validemaillogout@gmail.com') 
    assert result2 == {'is_success': True} #expect to return true since token is valid
    result3 = auth_login('validemaillogout@gmail.com', '123abc!@#')
    assert type(result3) is dict
    clear()

def test_invalid_logout():
    clear()
     #expect to return false since token is not valid
    assert auth_logout('invalidemaillogout@gmail.com') == {'is_success': False}
    clear()

def test_logout_twice():
    clear()
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert (auth_logout('validemaillogout@gmail.com')) == {'is_success': True}
    # expect false since already logged out
    assert (auth_logout('validemaillogout@gmail.com')) == {'is_success': False}