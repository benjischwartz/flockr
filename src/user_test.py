import pytest
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from auth import auth_register, auth_logout, auth_login
from error import InputError, AccessError
from other import clear
from channels import channels_create
from channel import channel_details

#User Setname Tests
def test_user_setname_positive_case():
    ''' Positive Case To Determine Whether the Name Changes '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_setname(userOne['token'], 'New First', 'New Last')
    #Create a Channel and Find Its Details to See if the Name has Changed
    #randomChannel_id = channels_create(userOne['token'], 'Random Channel', True)
    details = user_profile(userOne['token'], userOne['u_id'])
    assert(details['name_first'] == 'New First')
    assert(details['name_last'] == 'New Last')
    pass

def test_user_setname_name_first_short():
    ''' Test if Error Returned as Expected if First Name is Too Short '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setname(userOne['token'], '', 'New Last')
    
def test_user_setname_name_first_long():
    ''' Test if Error Returned as Expected if First Name is Too Long '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    longName = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(InputError):
        user_profile_setname(userOne['token'], longName, 'New Last')

def test_user_setname_name_last_short():
    ''' Test if Error Returned as Expected if Last Name is Too Short '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setname(userOne['token'], 'New First', '')

def test_user_setname_name_last_long():
    ''' Test if Error Returned as Expected if Last Name is Too Long '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    longName = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(InputError):
        user_profile_setname(userOne['token'], 'New First', longName)

def test_user_setname_name_invalid_token():
    ''' Test if Error Returned as Expected if the Token is Invalid '''
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        user_profile_setname('INVALID_TOKEN', 'New First', 'New Last')

def test_user_setname_name_invalid_token_after_logout():
    ''' Test if Error Returned as Expected if the Token is Invalid after Logout'''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        user_profile_setname(userOne['token'], 'New First', 'New Last')

# User Setemail Tests
def test_user_setemail_positive_case():
    ''' Test a Positive Case to Find if The Email Changes ''' 
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_setemail(userOne['token'], 'newemail@gmail.com')
    #Logging Out & Logging Back In With New Email
    auth_logout(userOne['token'])
    auth_login('newemail@gmail.com', '123abc!@#')

def test_user_setemail_already_used():
    ''' Test if Error is Returned if Email is Already Used '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    #Second User
    auth_register('randomemail@gmail.com', '123abc!@#', 'Second', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(userOne['token'], 'randomemail@gmail.com')

def test_user_setemail_invalid_email_no_at_symbol():
    ''' Test if Error is Returned if Email is Invalid  with No @ Symbol'''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(userOne['token'], 'newemailgmail.com')

def test_user_setemail_not_alphanumeric():
    ''' Test if Error is Returned if Email is Invalid as it is not Alphanumeric'''
    clear()
    #Creating First User
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(InputError):
        user_profile_setemail(userOne['token'], 'newemail  @gmail.com')

def test_user_setemail_invalid_token():
    ''' Test if Error is Returned if Token is Invalid '''
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        user_profile_setemail('INVALID_TOKEN', 'newemail@gmail.com')

def test_user_setemail_invalid_token_after_logout():
    ''' Test if Error Returned as Expected if the Token is Invalid after Logout'''
    clear()
    #Creating First User
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        user_profile_setemail(userOne['token'], 'newemail@gmail.com')

#TODO: BRIAN
# User Profile Tests
def test_user_profile_positive_case():
    ''' Positive case to determine whether the pratial detail of the user has returned'''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    user_profile_sethandle(userTwo['token'], '12345')
    userprofile = user_profile(userOne['token'], userTwo['u_id'])
    assert(userprofile == {
        'u_id' : userTwo['u_id'],
        'name_first' : 'Second',
        'name_last' : 'User',
        'handle' : '12345',
        'email' : 'seconduser@gmail.com',
    })

def test_user_profile_uid_not_valid():
    ''' Test if error raise when the input u_id is invalid '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')

    with pytest.raises(InputError):
        user_profile(userOne['token'], '0')
    
def test_user_profile_invalid_token():
    ''' Test if Error is raised as expected if token is invalid '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(AccessError):
        user_profile('INVALID_TOKEN', userOne['u_id'])

def test_user_profile_invalid_token_after_logout():
    ''' Test if Error Returned as Expected if the Token is Invalid after Logout'''
    clear()
    #Creating First User
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    auth_logout(userOne['token'])
    with pytest.raises(AccessError):
        user_profile(userOne['token'], userOne['u_id'])

# User Sethandle Tests
def test_user_sethandle_positive_case():
    ''' Positive case to determine whether the handle changes '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_sethandle(userOne['token'], '12345')

    details = user_profile(userOne['token'], userOne['u_id'])
    assert(details['handle'] == '12345')

def test_user_sethandle_length_short():
    ''' Test if error returned as expected if handle length is too short '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(InputError):
        user_profile_sethandle(userOne['token'], "12")

def test_user_sethandle_lenth_long():
    ''' Test if error returned as expected if handle length is too long '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(InputError):
        user_profile_sethandle(userOne['token'], "123456789123456789123456789")


def test_user_sethandle_handle_already_used():
    ''' Test if error is raised if handle already in use '''
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_sethandle(userOne['token'], "12345")
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')

    with pytest.raises(InputError):
        user_profile_sethandle(userTwo['token'], "12345")
    
def test_user_sethandle_invalid_token():
    ''' Test if Error is Returned if Token is Invalid '''
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    
    with pytest.raises(AccessError):
        user_profile_sethandle('INVALID_TOKEN', '12345')
