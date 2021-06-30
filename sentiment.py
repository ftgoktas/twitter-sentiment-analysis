from textblob import TextBlob
import tweepy
import sys

api_key = '*******************************************'
api_key_secret = '*******************************************'
access_token = '*************************************************'
access_token_secret = '*********************************************'

auth_handler = tweepy.OAuthHandler(consumer_key = api_key, consumer_secret = api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler)

search_term = ''
tweet_amount = 200

tweets = tweepy.Cursor(api.search, q = search_term, lang = 'en').items(tweet_amount)

polarity = 0
positive = 0
negative = 0
neutral = 0

for tweet in tweets:
    final_text = tweet.text.replace('RT', '')
    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position + 2:]
    #if final_text.startswith('@'):
    #   position = final_text.index(' ')
    #  final_text = final_text[position + 2:]
    analysis = TextBlob(final_text)     
    tweet_polarity = analysis.polarity
    if tweet_polarity > 0.00:
        positive += 1
    elif tweet_polarity < 0.00:
        negative += 1
    elif tweet_polarity == 0.00:
        neutral += 1        
    polarity += tweet_polarity

    print(final_text)
    print(f'Polarity: {tweet_polarity}')
    print()

print(polarity)
print(f'Overall polarity is:  {polarity}')
print(f'AMount of positive tweets : {positive}')
print(f'AMount of negative tweets : {negative}')
print(f'AMount of neutral tweets : {neutral}')

# Get data

data = api.user_timeline("elonmusk", tweet_mode = "extended",
                        count = 200, exlude_replies = True)

# Save the data
with open('elon_tweets.csv', mode = 'w', encoding = 'utf-8', newLine = '') as csv_file:
    fieldnames = ['created_at', 'text']
    writer = csv.DictWriter(csv_file, fieldnames)
    writer.writeheader()

    for tweetObject in data:
        writer.writerow('text': deEmojify(tweetObjects.full_text),
                        'created_at': tweetObject.created_at})



