from twitter_scraper import TwitterScraper

print('Write name of the file without .json')
file_name = input()
while file_name == '':
    print('Try better') 
    file_name = input()

print('Paste the username that you want to follow')
username = input()
while username == '':
    print('Try better') 
    username = input()

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

scraper = TwitterScraper()
# print(scraper.download_tweets(username, os.getcwd() + '/files/to_adjust/' + file_name, first_token, int(offset)))