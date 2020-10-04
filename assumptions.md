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
* owner of flockr is the first user registered, and will thus have u_id of `1`

## Auth.py assumptions
* auth_login - logging in twice will return the same valid token and user_id
* auth_register - registering will automatically log the user in with an 
authenticated token
* auth_register - email entered must be all lowercase, otherwise not a valid email
* auth_register - first user registered will have u_id `1`, and subsequent u_id's will be determined from the number of people registered, thus always unique
* auth_logout - logging out twice will return {'is_success': False}
