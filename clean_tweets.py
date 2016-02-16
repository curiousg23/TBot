import feedparser
import tweepy
import requests
import random
import pymongo
import json
import arrow
from bson.objectid import ObjectId

MONGODB_URI = ''
client =  pymongo.MongoClient(MONGODB_URI)
db = client['tweets']


def clean_db():
    collection = db['links']
    collection.delete_many({"timestamp": {"$lte": arrow.utcnow().replace(days=-1).timestamp}})

def clean_img():
    collection = db['imgs']
    collection.delete_many({"timestamp": {"$lte": arrow.utcnow().replace(days=-1).timestamp}})

clean_db()
clean_img()
