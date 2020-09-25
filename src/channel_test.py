# test file for the channel functions

from auth import auth_register
from channel import channel_invite, channel_details, channel_messages
from channels import channels_create
import pytest
from error import InputError




'''
# check channel_invite
# This test is meant to check if an inputError is given if the channel_id is 
# invalid; INCOMPLETE
# Note: "result['token'] may not be valid python but my intention was to get
# the token and u_id values that were returned from auth_register 

def test_channel_invite_except:
    result = auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    randChannel_id = channels_create(result['token'], 'randChannel', True)
    invalidChannel_id = 18
    if invalidChannel_id == randChannel_id:
        invalidChannel_id = 19
    with pytest.raises(InputError) as e:
        assert channel_invite(result['token'], invalidChannel_id, result['u_id'])
    # InputError also if u_id is not valid 
    
    # Accesserror when token is invalid 
    
    # Accesserror when the authorised user is not already a member of the channel
'''
def test_channel_removeowner():
    register_result = auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
    
        
    
