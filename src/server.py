import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth

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


### Keep code above this ###
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
