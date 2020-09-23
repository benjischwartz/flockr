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