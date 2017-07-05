import os
import urllib

# TODO remove
DEBUG = True

uri = os.environ.get('MONGO_URI', 'localhost:27017')
user = os.environ.get('MONGO_USERNAME')
if user:
    pw = urllib.parse.quote_plus(os.environ.get('MONGO_PASSWORD'))
    auth = '%s:%s@' % (user, pw)
else:
    auth = ''

SENTINEL_MONGO_URI = "mongodb://%s%s" % (auth, uri)
SENTINEL_MONGO_DBNAME = 'adam-oauth'

redis_url = os.environ.get('REDIS_URL')
if redis_url:
    SENTINEL_REDIS_URL = redis_url
