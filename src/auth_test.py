# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register 
import pytest
from error import InputError
from other import clear
from data import tokens

# checking the successful registration of a user
# checking the successful login of a user
def test_login_return_type():
    clear()
    result = auth_register('validemail1@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert result['u_id'] == 1, "registration unsuccessful"
    log_result = auth_login('validemail1@gmail.com', '123abc!@#')
    assert log_result['u_id'] == 1, "login unsuccessful" # Expect to work since we registered
    assert log_result['token'] == 'validemail1@gmail.com'
    clear()

def test_register_return_values():
    clear()
    result = auth_register('validemail2@gmail.com', '123abc!@#', 'second', 'person')
    assert result['u_id'] == 1
    assert result['token'] == 'validemail2@gmail.com'
    clear()

def test_register_and_login_multiple_users():
    clear()
    result1 = auth_register('validemailperson3@gmail.com', '123abc!@#', 'third', 'person')
    result2 = auth_register('validemailperson4@gmail.com', '345def#$%', 'fourth', 'person')
    # checking the return values of returned registration dictionary
    assert result1['u_id'] == 1
    assert result2['u_id'] == 2
    assert result1['token'] == 'validemailperson3@gmail.com'
    assert result2['token'] == 'validemailperson4@gmail.com'

     # checking the return values of returned login dictionary
    log_result_1 = auth_login('validemailperson3@gmail.com', '123abc!@#')
    log_result_2 = auth_login('validemailperson4@gmail.com', '345def#$%')
    assert log_result_1['u_id'] == 1
    assert log_result_2['u_id'] == 2
    with pytest.raises(InputError) as e:
        auth_login('validemailperson5@gmail.com', '456ghi$%^') # expect fail since did not register first
    clear()


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
    clear()

def test_logout_invalidate_token():
    clear()
    result1 = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert tokens[0] == 'validemaillogout@gmail.com'
    result2 = auth_logout('validemaillogout@gmail.com') 
    assert result2 == {'is_success': True} #expect to return true since token is valid
    assert len(tokens) == 0
    clear()

def test_invalid_logout():
    clear()
     #expect to return false since token is not valid
    assert auth_logout('invalidemaillogout@gmail.com') == {'is_success': False}
    clear()