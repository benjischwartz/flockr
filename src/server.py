import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channels
import channel
import admin_permissions_change
import message
import search
import user
import users
import other

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

@APP.route("/auth/register/", methods=['POST'])
def auth_register():
    """
    creating a user in data.py's users dictionary
    return {u_id : ___ , token: _____ }
    """
    payload = request.get_json()
    return auth.auth_register(payload["email"], payload["password"], payload["name_first"], payload["name_last"])

@APP.route("/auth/logout/", methods=['POST'])
def auth_logout():
    """
    logging out a user given a valid token
    return {"is_success": True} if successful, otherwise {"is_success": False}
    """
    payload = request.get_json()
    return dumps(auth.auth_logout(payload["token"]))

@APP.route("/auth/login/", methods=['POST'])
def auth_login():
    """
    logging in a user given a valid email and username
    return {"u_id": ____, "token": ___} if successful, otherwise error
    """
    payload = request.get_json()
    return dumps(auth.auth_login(payload["email"], payload["password"]))

@APP.route("/channel/invite/", methods=['POST'])
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
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    token = token if not None else False
    channel_id = int(channel_id) if not None else False
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
            'message_id' : ____
            'u_id' : _____
            'message' : '_____'
            'time_created' : ______
            ]
        'start' : _____
        'end' : ______
    }
    """
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    start = int(request.args.get("start"))
    return dumps(channel.channel_messages(token, channel_id, start))

@APP.route("/channels/create/", methods=['POST'])
def channels_create():
    """
    Creates a new channel and returns {"channel_id": ____ }
    if successful
    """
    payload = request.get_json()
    return dumps(channels.channels_create(payload["token"], payload["name"], payload["is_public"]))

@APP.route("/channels/list", methods=['GET'])
def channels_list():
    """
    Lists all channels the user, whose token is passed, is a member of
    """
    token = request.args.get("token")
    return dumps(channels.channels_list(token))

@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    """
    Lists all channels, regardless of membership or private/public
    """
    token = request.args.get("token")
    return dumps(channels.channels_listall(token))

@APP.route("/channel/join/", methods=['POST'])
def channel_join():
    """
    User joins channel
    return {}
    """
    payload = request.get_json()
    return dumps(channel.channel_join(payload["token"], payload["channel_id"]))

@APP.route("/channel/leave/", methods=['POST'])
def channel_leave():
    """
    User leaves channel
    return {}
    """
    payload = request.get_json()
    return dumps(channel.channel_leave(payload["token"], payload["channel_id"]))

@APP.route("/channel/addowner/", methods=['POST'])
def channel_addowner():
    """
    User adding owner
    return {}
    """
    payload = request.get_json()
    return dumps(channel.channel_addowner(payload["token"], payload["channel_id"], payload["u_id"]))

@APP.route("/channel/removeowner/", methods=['POST'])
def channel_removeowner():
    """
    User removing owner
    return {}
    """
    payload = request.get_json()
    return dumps(channel.channel_removeowner(payload["token"], payload["channel_id"], payload["u_id"]))

@APP.route("/admin/userpermission/change/", methods=['POST'])
def change_permissions():
    """
    Allows the changing of permissions levels for users/owners
    return {} if successful, otherwise throws error
    """
    payload = request.get_json()
    return dumps(admin_permissions_change.change_permissions(payload["token"], payload["u_id"], payload["permission_id"]))

@APP.route("/message/send/", methods=['POST'])
def message_send():
    """
    sends a message to a specified channel
    returns {"message_id" : ____}
    """
    payload = request.get_json()
    return dumps(message.message_send(payload['token'], payload['channel_id'], payload['message']))

@APP.route("/message/remove/", methods=['DELETE'])
def message_remove():
    """
    remove a message with a specified message_id
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_remove(payload['token'], payload['message_id']))

@APP.route("/message/edit/", methods=['PUT'])
def message_edit():
    """
    edits a message with a specified message_id
    returns {}
    """
    payload = request.get_json()
    return dumps(message.message_edit(payload['token'], payload['message_id'], payload['message']))

@APP.route("/search", methods=["GET"])
def search_messages():
    token = request.args.get("token")
    query = request.args.get("query_str")
    token = token if token is not None else False
    query = query if query is not None else False
    if token and query:
        return dumps(search.search(token, query))
    else:
        raise  InputError(description="token or qeury string is invalid")

@APP.route("/user/profile/setname/", methods=['PUT'])
def user_profile_setname():
    """
    User set name
    return {}
    """
    payload = request.get_json()
    return dumps(user.user_profile_setname(payload["token"], payload["name_first"], payload["name_last"]))

@APP.route("/user/profile/setemail/", methods=['PUT'])
def user_profile_setemail():
    """
    User set email
    return {}
    """
    payload = request.get_json()
    return dumps(user.user_profile_setemail(payload["token"], payload["email"]))

@APP.route("/users/all", methods=['GET'])
def users_all():
    """
    Returns all the user information
    """
    token = request.args.get("token")
    token = token if not None else False

    if token:
        return dumps(users.users_all(token))
    else:
        raise InputError(description="token passed in is None")

@APP.route("/clear/", methods=['DELETE'])
def clear():
    """
    Check if all the data is cleared
    should return a empty dictionary
    """
    return dumps(other.clear())

### Keep code above this ###
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
