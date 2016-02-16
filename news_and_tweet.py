import feedparser
import tweepy
import requests
import random
import pymongo
import json
import arrow
from bson.objectid import ObjectId

auth = tweepy.OAuthHandler('','')
auth.set_access_token('', '')

api = tweepy.API(auth)

MONGODB_URI = ''
# URLS HERE
URLS = ['']
client =  pymongo.MongoClient(MONGODB_URI)
db = client['tweets']
collection = db['links']
# gather news from rss feeds
def update_news():
    for idx, url in enumerate(URLS):
        d = feedparser.parse(url)
        for entry in d['entries']:
            if collection.find_one({"guid": entry.guid}) is None:
                collection.insert({
                    "title" : entry.title,
                    "link": entry.link,
                    "guid": entry.guid,
                    "url": url,
                    "timestamp": arrow.utcnow().timestamp,
                    "tweeted": 0
                })

def shorten_string(string):
    if (len(string) < 94):
        return string
    string = string[:93]
    i = string.rfind(" ")
    return string[:i] + "..."

def pic_tweet():
    d = feedparser.parse('')
    entry = d['entries'][1]
    print entry.media_content[0]['url']
    api.update_status("#foodporn " + entry.media_content[0]['url'])

pic_tweet()


# post stuff to twitter at reg time intervals
def tweet():
    cursor = collection.find({"tweeted": 0}).limit(1)
    if cursor.count() > 0:
        for doc in cursor:
            # shorten url and post to twitter w/title
            try:
                api.update_status(shorten_string(doc['title']) + " " + doc['link'] + " #FoodNews #foodies")
                collection.update_one({"guid": doc['guid']}, {"$set": {"tweeted": 1}})
            except:
                pass
