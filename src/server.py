import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from flask_mail import Mail, Message
import auth
import channels
import channel
import admin_permissions_change
import message
import search
import user
import other
import standup
import smtplib
import check_reset_code

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
APP.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'flockrmail@gmail.com',
	MAIL_PASSWORD = 'i2PXfayKUSKH7xW'
	)
mail = Mail(APP)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    payload = request.args.get('data')
    if payload == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': payload
    })

# No trailing `/`, this will cause issues with the frontend
@APP.route("/auth/register", methods=['POST'])
def auth_register():
    """
    creating a user in data.py's users dictionary
    return {u_id : ___ , token: _____ }
    """
    payload = request.get_json()
    return dumps(auth.auth_register(payload["email"], payload["password"], payload["name_first"], payload["name_last"]))

@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    """
    logging out a user given a valid token
    return {"is_success": True} if successful, otherwise {"is_success": False}
    """
    payload = request.get_json()
    return dumps(auth.auth_logout(payload["token"]))

@APP.route("/auth/login", methods=['POST'])
def auth_login():
    """
    logging in a user given a valid email and username
    return {"u_id": ____, "token": ___} if successful, otherwise error
    """
    payload = request.get_json()
    return dumps(auth.auth_login(payload["email"], payload["password"]))

@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request():
    """
    requesting a password reset for a valid email
    Sends an email containing the reset code to the supplied email address.
    returns {} if successful, otherwise InputError.
    """
    payload = request.get_json()
    result = auth.auth_passwordreset_request(payload["email"])
    code = check_reset_code.code_given_email(payload["email"])

    try:
        msg = Message("Password reset code",
          sender="flockrmail@gmail.com",
           recipients=[payload["email"]])
        msg.body = "Hello,\nhere is your reset code: "+code           
        mail.send(msg)
        return dumps(result)

    except Exception as e:
        return str(e)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset():
    """
    Given a reset code for a user, set that user's new password to the password provided.
    If code provided is invalid or user's new password is unsuitable, raise InputError.
    returns {}
    """
    payload = request.get_json()
    return dumps(auth.auth_passwordreset_reset(payload["reset_code"], payload["new_password"]))

@APP.route("/channel/invite", methods=['POST'])
def channel_invite():
    """
    enables a valid user of a channel to add a user to a channel
    returns {}
    """
    payload = request.get_json()
    return dumps(channel.channel_invite(payload["token"], payload["channel_id"], payload["u_id"]))
    
@APP.route("/channel/details", methods=['GET'])
def channel_details():
    """
    gets the details of a specified channel
    returns {
        'name': _____,
        'owner_members': [
            {    
                'u_id': ____,
                'name_first': ______,
                'name_last': ______,
            }
        ],
        'all_members': [
            {
                'u_id': _,
                'name_first': ______,
                'name_last': ______,
            }
        ],
      }
    """

    token = request.args.get("token") if not None else False
    channel_id = int(request.args.get("channel_id")) if not None else False
    if token and channel_id:
        return dumps(channel.channel_details(token, channel_id))
    else:
        raise InputError(description="channel_id or token can't be read")
    
@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    """
    gets all the messages that have been sent in the channel
    returns {
        'messages' : [
            {
                'message_id' : ____
                'u_id' : _____
                'message' : '_____'
                'time_created' : ______
            }
        ]
        'start' : _____
        'end' : ______
    }
    """
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    start = int(request.args.get("start"))
    return dumps(channel.channel_messages(token, channel_id, start))


@APP.route("/channel/join", methods=['POST'])
def channel_join():
    """
    user joins channel
    return {}
    """
    payload = request.get_json()
    return dumps(channel.channel_join(payload["token"], payload["channel_id"]))

@APP.route("/channel/leave", methods=['POST'])
def channel_leave():
    """
    user leaves channel
    returns {}
    """
    payload = request.get_json()
    return dumps(channel.channel_leave(payload["token"], payload["channel_id"]))

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    """
    user adding owner
    returns {}
    """
    payload = request.get_json()
    return dumps(channel.channel_addowner(payload["token"], payload["channel_id"], payload["u_id"]))

@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    """
    user removing owner
    returns {}
    """
    payload = request.get_json()
    return dumps(channel.channel_removeowner(payload["token"], payload["channel_id"], payload["u_id"]))

@APP.route("/channels/create", methods=['POST'])
def channels_create():
    """
    creates a new channel and returns {"channel_id": ____ }
    """
    payload = request.get_json()
    return dumps(channels.channels_create(payload["token"], payload["name"], payload["is_public"]))

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    """
    lists all channels the user whose token has been passed is a member of
    returns {
        'channels': [
            {
          		'channel_id': _,
          		'name': '______',
          	}
          ],
      }
    """
    token = request.args.get("token")
    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    """
    lists all channels, regardless of membership or private/public
    returns {
        'channels': [
            {
          		'channel_id': _,
          		'name': '______',
          	}
          ],
      }
    """
    token = request.args.get("token")
    return dumps(channels.channels_listall(token))

@APP.route("/message/send", methods=['POST'])
def message_send():
    """
    sends a message to a specified channel
    returns {"message_id" : ____}
    """
    payload = request.get_json()
    return dumps(message.message_send(payload['token'], payload['channel_id'], payload['message']))

