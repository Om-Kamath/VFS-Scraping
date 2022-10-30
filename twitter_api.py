import tweepy
import pandas as pd
from configparser import ConfigParser


#configuration
config = ConfigParser()
config.read('Scraper/config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authorization
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

#querying
query_topic = '@VFSGlobal OR @Vfsglobalcare__ AND urgent OR help -filter:retweets'
tweets = tweepy.Cursor(api.search_tweets, q=query_topic,count=200,tweet_mode='extended',result_type='recent').items(200)

#converting to dataframe
columns = ['User','Tweet','Date and Time']
data = []

for tweet in tweets:
    text = tweet.full_text.split()
    resultwords  = filter(lambda x:x[0]!='@', text)
    result = ' '.join(resultwords)
    data.append([tweet.user.screen_name,result, tweet.created_at])

df = pd.DataFrame(data,columns=columns)

print(df)

#converting to csv
df.to_csv('Scraper/tweets.csv')



