import tweepy
import time
import pandas as pd
from datetime import datetime, timedelta
import pytz
from sentiment_analysis import SentimentAnalysis



def tweets_to_csv(file_name, search_dict):

    client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAEKKdgEAAAAAqmpzyvS98w%2Ba%2BweD%2FO7YK19kqTA%3DYbEgLyHsYGHBNRt18lTvs6eRXRtfI0JOyYoX8dUmFGD5XsXQ3B")

# make query: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    source = search_dict["from"]
    key_word = search_dict["key_word"]
    location = search_dict["location"]
#query = '#obama lang:en is:verified -is:retweet' # - means no retweets
#query = 'from:BarackObama lang:en  -is:retweet' 
    # query = f'{f"from:{source}" if source else "from:MAQErendering"} {key_word if key_word else ""} {location if location else ""}  has:geo (from:NWSHouston) lang:en  -is:retweet' # Biden
    query = f'{key_word} has:geo (from:{location}) lang:en  -is:retweet' # Biden

# set timeframe for query
    end_time = datetime(search_dict["date"][0]+search_dict["date"][-1],search_dict["date"][1],search_dict["date"][2])
    end_time = pytz.UTC.localize(end_time) # add timezone to make it RFC 3339 compliant

    start_time =  datetime(search_dict["date"][0],search_dict["date"][1],search_dict["date"][2])
    start_time = pytz.UTC.localize(start_time)

    n = 0 # running total number for scraped tweets

# data table, will later be converted into a dataframe
    data = {
    "created_at":[],
    "author_id":[],
    "geo":[],
    "text":[],
    }

# Loops through the given time frame.
    while end_time > start_time: 
        tweets = tweepy.Paginator(client.search_all_tweets, 
                            query = query,
                            #user_fields = ['username','description'],  # I'm using author_id instead of username
                            tweet_fields = ['text',"created_at", "author_id", "geo"],
                            expansions = 'author_id',
                            #start_time = '2021-01-20T00:00:00Z',
                            #end_time = '2022-01-21T00:00:00Z',
                            start_time = start_time,
                            end_time = end_time, 
                            max_results=500).flatten(limit=500)
        
        

        time.sleep(3)

    
        got_any_tweets = False

    # go through all tweets we got so far
        for i, tweet in enumerate(tweets):      
            got_any_tweets = True
            date = tweet["created_at"]
            print(n+i, date)

        # append those keys to data structure lists
            for k in ["created_at", "author_id", "geo", "text"]:
                data[k].append(tweet[k])
        n += i
        end_time = date
        if got_any_tweets == False:
            print("No more tweets, done!")
            break


    # convert to dataframe and save as csv
    # doing this after each block so we have something in case we get a 429 error 
   
    df = pd.DataFrame.from_dict(data)

    df.to_csv(f'{file_name}.csv', header=True, index=False)
    print("Saved", n, "tweets, ending at", date)
    SentimentAnalysis.analyzer(df["text"])

tweets_to_csv("BillGates", {"from": "BillGates", "location": "", "key_word": "", "date": (2018,1,1,4)})