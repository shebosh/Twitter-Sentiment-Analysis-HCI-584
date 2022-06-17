import tweepy
import time
import pandas as pd
from datetime import datetime, timedelta
import pytz

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAEKKdgEAAAAAqmpzyvS98w%2Ba%2BweD%2FO7YK19kqTA%3DYbEgLyHsYGHBNRt18lTvs6eRXRtfI0JOyYoX8dUmFGD5XsXQ3B")

# make query: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

#query = '#obama lang:en is:verified -is:retweet' # - means no retweets
#query = 'from:BarackObama lang:en  -is:retweet' 
query = 'from:POTUS lang:en  -is:retweet' # Biden

# set timeframe for query
end_time = datetime(2022, 6, 17)
end_time = pytz.UTC.localize(end_time) # add timezone to make it RFC 3339 compliant

start_time =  datetime(2020, 1, 1)
start_time = pytz.UTC.localize(start_time)

n = 0 # running total number for scraped tweets

# data table, will later be converted into a dataframe
data = {
    "created_at":[],
    "author_id":[],
    "geo":[],
    "text":[],
}

# should loop through the given time frame.
# But, I've seen it stuck in an endless loop, if so just 
while end_time > start_time: 
    tweets = tweepy.Paginator(client.search_all_tweets, 
                            query = query,
                            #user_fields = ['username','description'],  # I'm using author_id instead of username
                            tweet_fields = ['text',"created_at", "author_id", "geo"],
                            expansions = 'author_id',
                            #start_time = '2021-01-20T00:00:00Z',
                            #end_time = '2022-01-21T00:00:00Z',
                            end_time = end_time, 
                            max_results=500).flatten(limit=500)

    time.sleep(3)


    # go through all tweets we got so far
    for i, tweet in enumerate(tweets):      
        date = tweet["created_at"]
        print(n+i, date)

        # append those keys to data structure lists
        for k in ["created_at", "author_id", "geo", "text"]:
            data[k].append(tweet[k])
    
    # update total number of tweets and set next end date
    n += i
    end_time = date # use date of last tweet as end_date for next request

    # convert to dataframe and save as csv
    # doing this after each block so we have something in case we get a 429 error 
    df = pd.DataFrame.from_dict(data)
    df.to_csv('tweets.csv', header=True, index=False)
    print("Saved", n, "tweets, ending at", date)


    


#fo.close()



