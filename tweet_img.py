import feedparser
import tweepy
import requests
import os
import random
import pymongo
import json
import arrow
from bson.objectid import ObjectId

auth = tweepy.OAuthHandler('','')
auth.set_access_token('', '')

api = tweepy.API(auth)
PHOTO_FEEDS = ['']

MONGODB_URI = ''
client =  pymongo.MongoClient(MONGODB_URI)
db = client['tweets']
collection = db['imgs']

def tweet_image():
    for url in PHOTO_FEEDS:
        d = feedparser.parse(url)
        image_posted = False
        for entry in d['entries']:
            request = requests.get(entry.media_content[0]['url'], stream=True)
            filename = 'temp.jpg'
            if request.status_code == 200:
                with open(os.path.join(os.getenv("OPENSHIFT_DATA_DIR"), filename), 'wb') as image:
                    for chunk in request:
                        image.write(chunk)

                api.update_with_media(os.path.join(os.getenv("OPENSHIFT_DATA_DIR"), filename), status="#foodporn")
                os.remove(os.path.join(os.getenv("OPENSHIFT_DATA_DIR"), filename))
                collection.insert({"guid": entry['guid'],
                    "timestamp": arrow.utcnow().timestamp
                })
                image_posted = True
                break
            else:
                print("Unable to download image")

        if image_posted is True:
            break

time_str = arrow.utcnow().format('YYYY-MM-DD HH:mm:ss ZZ')
# tweet + update from 8am-8pm est
if 13 > int(time_str[11:13]) and 1 < int(time_str[11:13]):
    pass
else:
    tweet_image()
