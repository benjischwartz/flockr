from data import users, codes, data_store, data_retreive
import jwt

def code_given_email(email):
    """
    returns a valid reset code for a supplied email
    """
    return jwt.encode({'email': email}, 'reset').decode('utf-8')

def email_given_code(code):
    """
    returns the email of a valid code
    otherwise returns None
    """
    try:
        decoded_jwt = jwt.decode(code, 'reset', algorithms='HS256')
        return decoded_jwt['email']
    except Exception:
        return None