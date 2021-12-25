from decouple import config
import json
import os

class TwitterScraper(object):
    def __init__(self):
        self.bearer_token = config('bearer_token')

# PRIVATE METHODS
    # INPUT: file name of the json downloaded
    # OUTPUT: the next token, so the string rapresenting the oldest tweets before the json ones
    def __read_next_token(self, name_file):
        with open (name_file) as json_file:
            data = json.load(json_file)
            if 'meta' in data:
                return data['meta']['next_token']
            else:
                return 'error'

    # INPUT: 
        # id_user, the twitter id of the person which i want the tweets
        # file_name, the file in which i want to save the json data (without extension)
        # token, the token rapresenting the next pagination
    # OUTPUT: the string representing the query, ready to be excecuted
    def __query_pagination(self, id_user, file_name, token = ''):
        query = 'curl "https://api.twitter.com/2/users/' + id_user + '/tweets?expansions=attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id&tweet.fields=author_id,context_annotations,conversation_id,created_at,geo,id,in_reply_to_user_id,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type&poll.fields=duration_minutes,end_datetime,id,options,voting_status&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics&max_results=100&' + token + '" -H "Authorization: Bearer ' + self.bearer_token + '" > ' + file_name
        print(query)
        return query

    def __get_id_from_username(self, username):
        json_result = os.popen('curl "https://api.twitter.com/2/users/by/username/' + username + '?user.fields=id" -H "Authorization: Bearer ' + self.bearer_token + '"')
        result = json.load(json_result)

        if 'data' in result:
            return result['data']['id']
        else:
            return 'Username not valid'


# PUBLIC METHODS
    # INPUT:
        # username, the twitter username of the person which i want the tweets
        # file_name_origin, the file in which i want to save the json data (without extension)
        # first_token, the first token where I start the pagination
        # offset, the offset number that i could use as a start for the numbering of the json files
    # OUTPUT: return 'completed', if all went weel. 'error' otherwise
    def download_tweets_pagination(self, username, file_name_origin, first_token, offset):
        id_user = self.__get_id_from_username(username)

        result = 'completed'
        i = 0
        name_file = str(file_name_origin) + '_' + f'{(i + offset):04}' + '.json'

        if first_token == '':
            query_str = self.__query_pagination(id_user, name_file)
        else:
            query_str = self.__query_pagination(id_user, name_file, first_token)

        # Excecute the query on the terminal
        os.system(query_str)

        # if there isn't the next_token, there is an error on the download
        next_token = self.__read_next_token(name_file)
        if next_token == 'error':
            result = 'error'
        else:
            token = 'pagination_token=' + next_token

        while i < 31 and result == 'completed':
            i += 1
            name_file = str(file_name_origin) + '_' + f'{(i + offset):04}' + '.json'

            query_str = self.__query_pagination(id_user, name_file, token)

            os.system(query_str)

            next_token = self.__read_next_token(name_file)
            if next_token == 'error':
                result = 'error'
            else:
                token = 'pagination_token=' + next_token

        return result