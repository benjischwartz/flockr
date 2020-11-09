# test suite for auth_* capabilities/functions
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, auth_passwordreset_reset
import pytest
from error import InputError
from other import clear
from check_token import get_handle, jwt_given_email
from check_reset_code import code_given_email, email_given_code

# checking the successful registration of a user
# checking the successful login of a user
def test_register_return_values():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'hello', 'goodbye')
    result['token'] == jwt_given_email('validemail@gmail.com') #user is registered
    assert type(result['u_id']) is int, "registration unsuccessful"

def test_register_multiple():
    clear()
    result1 = auth_register('validemail@gmail.com', '123abc!@#', 'first', 'person')
    result2 = auth_register('validemail2@gmail.com', '123abc!@#', 'second', 'person')
    assert result1['u_id'] != result2['u_id']          
    assert result1['token'] != result2['token']

def test_register_multiple_fail_login():
    clear()
    result1 = auth_register('validemailperson@gmail.com', '123abc!@#', 'first', 'person')
    result2 = auth_register('validemailperson2@gmail.com', '345def#$%', 'second', 'person')
    assert type(result1) is dict
    assert type(result2) is dict

    # checking an error is raised when trying to log-in (since already logged-in)
    with pytest.raises(InputError):
        auth_login('validemailperson3@gmail.com', '123abc!@#')
        auth_login('validemailperson4@gmail.com', '345def#$%')
        auth_login('validemailperson5@gmail.com', '456ghi$%^') # expect fail since did not register first

# Checking the invalid login of someone already logged in
def test_already_logged_in():
    clear()
    reg_result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    assert type(reg_result) == dict
    assert type(auth_login('validemail@gmail.com', '123abc!@#')) is dict

def test_register_logout_login():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    assert type(result) is dict
    assert(auth_logout(result['token']) == {'is_success': True})
    login_result = auth_login('validemail@gmail.com', '123abc!@#')
    assert type(login_result) is dict


# Checking the registration of users with invalid firstname, lastname, and password
def test_invalid_email_register():
    clear()
    with pytest.raises(InputError):
        auth_register('invalidemail.com', '123abc!@#', 'Firstname', 'Lastname')

def test_invalid_first_name():
    clear()
    with pytest.raises(InputError):
        auth_register('thisemailisfine@gmail.com', '123abc!@#', '', 'Nofirstname')

def test_invalid_last_name():
    clear()
    with pytest.raises(InputError):
        auth_register('thisemailisfine@gmail.com', '123abc!@#', 'Nolastname', '')

def test_invalid_password():
    clear()
    with pytest.raises(InputError):
        auth_register('thisemailisfine@gmail.com', 'five!', 'Bob', 'Thebuilder')


# checking the login of an unregistered user
def test_register():
    clear()
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    assert type(result) is dict
    with pytest.raises(InputError):
        auth_login('didntusethisemail@gmail.com', '123abc!@#') # Expect fail since never registered
 
# checking the registration of a user that is already registered
def test_already_registered():
    clear()
    auth_register('validemail1@gmail.com', '123abc!@#', 'Firstname', 'Lastname')
    with pytest.raises(InputError):
        auth_register('validemail1@gmail.com', '123abc!@#', 'Firstname', 'Lastname')

def test_logout():
    clear()
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert auth_logout(result["token"]) == {'is_success': True}, "logout was unsuccessful"

def test_logout_invalidate_token():
    clear()
    result1 = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert type(result1) is dict
    result2 = auth_logout(result1['token']) 
    assert result2 == {'is_success': True} #expect to return true since token is valid
    result3 = auth_login('validemaillogout@gmail.com', '123abc!@#')
    assert type(result3) is dict

def test_invalid_logout():
    clear()
     #expect to return false since token is not valid
    assert auth_logout('invalidemaillogout@gmail.com') == {'is_success': False}

