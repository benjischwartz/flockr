## Data assumptions
*  tokens will be using the email, as emails assumed to be unique

## Channels.py assumptions
* channels_list all will list all channels, whether private or public
* channel_id will be integers, named in the order of creation
* when a channel is created, the user whose token it is matched with, will auto-matically be the first owner and member of that channel

## Channel.py assumptions
* channel_invite – if the user with token 'token' invites themselves or someone else
    who is already in the channel, raise an inputerror
* Functions which behave the same whether the channel is private or public are:
    - channel_invite
    - channel_details
    - channel_messages
    - channel_leave
    - channel_addowner
    - channel_removeowner
* channel_addowner - if you make a user an owner of an channel where they are not a member, they become a
member and an owner.
* channel_messages – raise an InputError if start is less than zero
* channel_removeowner - if you remove an owner they become an ordinary member
* channel_removeowner – you can remove an owner even if they are the last owner of the channel
* channel_leave – empty channels should still exist even if last member leaves and shouldn't be deleted whether the channel is private or public
* channel_join – raise an AccessError if the user trying to join is already in the channel 

## Auth.py assumptions
* auth_login - logging in twice will return the same valid token and user_id
* auth_register - registering will automatically log the user in with an 
authenticated token
* auth_register - email entered must be all lowercase, otherwise not a valid email
* auth_register - first user registered will have u_id `1`, and subsequent u_id's will be determined from the number of people registered, thus always unique
* auth_logout - logging out twice will return {'is_success': False}
* owner of flockr is the first user registered, and will thus have u_id of `1`
* handle generation - No more than 99 people with the same name will register (otherwise handle will be > 20 characters)
* Passwords will be encoded with sha256_crypt from the passlib library



## message.py assumptiosn
* message_send/message_sendlater - first message will have message_id `1`, and subsequent message_ids will be each incremented by 1, thus always unique
* message_edit/message_remove - must be a member of the channel with the message to use message_edit or message_remove, thus
    * owners of flockr cannot remove/edit a message if they are not at least a regular member of the channel, and
    * the user who sent the message cannot remove/edit the message if they have left the channel 
    - raise an AccessError if the user is not a member of the channel (based on the spec requirement for message_pin) 
      regardless of whether the user is an owner of Flockr or a regular Flockr user
* message_send/message_sendlater - raise an InputError if the input 'message' is an empty string
* message_edit - 'time_created' is NOT updated when a message is edited 
* message_edit - raise an InputError if the input 'message' is over 1000 characters
* pinning messages - when message_send creates a message, by default is_pinned is False (so default status of a message is unpinned).
* message_react - a user cannot have multiple reacts for one message eg. user one cannot react to message with message_id 1 with both react_id 1 and react_id 2 (if hypothetically a react_id of 2 is a valid react_id)


