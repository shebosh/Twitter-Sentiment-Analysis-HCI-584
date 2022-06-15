import tweepy
import time
import pandas as pd
import re


client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAEKKdgEAAAAAqmpzyvS98w%2Ba%2BweD%2FO7YK19kqTA%3DYbEgLyHsYGHBNRt18lTvs6eRXRtfI0JOyYoX8dUmFGD5XsXQ3B")


result = []
search = ["obama", "trump"]
data = {
    "text": {},
    "username": {},
    "created_at": {}
}
y = 0

for item in search:
    for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = f'#{item} lang:en',
                                 user_fields = ['username','description'],
                                 tweet_fields = [ 'text',"created_at"],
                                 expansions = 'author_id',
                                 start_time = '2021-01-20T00:00:00Z',
                                 end_time = '2022-01-21T00:00:00Z',
                              max_results=500,limit=100):
        print("done")
        i = 0
        time.sleep(0.5)
        for tweet in response[0]:
            data["text"][y] = tweet["data"]["text"]
            try:
                data["username"][y] = response[1]["users"][i]["username"]
            except: 
                data["username"][y] = ""
            data["created_at"][y] = tweet["data"]["created_at"]
            i += 1
            y += 1

(pd.DataFrame.from_dict(data=data, orient='index')
   .to_csv('dict_file.csv', header=False))
    
    
print(result)


