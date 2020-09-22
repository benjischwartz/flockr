# test suite for auth_* capabilities/functions
import auth
import pytest
from error import InputError

def test_login():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    assert auth.auth_login('validemail@gmail.com', '123abc!@#') # Expect to work since we registered

# def test_register():
#     result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
#     with pytest.raises(InputError) as e:
#         assert auth.auth_login('didntusethis@gmail.com', '123abcd!@#') # Expect fail since never registered
