## Data assumptions
*  tokens will be using the email, as emails assumed to be unique

## Channels.py assumptions
* channels_list all will list all channels, whether private or public
* channel_id will be integers, named in the order of creation
* when a channel is created, the user whose token it is matched with, will auto-matically be the first owner and member of that channel

## Channel.py assumptions
* channel_invite – if the authorised user invites themselves or someone else already in the channel nothing will happen
* in the situation that an unauthorised user invites an invalid user there will be an AccessError
