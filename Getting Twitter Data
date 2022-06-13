import tweepy
import time
import pandas as pd


client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAEKKdgEAAAAAqmpzyvS98w%2Ba%2BweD%2FO7YK19kqTA%3DYbEgLyHsYGHBNRt18lTvs6eRXRtfI0JOyYoX8dUmFGD5XsXQ3B")


obama = []
for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = '#obama lang:en',
                                 user_fields = ['username','description'],
                                 tweet_fields = [ 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-01-20T00:00:00Z',
                                 end_time = '2022-01-21T00:00:00Z',
                              max_results=500,limit=100):
    time.sleep(1)
    obama.append(response)
print(obama)

trump = []
for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = '#trump lang:en',
                                 user_fields = ['username','description'],
                                 tweet_fields = [ 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-01-20T00:00:00Z',
                                 end_time = '2022-01-21T00:00:00Z',
                              max_results=500,limit=100):
    time.sleep(1)
    trump.append(response)
print(trump)

biden = []
for response in tweepy.Paginator(client.search_all_tweets, 
                                 query = '#biden lang:en',
                                 user_fields = ['username','description'],
                                 tweet_fields = [ 'text'],
                                 expansions = 'author_id',
                                 start_time = '2021-01-20T00:00:00Z',
                                 end_time = '2022-01-21T00:00:00Z',
                              max_results=500,limit=100):
    time.sleep(1)
    biden.append(response)
print(biden)


