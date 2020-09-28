# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register 
import pytest
from error import InputError

# checking the successful registration of a user
# checking the successful login of a user
def test_login_return_type():
    result = auth_register('validemail1@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert result['u_id'] == 1, "registration unsuccessful"
    log_result = auth_login('validemail1@gmail.com', '123abc!@#')
    assert log_result['u_id'] == 1, "login unsuccessful" # Expect to work since we registered
    assert log_result['token'] == 'validemail1@gmail.com'

def test_register_return_values():
    result = auth_register('validemail2@gmail.com', '123abc!@#', 'second', 'person')
    assert result['u_id'] == 2
    assert result['token'] == 'validemail2@gmail.com'

def test_register_and_login_multiple_users():
    result1 = auth_register('validemailperson3@gmail.com', '123abc!@#', 'third', 'person')
    result2 = auth_register('validemailperson4@gmail.com', '345def#$%', 'fourth', 'person')
    # checking the return values of returned registration dictionary
    assert result1['u_id'] == 3
    assert result2['u_id'] == 4
    assert result1['token'] == 'validemailperson3@gmail.com'
    assert result2['token'] == 'validemailperson4@gmail.com'

     # checking the return values of returned login dictionary
    log_result_1 = auth_login('validemailperson3@gmail.com', '123abc!@#')
    log_result_2 = auth_login('validemailperson4@gmail.com', '345def#$%')
    assert log_result_1['u_id'] == 3
    assert log_result_2['u_id'] == 4
    with pytest.raises(InputError) as e:
        auth_login('validemailperson5@gmail.com', '456ghi$%^') # expect fail since did not register first


# Checking the registration of users with invalid firstname, lastname, and password
def test_invalid_email_register():
    with pytest.raises(InputError) as e:
        auth_register('invalidemail.com', '123abc!@#', 'Firstname', 'Lastname')

def test_invalid_first_name():
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', '123abc!@#', '', 'Nofirstname')

def test_invalid_last_name():
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', '123abc!@#', 'Nolastname', '')

def test_invalid_password():
    with pytest.raises(InputError) as e:
        auth_register('thisemailisfine@gmail.com', 'five!', 'Bob', 'Thebuilder')


# checking the login of an unregistered user
def test_register():
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    with pytest.raises(InputError) as e:
        auth_login('didntusethisemail@gmail.com', '123abc!@#') # Expect fail since never registered
 
# checking the registration of a user that is already registered
def test_already_registered():
    with pytest.raises(InputError) as e:
        auth_register('validemail1@gmail.com', '123abc!@#', 'Firstname', 'Lastname')


def test_logout():
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert auth_logout(result["token"]) == {'is_success': True}, "logout was successful!"

# TODO: write tests for logout