@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    """
    remove a message with a specified message_id
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_remove(payload['token'], payload['message_id']))

@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    """
    edits a message with a specified message_id
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_edit(payload['token'], payload['message_id'], payload['message']))


@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    """
    sends a message to a specified channel at a specified time
    returns {"message_id" : ____}
    """
    payload = request.get_json()
    return dumps(message.message_sendlater(payload['token'], payload['channel_id'], payload['message'], payload['time_sent']))

@APP.route("/message/react", methods=['POST'])
def message_react():
    """
    reacts to a specified message
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_react(payload['token'], payload['message_id'], payload['react_id']))

@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    """
    unreacts a specified message
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_unreact(payload['token'], payload['message_id'], payload['react_id']))

@APP.route("/message/pin", methods=['POST'])
def message_pin():
    """
    pins a specified message
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_pin(payload['token'], payload['message_id']))

@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    """
    unpins a specified message
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_unpin(payload['token'], payload['message_id']))

@APP.route("/user/profile", methods=["GET"])
def user_profile():
    """
    gets a specific user's profile information
    returns {
        'u_id' : ___,
        'name_first' : '____',
        'name_last' : '____',
        'handle' : '____',
        'email' : '_____',
    }
    """
    token = request.args.get("token")
    u_id = int(request.args.get("u_id"))
    token = token if token is not None else False
    u_id = u_id if u_id is not None else False
    if token and u_id:
        return dumps(user.user_profile(token, u_id))
    else:
        raise InputError(description="token or u_id is invalid")

@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    """
    enables the user to set their first and last name
    returns {}
    """
    payload = request.get_json()
    return dumps(user.user_profile_setname(payload["token"], payload["name_first"], payload["name_last"]))

@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    """
    enables the user to set their email
    returns {}
    """
    payload = request.get_json()
    return dumps(user.user_profile_setemail(payload["token"], payload["email"]))

@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    '''
    enables the user to set their handle
    return {}
    '''
    payload = request.get_json()
    return dumps(user.user_profile_sethandle(payload["token"], payload["handle"]))

@APP.route("/imgurl/<path:filename>")
def static_returning_images(filename):
    return send_from_directory('imgurl/', filename)

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphoto():
    '''
    enables the user to upload a photo as their profile picture
    return {}
    '''
    payload = request.get_json()
    current_url = request.base_url
    server_url = current_url.replace("/user/profile/uploadphoto", "")
    return dumps(user.user_profile_uploadphoto(payload["token"], payload["img_url"], server_url, payload["x_start"], payload["y_start"], payload["x_end"], payload["y_end"]))

@APP.route("/users/all", methods=['GET'])
def users_all():
    """
    gets a list of all users and their associated details
    returns [
        {
            'u_id' : ___,
            'name_first' : '____',
            'name_last' : '____',
            'handle' : '____',
            'email' : '_____',
        },
        {
            'u_id' : ___,
            'name_first' : '____',
            'name_last' : '____',
            'handle' : '____',
            'email' : '_____',
        }
    ]
    """
    token = request.args.get("token")
    token = token if not None else False

    if token:
        return dumps(other.users_all(token))
    else:
        raise InputError(description="token passed in is None")

@APP.route("/admin/userpermission/change", methods=['POST'])
def change_permissions():
    """
    allows the changing of permissions levels for users/owners
    returns {} 
    """
    payload = request.get_json()
    return dumps(admin_permissions_change.admin_userpermission_change(payload["token"], payload["u_id"], payload["permission_id"]))

@APP.route("/search", methods=["GET"])
def search_messages():
    '''
    Given a query string, return a collection of messages in all of the channels 
    that the user has joined that match the query
    
    returns [
            {
                'message_id' : ____
                'u_id' : _____
                'message' : '_____'
                'time_created' : ______
            }
         ]
    '''
    token = request.args.get("token")
    query = request.args.get("query_str")
    token = token if token is not None else False
    query = query if query is not None else False
    if token and query:
        return dumps(search.search(token, query))
    else:
        raise  InputError(description="token or qeury string is invalid")

@APP.route("/standup/start", methods=['POST'])
def standup_start():
    '''
    For a given channel, start the standup period whereby for
    the next "length" seconds if someone calls "standup_send" with a message.
    returns time_finish for standup period
    '''
    payload = request.get_json()
    return dumps(standup.standup_start(payload["token"], int(payload["channel_id"]), int(payload["length"])))

@APP.route('/standup/active', methods=['GET'])
def standup_active():
    '''
    For a given channel, return whether a standup is active in it,
    and what time the standup finishes. If no standup is active,
    then time_finish returns None
    '''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    token = token if token is not None else False
    channel_id = channel_id if channel_id is not None else False
    if token and channel_id:
        return dumps(standup.standup_active(token, channel_id))
    else:
        raise InputError(description="token or channel_id is invalid")

@APP.route('/standup/send', methods=['POST'])
def standup_send():
    '''
    Sending a message to get buffered in the 
    standup queue, assuming a standup is currently active
    returns {}
    '''
    payload = request.get_json()
    return dumps(standup.standup_send(payload["token"], int(payload["channel_id"]), payload["message"]))

@APP.route("/clear", methods=['DELETE'])
def clear():
    """
    check if all the data is cleared
    should return a empty dictionary
    """
    return dumps(other.clear())

### Keep code above this ###
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
