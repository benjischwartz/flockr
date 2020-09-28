# example global variable(s) for milestone 1 data
data = {
    'users' : {
        'email' : {
            'name_first' : " ",
            'name_last' : " ",
            'u_id' : "0000" ,
        }
    },
    'channels' : {
        'u_id' : "name"
    },
    'messages' : {
        'channel' : ['history'],
    }
}

# example register function
# login can look up dict using email as key for quick
def register(email, password, name_first, name_last):
    userInfo = dict()
    userInfo['password'] = password
    userInfo['name_first'] = name_first
    userInfo['name_last'] = name_last
    # TODO generate and add unique id
    data['users'][email] = userInfo

users = {
    'email': {
        'u_id' : " ",
        'name_first' : " ",
        'name_last' : " ",
        'password' : " "
    }
}

tokens = ['benji.schwartz@gmail.com']

channel = {
    'channel_id(int)' : {
        'channel_name(str)' : " ",
        'is_public' : False,
        'owner_members(str)' : {
            78978 : True,
            223423 : True,
            567 : True
        },
        'all_members(str)' : {
            78978 : True,
            223423 : True,
            567 : True
        },
        'messages(str)' : {
            'message(int)' : {
              'u_id(int)' : " ",
              'message_content' : " ",
              'time' : " "
            }
        }
    }
}      
