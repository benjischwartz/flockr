

users = {
    'email': {
        'u_id' : " ",
        'name_first' : " ",
        'name_last' : " ",
        'password' : " ",
        'handle' : " "
        }
    }

tokens = ['benji.schwartz@gmail.com']

channel = { # 'channel_id' are the int values themselves, per channel
    'channel_id' : {
        'channel_name' : " ",
        'is_public' : False,
        'owner_members': { #numbers in owner members are the user ids
            78978 : True,
            223423 : True,
            567 : True
        },
        'all_members' : { #numbers in all members are the user ids
            78978 : True,
            223423 : True,
            567 : True
        },
        'messages' : [ {
            'message_id': 1,
            'u_id' : 1,
            'message_content' : 'Hello',
            'time_created' : 3
            }]
    }
}      
 
