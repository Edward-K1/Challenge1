import os
import requests
import pickle
import re
import json

from collections import defaultdict
from django.shortcuts import render
from dotenv import load_dotenv
from django.core.serializers.json import DjangoJSONEncoder

load_dotenv()
def index(request):
    username = os.getenv('TUSERNAME')
    password = os.getenv('TPASSWORD')
    url = os.getenv('TWEETS_URL')

    raw_data = requests.get(url, auth=(username,password))
    # raw_data = get_pickled_data()
    data = format_tweet_data(raw_data.json())
    # data = format_tweet_data(raw_data)
    tweet_stats = get_tweet_statistics(data)

    context = {"tweets": data, "languages":tweet_stats[0],"sources":tweet_stats[1]}
    return render(request,'tweeter/index.html',context)

def get_pickled_data():
    with open('raw-data.pickle','rb') as rawfile:
        data = pickle.load(rawfile)
    return data

def format_tweet_data(raw_data):
    formatted_tweets = []
    for tweet in raw_data:
        new_tweet_dict = {
            "text":tweet["text"],
            "language":tweet["lang"],
            "retweet_count":tweet["retweet_count"],
            "source":get_tweet_source(tweet),
            "hashtags":get_hash_tags(tweet),
            "name":tweet["user"]["name"],
            "screen_name": tweet["user"]["screen_name"],
            "profile_image":tweet["user"]["profile_image_url"],
            "friends_count":tweet["user"]["friends_count"],
            "followers_count":tweet["user"]["followers_count"],
            "location":tweet["user"]["location"],
            "joined":tweet["user"]["created_at"],
        }
        formatted_tweets.append(new_tweet_dict)

    return formatted_tweets

def get_tweet_statistics(tweet_data):
    language_map = load_languages()
    language_codes =[x['language'] for x in tweet_data]
    unique_language_codes = set(language_codes)
    language_stats = {language_map[x]: language_codes.count(x) for x in unique_language_codes}

    tweet_sources = [x['source'] for x in tweet_data]
    unique_sources = set(tweet_sources)
    source_stats = {x: tweet_sources.count(x) for x in tweet_sources}
    stats = language_stats, source_stats

    return stats

def get_tweet_source(tweet):
    source = re.sub("<[^>]+>","",tweet['source'])
    source = re.sub("[\w]+ for ","",source)
    return source

def get_hash_tags(tweet):
    return [x['text'] for x in tweet['entities']['hashtags']]

def load_languages():
    with open("languages.dat","r") as language_file:
        language_data = language_file.readlines()

    language_dict = {x.split(':')[0]:f"{x.split(':')[1]}".strip() for x in language_data}
    safe_dict = defaultdict(lambda: "Unknown")
    safe_dict.update(language_dict)

    return safe_dict