def test_logout_twice():
    clear()
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    assert type(result) is dict
    assert (auth_logout(result['token'])) == {'is_success': True}
    # expect false since already logged out
    assert (auth_logout(result['token'])) == {'is_success': False}

def test_logout_invalid_login():
    clear()
    result = auth_register('validemaillogout@gmail.com', '123abc!@#', 'hello', 'goodbye')
    auth_logout(auth_logout(result['token']))
    with pytest.raises(InputError):
        auth_login('validemaillogout@gmail.com', 'nottherightpassword')

def test_get_handle():
    clear()
    result = auth_register('bobby@gmail.com', '123abc!@#', 'Bobby', 'Brown')
    assert get_handle(result['u_id']) == 'bobbybrown'

def test_get_handle_unique():
    clear()
    result1 = auth_register('bobby1@gmail.com', '123abc!@#', 'Bobby', 'Brown')
    result2 = auth_register('bobby2@gmail.com', '123abc!@#', 'Bobby', 'Brown')
    result3 = auth_register('bobby3@gmail.com', '123abc!@#', 'Bobby', 'Brown')

    # test that all three handles are unique
    assert get_handle(result1['u_id']) == 'bobbybrown'
    assert get_handle(result2['u_id']) == 'bobbybrown0'
    assert get_handle(result3['u_id']) == 'bobbybrown1'
    
def test_get_handle_long_name():
    clear()
    result = auth_register('reallylongname@gmail.com', '123abc!@#', 'Longfirstname', 'Longlastname')
    assert get_handle(result['u_id']) == 'longfirstnamelonglas'

def test_passwordreset_request():
    clear()
    auth_register('flockrrecipient@gmail.com', '123abc!@#', 'Example', 'Recipient')
    request_result = auth_passwordreset_request('flockrrecipient@gmail.com')
    assert request_result == {}
    assert code_given_email('flockrrecipient@gmail.com') is not None     # there exists a valid reset code in the code dictionary

def test_passwordreset_reset():
    # continuation from previous test
    reset_result = auth_passwordreset_reset(code_given_email('flockrrecipient@gmail.com'), 'newpassword123')
    assert reset_result == {}
    assert auth_login('flockrrecipient@gmail.com', 'newpassword123')    # successfully login with new password

    auth_logout(jwt_given_email('flockrrecipient@gmail.com'))           # user logs out
    with pytest.raises(InputError):
        auth_login('flockrreceipient@gmail.com', '123abc!@#')           # user fails to log in with old password
    
def test_passwordreset_reset_invalid_code():
    # continuation from previous tests
    with pytest.raises(InputError):
        auth_passwordreset_reset('invalidcode', 'newpassword456')           # expect fail since invalid code given
    
def test_passwordreset_invalid_newpassword():
    clear()
    auth_register('johndoe@gmail.com', '123abc!@#', 'John', 'Doe')
    auth_passwordreset_request('johndoe@gmail.com')
    with pytest.raises(InputError):
        auth_passwordreset_reset(code_given_email('johndoe@gmail.com'), 'short')   # expect fail since password too short

def test_twousers_reset():
    """
    Two users request a password reset. First user successfully enters code
    and their password is changed. Second user successfully enters a code with
    their previous password and reset fails. 
    """
    clear()
    auth_register('johndoe@gmail.com', '123abc!@#', 'John', 'Doe')      # users register
    auth_register('flockrrecipient@gmail.com', '123abc!@#', 'Example', 'Recipient') 

    auth_passwordreset_request('johndoe@gmail.com')                     # both users request password reset
    auth_passwordreset_request('flockrrecipient@gmail.com')    

    auth_passwordreset_reset(code_given_email('johndoe@gmail.com'), 'new_password')     # first user successfully resets with new password
    with pytest.raises(InputError):
        auth_passwordreset_reset(code_given_email('flockrrecipient@gmail.com'), '123abc!@#') # second user fails with old password
