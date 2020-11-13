

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
    #       },
    #       {
    #           'message_id': 2,
    #           'u_id': 1,
    #           'message': 'Hello again',
    #           'time_created': 1582426799,
    #       }
    #     ]
    # }
}

highest_ids = { # for iteration 2, records the highest message_id outputted
    #'highest_message_id' : 2
    }      

