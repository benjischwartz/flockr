from data import users, tokens, codes, channel, highest_ids

def data_store():
    #Adding Line by Line
    '''
    with open('src/data.py', 'w') as outfile:
        output = f"users = {users}\n \ntokens = {tokens}\n \ncodes = {codes} \nchannel = {channel} \nhighest_ids = {highest_ids}"
        outfile.write(output)
        outfile.close()
    '''
    outfile =  open('src/data.py', 'w')
    output = f"users = {users}\n \ntokens = {tokens}\n \ncodes = {codes} \nchannel = {channel} \nhighest_ids = {highest_ids}"
    outfile.write(output)


