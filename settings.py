import os
import urllib

DEBUG = True

user = os.environ.get('MONGO_USERNAME', 'user')
pw = urllib.parse.quote_plus(os.environ.get('MONGO_PASSWORD', 'pw'))
uri = os.environ.get('MONGO_URI', 'localhost')
SENTINEL_MONGO_URI = "mongodb://%s:%s%s" % (user, pw, uri)
SENTINEL_MONGO_DBNAME = 'adam-oauth'

redis_url = os.environ.get('REDIS_URL')
if redis_url:
    SENTINEL_REDIS_URL = redis_url
