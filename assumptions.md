## Data assumptions
*  tokens will be using the email, as emails assumed to be unique

## Channels.py assumptions
* channels_list all will list all channels, whether private or public
* channel_id will be integers, named in the order of creation
* when a channel is created, the user whose token it is matched with, will auto-matically be the first owner and member of that channel

## Auth.py assumptions
* logging in twice will return the same valid token and user_id
* registering will automatically log the user in with an 
authenticated token
* logging out twice will return {'is_success': False}