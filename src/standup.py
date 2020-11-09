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
from datetime import time, timedelta, datetime
import time
from threading import Timer

def standup_start(token, channel_id, length):

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
    current_time = datetime.now()
    buffer = current_time + timedelta(seconds=int(length))
    channel[channel_id]['standtime'] = int(buffer.timestamp())
    time = channel[channel_id]['standtime']

    timer = Timer(int(length), message_send(token, channel_id, str(channel[channel_id]['standuplist'])))
    timer.start()

    channel[channel_id]['standup'] = False
    channel[channel_id]['standtime'] = None
    channel[channel_id]['standlist'] = ''

    return {
        'finish_time': time
    }


def standup_active(token, channel_id):

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
        'time_finish': channel[channel_id]['finish_time'] 
    }

def standup_send(token, channel_id, message):

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