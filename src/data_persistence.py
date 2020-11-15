from data import users, tokens, codes, channel, highest_ids
import json

def data_store():
    print("OUTDATA")
    print(users)
    all_data = {
        "users": users,
        "tokens": tokens,
        "codes": codes,
        "channel": channel,
        "highest_ids": highest_ids
    }

    with open('src/all_data.json', 'w') as outfile:
        outfile.write(json.dumps(all_data))
        outfile.close()

    #Adding Line by Line
    with open('src/data.py', 'w') as outfile:
        output = f"users = {users}\n \ntokens = {tokens}\n \ncodes = {codes} \nchannel = {channel} \nhighest_ids = {highest_ids}"
        outfile.write(output)
        outfile.close()

def data_retreive():
    return

