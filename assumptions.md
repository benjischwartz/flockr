## Data assumptions
*  tokens will be using the email, as emails assumed to be unique

## Channels.py assumptions
* channels_list all will list all channels, whether private or public
* channel_id will be integers, named in the order of creation
* when a channel is created, the user whose token it is matched with, will auto-matically be the first owner and member of that channel

## Channel.py assumptions
* channel_invite – if the authorised user invites themselves or someone else
    who is already in the channel, a message will be printed out notifying the
    authorised user that the user invitee is in the channel and the function 
    will return; no exception is raised
* channel_invite – any member can invite to the channel (whether they are owner or not is irrelevant) 
* channel_invite – behaves the same whether the channel is private or public
* channel_details – behaves the same whether the channel is private or public
* channel_messages – behaves the same whether the channel is private or public
* channel_messages – raise an InputError if start is less than zero
* channel_leave – empty channels should still exist last person leaves and not deleted whether channel is private or public 
