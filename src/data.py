import json

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

all_data = {
        "users": users,
        "tokens": tokens,
        "codes": codes,
        "channel": channel,
        "highest_ids": highest_ids
}     

def data_store():
    global all_data
    global users
    global tokens
    global codes
    global channel
    global highest_ids
    all_data = {
        "users": users,
        "tokens": tokens,
        "codes": codes,
        "channel": channel,
        "highest_ids": highest_ids
    }

    with open('src/all_data.json', 'w') as outfile:
        json.dump(all_data, outfile)

def data_retreive():
    global all_data
    global users
    global tokens
    global codes
    global channel
    global highest_ids

    with open('src/all_data.json') as infile:
        try:
            all_data = json.load(infile)
            users = all_data['users']
            tokens = all_data['tokens']
            codes = all_data['codes']
            channel = all_data['channel']
            highest_ids = all_data['highest_ids']
        except:
            return
