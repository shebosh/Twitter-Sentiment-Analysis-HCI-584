# Twitter-Sentiment-Analysis-Project-HCI-584

The program in this project uses Twitter API and scrapes tweets based on key word and a US city.

As a first step, users who would like to use this program should apply for a Twitter developer account. 
The code here is based on the academic research, allowing the user to scrape 10 million tweets a month.
After obtaining the required API keys, the users can proceed to use the code in this project.

To run this program, the users enter a key word they would like to look up, e.g., abortion, and enter a US city, e.g., Houston, and scrape all 
the tweets about that key word from the tweets in that city from the day of the query till the oldest time that key word was mentioned in tweets.

All the scraped tweets are saved as csv files. The name of the csv files are determined as the key word_city name.

After the tweets are scraped, there is a function that clears the tweets from unneccesary text such as http's and leaves only the body text (the tweet)
and the time.

The program, then, allows the user to do a Sentiment Analysis on the csv files and displays the results of the analysis in bar charts,
allowing the user to compare two US cities about one key word.
