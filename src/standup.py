import channels
import channel
import admin_permissions_change
import message
import search
import user
import other
from message import message_send
from data import users, channel
from data_persistence import data_store
from check_token import user_id_given_token, email_given_jwt
from error import AccessError, InputError
from datetime import timedelta, datetime
from time import time
from threading import Timer

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for
    the next "length" seconds if someone calls "standup_send" with a message.
    returns time_finish for standup period
    '''
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")

    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError(description="Member not in selected channel.")    

    if channel[channel_id]['standup'] == True:
        raise InputError(description="standup already exists in the selected channel")

    channel[channel_id]['standup'] = True
    now = datetime.now() + timedelta(seconds=int(length))
    channel[channel_id]['standuptime'] = int(now.timestamp())
    final_time = channel[channel_id]['standuptime']

    timer = Timer(int(length), message_to_be_sent, [token, channel_id])
    timer.start()

    data_store()
    return {
        'time_finish': final_time
    }

def message_to_be_sent(token, channel_id):
    '''
    this is a helper function, which is run after interval seconds have passed.
    '''
    
    message_send(token, channel_id, channel[channel_id]['standuplist'])

    channel[channel_id]['standup'] = False
    channel[channel_id]['standuptime'] = None
    channel[channel_id]['standuplist'] = ''

    return

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it,
    and what time the standup finishes. If no standup is active,
    then time_finish returns None
    '''

    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")

    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError(description="Member not in selected channel.")

    return {
        'is_active' : channel[channel_id]['standup'],
        'time_finish': channel[channel_id]['time_finish']
    }

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the 
    standup queue, assuming a standup is currently active
    returns {}
    '''
    token_u_id = user_id_given_token(token)
    if token_u_id == None:
        raise AccessError(description="Token passed is not valid. If you recently reset your "
            "email you will need to logout and login again using your updated email.")

    if channel_id not in channel:
        raise InputError(description="Channel ID is invalid.")

    if token_u_id not in channel[channel_id]['all_members']:
        raise AccessError(description="Member not in selected channel.")

    if len(message) > 1000:
        raise InputError(description="Message exceeds limit(1000).")

    if channel[channel_id]['standup'] != True:
        raise InputError(description="standup is not active.")

    email = email_given_jwt(token)
    full_name = users[email]['name_first'] + users[email]['name_last']
    final_message = full_name + ': ' + str(message)
    
    if channel[channel_id]['standuplist'] == '':
        channel[channel_id]['standuplist'] = final_message
    else:
        channel[channel_id]['standuplist'] += '\n' + final_message

    data_store()
    return {
    }
