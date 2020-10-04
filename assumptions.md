## Data assumptions
*  tokens will be using the email, as emails assumed to be unique

## Channels.py assumptions
* channels_list all will list all channels, whether private or public
* channel_id will be integers, named in the order of creation
* when a channel is created, the user whose token it is matched with, will auto-matically be the first owner and member of that channel

## Channel.py assumptions
* channel_invite – if the user with token 'token' invites themselves or someone else
    who is already in the channel, a message will be printed out notifying the
    the user that the user they are inviting is already in the channel and the function 
    will return an empty dictionary; no exception is raised
* any member of the channel can call these functions (whether they are owner or not is irrelevant)
    - channel_invite
    - channel_details
    - channel_messages
    - channel_leave
* Functions which behave the same whether the channel is private or public are:
    - channel_invite
    - channel_details
    - channel_messages
    - channel_leave
    - channel_addowner
    - channel_removeowner
* channel_messages – raise an InputError if start is less than zero
* channel_addowner - if you make a user an owner of an channel where they are not a member, they become a
member and an owner.
* channel_removeowner – if you remove an owner they become an ordinary member
* channel_removeowner – you can remove an owner even if they are the last owner of the channel
* channel_leave – empty channels should still exist even if the last member leaves whether channel is private or public
* channel_join – raise an AccessError if the user trying to join is already in the channel 

