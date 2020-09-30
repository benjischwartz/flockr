users = {
    'benji.schwartz@gmail.com': {
        'u_id' : 1,
        'name_first' : "benji",
        'name_last' : "schwarz",
        'password' : "abcdefg1234!!!"
    }, 'keshigagopalarajah@gmail.com': {
        'u_id' : 2,
        'name_first' : "Keshiga",
        'name_last' : "Gopal",
        'password' : "abcdefg1234!!!"
    }
        
}

tokens = ['benji.schwartz@gmail.com']

channel = {
    8 : {
        'channel_name' : "First_channel",
        'is_public' : False,
        'owner_members' : {
            1 : True,
            2 : True,
            567 : True
        },
        'all_members' : {
            1 : True,
            2 : True,
            567 : True
        },
        'messages' : [
            { 'message_id' : "1",
              'u_id' : "1",
              'message_content' : "Hi Kesh",
              'time_created' : "5:00pm"
            }, { 'message_id' : "2",
              'u_id' : "2",
              'message_content' : "Hi yourself",
              'time_created' : "6:00pm"
            }
        ]
    }
}      
 
