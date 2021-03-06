import pytest
from auth import auth_register, auth_logout
from user import user_profile_sethandle
from other import clear, users_all
from error import InputError, AccessError

def test_users_all_positive_test():
    '''Positive case to determine whether full detail is returned''' 
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_sethandle(userOne['token'], '12345')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    user_profile_sethandle(userTwo['token'], '123456')
    details = users_all(userOne['token'])
    assert(details == { 'users' : [
    {
        'u_id' : userOne['u_id'],
        'name_first' : 'First',
        'name_last' : 'User',
        'handle_str' : '12345',
        'email' : 'firstuser@gmail.com',
        'profile_img_url': ''
    },
    {
        'u_id' : userTwo['u_id'],
        'name_first' : 'Second',
        'name_last' : 'User',
        'handle_str' : '123456',
        'email' : 'seconduser@gmail.com',
        'profile_img_url': ''
    }
    ]})

def test_users_all_invalid_token():
    ''' Test if Error Returned as Expected if the Token is Invalid '''
    clear()
    auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    with pytest.raises(AccessError):
        users_all("invalidtoken")
    clear()
