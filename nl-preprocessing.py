import nltk                                # Python library for NLP
from nltk.corpus import twitter_samples    # sample Twitter dataset from NLTK
#import matplotlib.pyplot as plt            # library for visualization
import random
from nltk.corpus.reader import api
from oauthlib.oauth1.rfc5849 import Client

from textblob import TextBlob
import tweepy
import sys

import datetime, time

import re                                  # library for regular expression operations
import string                              # for string operations

from nltk.corpus import stopwords          # module for stop words that come with NLTK
from nltk.stem import PorterStemmer        # module for stemming
from nltk.tokenize import TweetTokenizer   # module for tokenizing strings

from nltk.stem.porter import *

from os import getcwd

def twitter_auth():
    try:
        api_key = '*********************************'
        api_key_secret = '***********************************'
        access_token = '********************************'
        access_token_secret = '***********************************'
    except KeyError:
        sys.stderr.write("TWITTER environment variable is not set\n")
        sys.exit(1)
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def get_twitter_client():
    auth = twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client  

def show_tweets(username, tweetday):
    page = 1
    deadend = False
    tweets_to_analyze = []
    while True:
        tweets = tweepy.Cursor(client.user_timeline, screen_name=username, tweet_mode="extended").items()

        for status in tweets:
            if((datetime.datetime.now() - status.created_at).days) < tweetday: 
               tweets_to_analyze.append(status.full_text)
            else:
                deadend = True
                print("The user tweeted ", len(tweets_to_analyze), " times in ", tweetday, " days")
                return tweets_to_analyze
            if not deadend:
                page + 1
                #time.sleep(1)
                
def tokenize_tweets(tweet):

    tweet2 = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    tweet2 = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet2)

    # remove hashtags
    # only removing the hash # sign from the word
    tweet2 = re.sub(r'#', '', tweet2)

    print(tweet2)

    print()
    print('\033[92m' + tweet2)
    print('\033[94m')
    tweet_sentences.append(tweet2) # **********************************************

    # instantiate tokenizer class
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)

    # tokenize tweets
    tweet_tokens = tokenizer.tokenize(tweet2)

    #print()
    #print('Tokenized string:')
    #print(tweet_tokens)
    return tweet_tokens

    #delete_stopwords(tweet_tokens)

def delete_stopwords(tweet_tokens):

    #Import the english stop words list from NLTK
    stopwords_english = stopwords.words('english')
    stopwords_turkish = stopwords.words('turkish')
    other_punctuation = (':', '”', '“', '’', '’')

    print('\033[92m')
    print('Tokenized string:')
    print(tweet_tokens)
    print('\033[94m')

    tweets_clean = []
    for word in tweet_tokens: # Go through every word in your tokens list
        if (word not in stopwords_english and
            word not in stopwords_turkish and  # remove stopwords
            word not in string.punctuation and
            word not in other_punctuation):  # remove punctuation
            tweets_clean.append(word)

    print('removed stop words and punctuation:')
    print(tweets_clean,'\n')
    print('--------------------------------------------------------')
    return tweets_clean

def stem_it(clean_tweets):
    for stem in clean_tweets:
        print()
        print('\033[92m')
        print(clean_tweets)
        print('\033[94m')

        # Instantiate stemming class
        stemmer = PorterStemmer() 

        # Create an empty list to store the stems
        tweets_stem = [] 

        for word in clean_tweets:
           stem_word = stemmer.stem(word)  # stemming word
           tweets_stem.append(stem_word)  # append to the list

        print('stemmed words:')
        print(tweets_stem)

def sentiment(tweet_sentences):

    polarity = 0
    positive = 0
    negative = 0
    neutral = 0

    for tweet in tweet_sentences:
        if tweet.startswith(' @'):
            position = tweet.index(':')
            tweet = tweet[position + 2:]

        analysis = TextBlob(tweet)
        
        analysis = analysis.translate(from_lang='tr', to = "en")
   
        tweet_polarity = analysis.polarity
        if tweet_polarity > 0.00:
            positive += 1
            positive_tweets.append(tweet)
        elif tweet_polarity < 0.00:
            negative += 1
            negative_tweets.append(tweet)
        elif tweet_polarity == 0.00:
            neutral += 1
            neutral_tweets.append(tweet)
        polarity += tweet_polarity

        print(tweet)
        print(f'Polarity: {tweet_polarity}')
        print()

    print(polarity)
    print(f'Overall polarity is:  {polarity}')
    print(f'Amount of positive tweets : {positive}')
    print(f'Amount of negative tweets : {negative}')
    print(f'Amount of neutral tweets : {neutral}')


def is_foreign():
    is_foreign = input("Is the account you want to analyze is foreign? ")
    return(is_foreign)
    
if __name__ == '__main__':
    nltk.download('stopwords')
    clean_tweets = []
    tweet_sentences = []
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []

    client = get_twitter_client()
    username = input("Enter username: ")
    tweetday = int(input("How many days of tweets you want to analyze: "))

    tweets_to_analyze = show_tweets(username, tweetday)
    print(tweets_to_analyze)

    for tweet in tweets_to_analyze:
        tweet_tokens = tokenize_tweets(tweet)
        tweet_tokens2 = delete_stopwords(tweet_tokens)
        clean_tweets.append(tweet_tokens2)

    sentiment(tweet_sentences)

    print("Positive tweets: ")
    print(positive_tweets)
    print("Negative tweets: ")
    print(negative_tweets)
    print("Neutral tweets: ")
    print(neutral_tweets)

