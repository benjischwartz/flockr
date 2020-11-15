users = {'firstuser@gmail.com': {'u_id': 1, 'name_first': 'First', 'name_last': 'User', 'password': '$5$rounds=535000$9C1n3NBpp/CYdVje$6INr9TjCiGCThgYkUE7ZmBTElwAw3hbI0J1Pxr3OvXD', 'permission_id': 1, 'handle': 'firstuser', 'profile_img_url': ''}}
 
tokens = ['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImZpcnN0dXNlckBnbWFpbC5jb20ifQ.Kf4u0UK5EshbTYjum776zzwA3vOSjwbJVXadcPfUT50']
 
codes = {} 
channel = {} 
users = {
    # 'email': {
    #     'u_id' : " ",
    #     'name_first' : " ",
    #     'name_last' : " ",
    #     'password' : " ",
    #     'permission_id' : 1, # Global flocker permission_id
    #     # 1 for owner of flocker, 2 for regular members 
    #     'handle' : " ",
    #     'profile_img_url' : " "
    #     }
    }

# tokens are currently the hashed emails of the users
tokens = [
    # 'kdjfakljdflka.skajflkjlkkk.lkjalkfjd'
    ]

# reset password codes temporarily stored in a dictionary
codes = {
    # 'email' : 'code'
}

channel = { # 'channel_id' are the int values themselves, per channel
    # 'channel_id' : {
    #     'channel_name' : " ",
    #     'is_public' : False,
    #     'owner_members': { #numbers in owner members are the user ids
    #         78978 : True, #'True' value is redundant; used because finding keys in dict has faster lookup times than list
    #     },
    #     'all_members' : { #numbers in all members are the user ids
    #         78978 : True, #'True' value is redundant; used because finding keys in dict has faster lookup times than list
    #     },
    #     'messages' : [
    #       {
    #           'message_id': 1,
    #           'u_id': 1,
    #           'message': 'Hello world',
    #           'time_created': 1582426789,
    #           'reacts': [
    #                   { "react_id" : 1 },
    #                   { "u_ids : [1, 3, 4, 5]},
    #                   { "is_this_user_reacted" : False}
    #               ]
    #           'is_pinned' : False
    #       },
    #       {
    #           'message_id': 2,
    #           'u_id': 1,
    #           'message': 'Hello again',
    #           'time_created': 1582426799,
    #       },
    #       'standup' : True,
    #       'standuptime' : 1582426799,
    #       'standuplist' : '',
    #       }
    # }
}

highest_ids = { # for iteration 2, records the highest message_id outputted
    #'highest_message_id' : 2
    }      

