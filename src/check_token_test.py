import pytest
from check_token import user_id_given_token, get_handle, email_given_user_id, permission_id_given_token
from check_token import jwt_given_email, email_given_jwt
from auth import auth_register, auth_logout
from other import clear

def test_user_id_given_token_positive_case():
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert(user_id_given_token(register_first_result['token']) == 1) 

def test_user_id_given_token_false_token():
    clear()
    # registering first user as the first user is the owner of the flockr
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert(user_id_given_token(register_first_result['token']) == 1) 

def test_user_id_given_token_after_logout():
    clear()
    # registering first user as the first user is the owner of the flockr
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user
    register_second_result = auth_register('secondemail@gmail.com', 'password1234', 'Second', 'User')
    auth_logout(register_second_result['token'])
    assert(user_id_given_token(register_second_result['token']) == None)

def test_get_handle():
    clear()
    # registering first user 
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    register_first_result_uid = user_id_given_token(register_first_result['token'])
    assert(get_handle(register_first_result_uid) == "janecitizen")

def test_get_handle_negative_case():
    clear()
    assert(get_handle(10) == None)

def test_email_given_user_id():
    clear()
    # registering first user 
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    register_first_result_uid = user_id_given_token(register_first_result['token'])
    assert(email_given_user_id(register_first_result_uid) == "randemail@gmail.com")

def test_email_given_user_id_false_case():
    clear()
    assert(email_given_user_id(5) == None)

def test_permission_id_given_token_flockr():
    clear()
    # registering first user 
    register_first_result = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert(permission_id_given_token(register_first_result['token']) == 1)

def test_permission_id_given_token_normal_user():
    clear()
    # registering first user 
    auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    # registering second user 
    register_second_result = auth_register('secondemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert(permission_id_given_token(register_second_result['token']) == 2)

def test_jwt_given_email():
    clear()
    assert type(jwt_given_email("firstemail@gmail.com")) is str

def test_email_given_jwt():
    clear()
    # registering first user 
    first_user = auth_register('randemail@gmail.com', 'password1234', 'Jane', 'Citizen')
    assert(email_given_jwt(first_user['token']) == "randemail@gmail.com")

