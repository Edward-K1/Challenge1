import os
import requests
import pickle

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
    return raw_data

def get_tweet_statistics(tweet_data):
    return tweet_data

