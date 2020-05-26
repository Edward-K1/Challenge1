import os
import requests
import pickle
import re

from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()
def index(request):
    username = os.getenv('TUSERNAME')
    password = os.getenv('TPASSWORD')
    url = os.getenv('TWEETS_URL')

    # raw_data = requests.get(url, auth=(username,password))
    raw_data = get_pickled_data()
    # data = format_tweet_data(raw_data.json())
    data = format_tweet_data(raw_data)
    tweet_stats = get_tweet_statistics(data)

    context = {'tweets': data, 'statistics':tweet_stats}
    return render(request,'tweeter/index.html', context)

def get_pickled_data():
    with open('raw-data.pickle','rb') as rawfile:
        data = pickle.load(rawfile)
    return data

def format_tweet_data(raw_data):
    formatted_tweets = []
    for tweet in raw_data:
        new_tweet_dict = {
            'text':tweet['text'],
            'language':tweet['lang'],
            'retweet_count':tweet['retweet_count'],
            'source':get_tweet_source(tweet),
            'hashtags':get_hash_tags(tweet),
            'name':tweet['user']['name'],
            'screen_name': tweet['user']['screen_name'],
            'profile_image':tweet['user']['profile_image_url'],
            'friends_count':tweet['user']['friends_count'],
            'followers_count':tweet['user']['followers_count'],
            'location':tweet['user']['location'],
            'joined':tweet['user']['created_at'],
        }
        formatted_tweets.append(new_tweet_dict)

    return formatted_tweets

def get_tweet_statistics(tweet_data):
    return tweet_data

def get_tweet_source(tweet):
    return re.sub("<[^>]+>","",tweet['source'])

def get_hash_tags(tweet):
    return [x['text'] for x in tweet['entities']['hashtags']]

