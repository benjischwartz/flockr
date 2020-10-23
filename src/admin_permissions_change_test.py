import pytest
from error import AccessError, InputError
from admin_permissions_change import admin_userpermission_change
from auth import auth_register, auth_logout
from other import clear
from check_token import permission_id_given_token

# test change from non-owner of flocker to owner
def test_change_to_owner():
    clear()
    user_one = auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    user_two = auth_register("second@user.com", "thisisapassword", "Not a owner", "Flocker")
    # change user two into owner
    admin_userpermission_change(user_one['token'], user_two['u_id'], 1)
    assert permission_id_given_token(user_two['token']) == 1, "permission_id is not owner value"

# test change from owner of flocker to non-owner

def test_change_owner_to_member():
    clear()
    user_one = auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    user_two = auth_register("second@user.com", "thisisapassword", "Not a owner", "Flocker")
    # user one makes user two an owner
    admin_userpermission_change(user_one['token'], user_two['u_id'], 1)
    assert permission_id_given_token(user_two['token']) == 1, "permission_id is not owner value"
    # user two removes user one as an owner
    admin_userpermission_change(user_two['token'], user_one['u_id'], 2)
    assert permission_id_given_token(user_one['token'])== 2, "permission_id is not member value"

# test access error - not owner
def test_access_error_token_not_owner():
    clear()
    auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    not_owner = auth_register("second@user.com", "thisisapassword", "Not a owner", "Flocker")
    with pytest.raises(AccessError):
        # even though u_id 1 is owner, should still raise access error 
        # as user calling func is themselves not an owner
        admin_userpermission_change(not_owner['token'], 1, 1)

# test access error - invalid token, i.e. not a member or owner
def test_invalid_token_access_error():
    clear()
    with pytest.raises(AccessError):
        admin_userpermission_change("invalidtoken", 1, 1)

# test input error, u_id indicated does not refer to valid user
def test_input_error_invalid_u_id():
    clear()
    owner = auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    with pytest.raises(InputError):
        # testing u_id of 0 which is invalid
        admin_userpermission_change(owner['token'], 0, 1) 


# test input error, permission_id does not refer to a valid value
def test_input_error_invalid_permission_id():
    clear()
    owner = auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    not_owner = auth_register("second@user.com", "thisisapassword", "Not a owner", "Flocker")
    with pytest.raises(InputError):
        admin_userpermission_change(owner['token'],not_owner['u_id'], 23)
