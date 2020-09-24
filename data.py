
users = {
    'email': {
    'name_first' : " ",
    'name_last' : " ",
    'u_id' : "0023423"
  }
}


channel = {
    'channel_id(int)' : {
        'channel_name(str)' : " ",
        'owner_members(str)': {
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
 

######### channels dict: matches channel_id (int) to channel name (string)
# i.e. key is the channel id integer and value is name of channel
# starter channels: one named "cat", other named "dog"
channels = {
    1 : "cat",
    2 : "dog",
    'totalChannels' : 2,
}