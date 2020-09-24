# example global variable(s) for milestone 1 data
data = {
    'users' : {
        'email' : {
            'name_first' : " ",
            'name_last' : " ",
            'u_id' : "0000" ,
        }
    },

    'messages' : {
        'channel' : ['history'],
    }
}
users = {
    'email': {
        'name_first' : " ",
        'name_last' : " ",
        'u_id' : "0023423" ,
    }
}



######### channels dict: matches channel_id (int) to channel name (string)
# i.e. key is the channel id integer and value is name of channel
# starter channels: one named "cat", other named "dog"
channels = {
    1 : "cat",
    2 : "dog",
}

###### TESTING: channels_list user testing  #####
channel_1 = {
    'users' : [],
    'owners' : []
}
channel_1['users'].append("004")
channel_1['users'].append("123")
channel_1['owners'].append("002")

