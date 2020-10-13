from data import users
from error import AccessError, InputError
from check_token import user_id_given_token

# required function changing permission
def change_permissions(token,u_id,permission_id):
    """
    Given a User by their user ID, set their permissions
     to new permissions described by permission_id
    """
    # token itself is invalid, i.e. not a member or owner
    if user_id_given_token(token) == None:
        raise AccessError
    # token does not belong to an existing owner
    if users[token]['permission_id'] != 1:
        raise AccessError

    # invalid u_id
    userFound = False
    for email in users:
        if users[email]['u_id'] == u_id:
            userFound = True 
    if userFound is False:
        raise InputError
    
    # invalid permission_id
    if permission_id != 1 and permission_id != 2:
        raise InputError

    return {}
