import pytest
from auth import auth_register
from user import user_profile_sethandle
from users import users_all
from other import clear

def test_users_all_positive_test():
    clear()
    userOne = auth_register('firstuser@gmail.com', '123abc!@#', 'First', 'User')
    user_profile_sethandle(userOne['token'], '12345')
    userTwo = auth_register('seconduser@gmail.com', '456abc!@#', 'Second', 'User')
    user_profile_sethandle(userTwo['token'], '123456')
    details = users_all(userOne['token'])
    assert(details == [
    {
        'u_id' : userOne['u_id'],
        'name_first' : 'First',
        'name_last' : 'User',
        'handle' : '12345',
        'email' : 'firstuser@gmail.com'
    },
    {
        'u_id' : userTwo['u_id'],
        'name_first' : 'Second',
        'name_last' : 'User',
        'handle' : '123456',
        'email' : 'seconduser@gmail.com'
    }
    ])