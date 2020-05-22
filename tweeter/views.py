import os
import requests

from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv

load_dotenv()
def index(request):
    username = os.getenv('TUSERNAME')
    password = os.getenv('TPASSWORD')
    url = os.getenv('TWEETS_URL')

    # data = requests.get(url, auth=(os.getenv(username,password)))

    context = {'tweets': ''}
    return render(request,'tweeter/index.html', context)
