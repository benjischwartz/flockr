import channels
import channel
import admin_permissions_change
import message
import search
import user
import other
from message import message_send
from data import users, channel
from check_token import user_id_given_token, email_given_jwt
from error import AccessError, InputError
from datetime import timedelta, datetime
from time import time
from threading import Timer

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for
    the next "length" seconds if someone calls "standup_send" with a message.
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
    channel[channel_id]['standtime'] = int(now.timestamp())
    final_time = channel[channel_id]['standtime']

    timer = Timer(int(length), message_to_be_sent, [token, channel_id])
    timer.start()

    return {
        'finish_time': final_time
    }

def message_to_be_sent(token, channel_id):
    '''
    this is a helper function, which is ran after interval seconds have passed.
    '''
    message_send(token, channel_id, channel[channel_id]['standlist'])

    channel[channel_id]['standup'] = False
    channel[channel_id]['standtime'] = None
    channel[channel_id]['standlist'] = ''

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
    if channel[channel_id]['standup'] == False:
        return {
            'is_active' : False,
            'time_finish' : None
        }
    else:
        return {
            'is_active' : True,
            'time_finish': channel[channel_id]['time_finish']
        }

def standup_send(token, channel_id, message):
    '''
    Sending a message to get buffered in the 
    standup queue, assuming a standup is currently active
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

    full_name = users[token]['name_first'] + users[token]['name_last']
    final_message = full_name + ': ' + str(message)

    if channel[channel_id]['standuplist'] is None:
        channel[channel_id]['standuplist'] = final_message
    else:
        channel[channel_id]['standuplist'] += '/n' + final_message

    return {
    }