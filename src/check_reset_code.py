from data import users, codes

def code_given_email(email):
    for emails in codes.keys():
        if email == emails:
            return codes[email]
    # no code found for the given email
    return None

def email_given_code(code):
    for emails in codes.keys():
        if codes[emails] == code:
            return emails
    # no email found for the given code
    return None

def password_given_email(email):
    for emails in users.keys():
        if email == emails:
            return users[email]['password']
    return None