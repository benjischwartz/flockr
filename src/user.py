from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token, email_given_jwt
import re

regex = '^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
def check(email):
    '''
    Helper function to determine whether an email is valid.
    '''
    if(re.search(regex,email)):
        return("Valid Email")
    else:
        return("Invalid Email")

def user_profile(token, u_id):
    '''
    Returns a list of all users and their associated details.

    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        u_id (int): u_id that identifies the specified user to find the profile of
    
    Returns:
        (dict): {

        }
    '''

    validid = 0
    selected_data = {}
    selected_email = ' '
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    for tokens, data in users.items():
        if data['u_id'] == u_id:
            validid = 1
            selected_data = data
            selected_email = tokens

    if validid == 0:
        raise InputError(description="Invalid ID.")
    else:
        selected_data.pop('password')
        selected_data.pop('permission_id')
        selected_data['email'] = selected_email

    return selected_data

def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name.  

    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        name_first (str): the new first name that should be set on the user profile
        name_last (str): the new last name that should be set on the user profile
    
    Returns:
        (dict): {

        }
    '''

    #Error Checking: Raise an Input Error if Names not Between 1 & 50 Characters
    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError(description="First Name is not Between 1 and 50 Characters")
    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError(description="Last Name is not Between 1 and 50 Characters")

    #Error Checking: Raise an AccessError if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    email = email_given_jwt(token)
    users[email]['name_first'] = name_first
    users[email]['name_last'] = name_last

    return {
    }

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address.  

    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        email (str): the new email that should be set on the user profile
    
    Returns:
        (dict): {

        }
    '''
    #Error Checking: Raise an InputError if the email is invalid
    if (check(email) != "Valid Email"):
        raise InputError (description="Invalid email")

    #Error Checking: Raise an AccessError if the token is invalid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    #Error Checking: Raise an InputError if email is already used
    if email in users:
        raise InputError(description="Email has already been used.")
    
    old_email = email_given_jwt(token)
    users[email] = users.pop(old_email)

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Update the authorised user's handle.  

    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        handle (str): the new handle that should be set on the user profile
    
    Returns:
        (dict): {

        }
    '''
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    if ((len(handle_str) < 3) or (len(handle_str) > 20)):
        raise InputError(description="Handle has to be in between 3 and 20 letters inclusive.")
    
    #for tokens, data in users.items():

    for email in users:
        if users[email]['handle'] == handle_str:
            raise InputError(description="Handle is already being used by another user.")
    
    email = email_given_jwt(token)
    users[email]['handle'] = handle_str
    
    return {
    }
    
