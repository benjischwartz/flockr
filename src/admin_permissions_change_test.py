import pytest
from error import AccessError, InputError
from admin_permissions_change import change_permissions
from auth import auth_register, auth_logout
from other import clear

# test change from owner of flocker to non-owner

# test change from non-owner of flocker to owner

# test access error
def test_access_error_token_not_owner():
    clear()
    auth_register("first@user.com", "thisisapassword", "Owner", "Flocker")
    not_owner = auth_register("second@user.com", "thisisapassword", "Not a owner", "Flocker")
    with pytest.raises(AccessError):
        # even though u_id 1 is owner, should still raise access error 
        # as user calling func is themselves not an owner
        change_permissions(not_owner['token'], 1, 1)

# test input error, u_id indicated does not refer to valid user

# test input error, permission_id does not refer to a value permission

# test permissions id

# test u_id