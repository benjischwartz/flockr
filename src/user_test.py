import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register
from error import InputError
from other import clear

#TODO: ETHAN 
#User Setname Tests
def test_user_setname_positive_case():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_setname(token[userOne], 'New First', 'New Last')
    assert(users['firstuser@gmail.com']['name_first'] == 'New First')
    assert(users['firstuser@gmail.com']['name_last'] == 'New Last')

def test_user_setname_name_first_short():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setname(token[userOne], '', 'New Last')
    
def test_user_setname_name_first_long():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    longName = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(InputError):
        user_profile_setname(token[userOne], longName, 'New Last')

def test_user_setname_name_last_short():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setname(token[userOne], 'New First', '')

def test_user_setname_name_last_long():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    longName = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(InputError):
        user_profile_setname(token[userOne], 'New First', longName)

def test_user_setname_name_invalid_token():
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        user_profile_setname('INVALID_TOKEN', 'New First', 'New Last')

# User Setemail Tests
def test_user_setemail_positive_case():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_setemail(token[userOne], 'newemail@gmail.com')
    assert(users['newemail@gmail.com']['name_first'] == 'First')
    assert(users['newemail@gmail.com']['name_last'] == 'User')

def test_user_setemail_already_used():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    #Second User
    auth_register('randomemail@gmail.com', '123abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(token[userOne], 'randomemail@gmail.com')

def test_user_setemail_invalid_email_no_at_symbol():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(token[userOne], 'newemailgmail.com')

def test_user_setemail_not_alphanumeric():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(token[userOne], 'newemail  @gmail.com')

def test_user_setemail_invalid_token():
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        user_profile_setemail('INVALID_TOKEN', 'newemail@gmail.com')

#TODO: BRIAN
# User Profile Tests
def test_user_profile_positive_case():
    pass

def test_user_profile_uid_not_valid():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    pass

# User Sethandle Tests
def test_user_sethandle_positive_case():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')

    pass

def test_user_sethandle_length_short():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(InputError):
        user_profile_sethandle(userOne['token'], "12")

def test_user_sethandle_lenth_long():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(InputError):
        user_profile_sethandle(userOne['token'], "123456789123456789123456789")

def test_user_sethandle_handle_already_used():
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_sethandle(userOne['token'], "12345")
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')

    with pytest.raises(InputError):
        user_profile_sethandle(userTwo['token'], "12345")