from sys import hash_info
from decouple import config
import json
import os

# INPUT: file name of the json downloaded
# OUTPUT: the next token, so the string rapresenting the oldest tweets before the json ones
def read_next_token(name_file):
    with open (name_file) as json_file:
        data = json.load(json_file)
        if 'meta' in data:
            return data['meta']['next_token']
        else:
            return 'error'

# INPUT: 
    # id_user, the twitter id of the person which i want the tweets
    # bearer_token, the token imported from the .env file
    # file_name, the file in which i want to save the json data (without extension)
    # token, the token rapresenting the next pagination
# OUTPUT: the string representing the query, ready to be excecuted
def query(id_user, bearer_token, file_name, token = ''):
    query = 'curl "https://api.twitter.com/2/users/' + id_user + '/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=author_id,context_annotations,conversation_id,created_at,geo,id,in_reply_to_user_id,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results=100&' + token + '" -H "Authorization: Bearer ' + bearer_token + '" > ' + file_name
    return query

# INPUT:
    # id_user, the twitter id of the person which i want the tweets
    # bearer_token, the token imported from the .env file
    # file_name_origin, the file in which i want to save the json data (without extension)
    # first_token, the first token where I start the pagination
    # offset, the offset number that i could use as a start for the numbering of the json files
# OUTPUT: return 'completed', if all went weel. 'error' otherwise
def download_tweets(id_user, bearer_token, file_name_origin, first_token, offset):
    result = 'completed'
    i = 0
    name_file = str(file_name_origin) + '_' + str(i + offset) + '.json'

    if first_token == '':
        query_str = query(id_user, bearer_token, name_file )
    else:
        query_str = query(id_user, bearer_token, name_file, first_token)

    # Excecute the query on the terminal
    os.system(query_str)

    # if there isn't the next_token, there is an error on the download
    next_token = read_next_token(name_file)
    if next_token == 'error':
        result = 'error'
    else:
        token = 'pagination_token=' + next_token

    while i < 31 and result == 'ok':
        i += 1
        name_file = str(file_name_origin) + '_' + str(i + offset) + '.json'

        query_str = query(id_user, bearer_token, name_file, token)

        # Excecute the query on the terminal
        os.system(query_str)

        # if there isn't the next_token, there is an error on the download
        next_token = read_next_token(name_file)
        if next_token == 'error':
            result = 'error'
        else:
            token = 'pagination_token=' + next_token

    return result



print('Write name of the file without .json')
file_name = input()
while file_name == '':
    print('Try better') 
    file_name = input()

print('Paste the id that you want to follow')
id_user = input()
while id_user == '':
    print('Try better') 
    id_user = input()

print('Have you the first token? y/n')
first_token = input()
while first_token != 'y' and first_token != 'n':
    print('Try better') 
    first_token = input()

if first_token == 'n':
    first_token = ''
    offset = 1
else:
    print('Paste your token')
    first_token = input()
    while first_token == '':
        print('Try better') 
        first_token = input()
    first_token = 'pagination_token=' + first_token

    print('Paste your number of file')
    offset = input()
    while offset == '':
        print('Try better') 
        offset = input()

bearer_token = config('bearer_token')
print(download_tweets(id_user, bearer_token, os.getcwd() + '/files/' + file_name, first_token, int(offset)))