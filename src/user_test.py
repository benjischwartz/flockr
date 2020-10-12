import user
import pytest

#TODO: ETHAN 
#User Setname Tests
def test_user_setname_positive_case():
    pass

def test_user_setname_name_first_short():
    pass

def test_user_setname_name_first_long():
    pass

def test_user_setname_name_last_short():
    pass

def test_user_setname_name_last_long():
    pass

# User Setemail Tests
def test_user_setemail_positive_case():
    pass

def test_user_setemail_already_used():
    pass

def test_user_setemail_invalid_email_no_at_symbol():
    pass

def test_user_setemail_not_alphanumeric():
    pass

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