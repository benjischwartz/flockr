from data import users, channel
from error import InputError, AccessError
from check_token import user_id_given_token, email_given_jwt
import re
import requests
#from werkzeug import secure_filename
import os
#import cv2
import urllib
import uuid
from PIL import Image

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

    user = None
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    for tokens, data in users.items():
        if data['u_id'] == u_id:
            user = {
                'u_id': data['u_id'],
                'email': tokens,
                'name_first': data['name_first'],
                'name_last': data['name_last'],
                'handle_str': data['handle'],
                'profile_img_url': data['profile_img_url']
            }

    if user is None:
        raise InputError(description="Invalid ID.")

    return {
        'user': user
    }

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

def user_profile_uploadphoto(token, img_url, server_url, x_start, y_start, x_end, y_end):
    '''
    The function allows a user to upload a photo given a URL on the Internet and then crops
    the image to the specified dimensions. It then stores the image with a unique ID in the
    imgurl folder.

    Parameters:
        token (str): refers to a valid user on flockr who is calling this function
        img_url (str): URL on the Internet of the image to be uploaded
        server_url (str): URL of the server
        x_start (int): pixels from the left to start cropping
        y_start (int): pixels from the top to start cropping
        x_end (int): pixels from the left to end cropping
        y_end (int): pixels from the top to end cropping

    Returns:
        (dict): {

        }
    '''

    # Check if the token is valid
    token_u_id = user_id_given_token(token)
    if token_u_id is None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    # Check if the URL is valid
    try:
        r = requests.head(img_url)
        img_url_status_code = r.status_code
        #Check if URL is valid but does not return Success HTTP 200 Response
        if (img_url_status_code != 200):
            raise InputError(description="URL Invalid")
    except requests.ConnectionError:
        raise InputError(description="URL Invalid")
    
    # Check if the image is in the JPG file format
    file_extension = (os.path.splitext(img_url))[1]
    if (file_extension != '.jpg'): 
        raise InputError(description="Not a JPG image")
    
    # Save image in the "imgurl" folder
    randomised_filename = str(uuid.uuid4()) + ".jpg"
    save_url = "src/imgurl/" + randomised_filename
    urllib.request.urlretrieve(img_url, save_url)

    img = Image.open(save_url)

    # Check if the image is within the bounds
    if (x_start < 0 or y_start < 0):
        os.remove(save_url)
        raise InputError(description="Cropping bounds are not within the dimensions of the image")

    # Checking Width
    if (x_end > img.size[0]):
        os.remove(save_url)
        raise InputError(description="Cropping bounds are not within the dimensions of the image")
    
    # Checking Height
    if (y_end > img.size[1]):
        os.remove(save_url)
        raise InputError(description="Cropping bounds are not within the dimensions of the image")

    # Save URL in the user profile details
    email = email_given_jwt(token)
    users[email]['profile_img_url'] = server_url + "/imgurl/" + randomised_filename
    
    # Cropping Image to Given Dimensions
    cropped = img.crop((x_start,y_start, x_end, y_end))
    cropped.save(save_url)

    return {
    }
    


