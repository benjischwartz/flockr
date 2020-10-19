import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channels
import channel
import admin_permissions_change

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
    return auth.auth_logout(payload["token"])

@APP.route("/auth/login/", methods=['POST'])
def auth_login():
    """
    logging in a user given a valid email and username
    return {"u_id": ____, "token": ___} if successful, otherwise error
    """
    payload = request.get_json()
    return auth.auth_login(payload["email"], payload["password"])

@APP.route("/channels/create/", methods=['POST'])
def channels_create():
    """
    Creates a new channel and returns {"channel_id": ____ }
    if successful
    """
    payload = request.get_json()
    return channels.channels_create(payload["token"], payload["name"], payload["is_public"])

@APP.route("/channels/list/", methods=['GET'])
def channels_list():
    """
    Lists all channels the user, whose token is passed, is a member of
    """
    payload = request.get_json()
    return channels.channels_list(payload["token"])

@APP.route("/channels/listall/", methods=['GET'])
def channels_listall():
    """
    Lists all channels, regardless of membership or private/public
    """
    payload = request.get_json()
    return channels.channels_listall(payload["token"])

@APP.route("/channel/join/", methods=['POST'])
def channel_join():
    """
    User joins channel
    return {}
    """
    payload = request.get_json()
    return channel.channel_join(payload["token"], payload["channel_id"])

@APP.route("/channel/leave/", methods=['POST'])
def channel_leave():
    """
    User leaves channel
    return {}
    """
    payload = request.get_json()
    return channel.channel_leave(payload["token"], payload["channel_id"])

@APP.route("/channel/addowner/", methods=['POST'])
def channel_addowner():
    """
    User adding owner
    return {}
    """
    payload = request.get_json()
    return channel.channel_addowner(payload["token"], payload["channel_id"], payload["u_id"])

@APP.route("/channel/removeowner/", methods=['POST'])
def channel_removeowner():
    """
    User removing owner
    return {}
    """
    payload = request.get_json()
    return channel.channel_removeowner(payload["token"], payload["channel_id"], payload["u_id"])

@APP.route("/admin/userpermission/change/", methods=['POST'])
def change_permissions():
    """
    Allows the changing of permissions levels for users/owners
    return {} if successful, otherwise throws error
    """
    payload = request.get_json()
    return admin_permissions_change.change_permissions(payload["token"], payload["u_id"], payload["permission_id"])
    
### Keep code above this ###
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
