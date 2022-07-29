#First, run: !pip install transformers in the terminal

#Import the required libraries
import tweepy
import time
import pandas as pd
from datetime import datetime, timedelta
import pytz
import re
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax


def clean(text):
    """Returns the cleaned text"""
    
    text = re.sub(r"@\w*", "", text) # remove all words starting with @
    text = re.sub(r"#\w*", "", text)
    text = re.sub(r"http\S*", "", text) 
    text = text.encode('ascii', 'ignore').decode('UTF-8')  #removes unicode chars like emoticons
    return text

def tweets_to_csv(keyword, city):

    client = tweepy.Client("your key")

    # make query: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
    #query = f'"{keyword}" has:geo place:"{city}" lang:en -is:retweet'   # Not sure if has:geo is needed as we use place already?
    query = f'"{keyword}" place:"{city}" lang:en -is:retweet' 

# set timeframe for query
    end_time = datetime.now()
    end_time = pytz.UTC.localize(end_time) # add timezone to make it RFC 3339 compliant

    start_time = datetime(2015, 7, 1, 0, 0, 0, 0) # Go back until Jan 1, 2015
    start_time = pytz.UTC.localize(start_time)

    n = 0 # running total number for scraped tweets

    # data table, will later be converted into a dataframe
    data = {
        "created_at":[],
        # "author_id":[],
        # "geo":[],
        "text":[],
    }

    # Loops through the given time frame.
    while end_time > start_time: 
        tweets = tweepy.Paginator(client.search_all_tweets, 
                            query = query,
                            tweet_fields = ['text',"created_at", "author_id", "geo"],
                            expansions = 'author_id',
                            #start_time = '2021-01-20T00:00:00Z',
                            #end_time = '2022-01-21T00:00:00Z',
                            start_time = start_time,
                            end_time = end_time, 
                            max_results=500).flatten(limit=500)
        got_any_tweets = False

        # go through all tweets we got so far
        for i, tweet in enumerate(tweets):      
            got_any_tweets = True

            text = clean(tweet["text"]) # removes URLs, @ and #

            date = tweet["created_at"]
            print(n+i, date, tweet["geo"], text[:100])

           
            data["created_at"].append(tweet["created_at"])
            # data["geo"].append(tweet["geo"])
            data["text"].append(text) # Store cleaned text
        
        
        n += i
        end_time = date
        time.sleep(1)

        if got_any_tweets == False:
            print("No more tweets, done!")
            break


    # convert to dataframe and save as csv
    # doing this after each block so we have something in case we get a 429 error 
   
    df = pd.DataFrame.from_dict(data)
    file_name = keyword + "_" + city + ".csv"
    df.to_csv(file_name, header=True, index=False)
    print("Saved", n, "tweets in", file_name, "from now, ending at", date)
    return df
    

df = tweets_to_csv("Gun Violence", "Phoenix")

# run with a batch on cities
cities = ["Houston", "Chicago"] 
keyword = "Abortion"

#Running the Sentiment Analysis with trained data

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def run_sentiment_analyzer(data, tokenizer, model):
    # Run for Roberta Model
    encoded_text = tokenizer(data, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2]
    }
    return scores_dict


keyword = "Abortion"
cities = ["Houston", "Chicago"] 


import pandas as pd

# columns for making the data frame later, start with empty list = no rows
data = {"neg":[], "neu":[], "pos":[]}

for city in cities:
    filename = keyword + "_" + city + ".csv"
    df = pd.read_csv(filename)
    text = str(df["text"].values)
    res_dict = run_sentiment_analyzer(text, tokenizer, model)
    
    # append a row of sentiment values to the columns dict 
    data["neg"].append(res_dict["roberta_neg"])
    data["neu"].append(res_dict["roberta_neu"])
    data["pos"].append(res_dict["roberta_pos"])
    

df = pd.DataFrame(data=data, index=cities)
df  # you could save this as csv ....

df.plot.bar(stacked=True,rot=0, title=keyword, figsize=(10,5));

df.plot.bar(rot=0, subplots=True, figsize=(5, 10), legend=False);

keyword = "Abortion"


import pandas as pd

# columns for making the data frame later, start with empty list = no rows
data = {"neg":[], "neu":[], "pos":[]}

for city in cities:
    filename = keyword + "_" + city + ".csv"
    df = pd.read_csv(filename)
    text_lst = list(df["text"].values)
    n = 0
    neg = neu = pos = 0

    print(city, len(text_lst))
    for text in text_lst:
        res_dict = run_sentiment_analyzer(text, tokenizer, model)
        n += 1
        neg += res_dict["roberta_neg"]
        neu += res_dict["roberta_neu"]
        pos += res_dict["roberta_pos"]

        if n % 100 == 0:
          print(n, round(neg/n,2), round(neu/n, 2), round(pos/n, 2))

    
    # append a row of sentiment values to the columns dict 
    data["neg"].append(neg/n)
    data["neu"].append(neu/n)
    data["pos"].append(pos/n)
    

df = pd.DataFrame(data=data, index=cities)


df.plot.bar(rot=0, subplots=True, figsize=(5, 10), legend=False);
