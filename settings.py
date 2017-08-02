import os
import urllib

if not os.environ.get('PORT'):
    DEBUG = True

uri = os.environ.get('MONGO_URI', 'localhost:27017/adam-auth')
user = os.environ.get('MONGO_USERNAME')
if user:
    pw = urllib.parse.quote_plus(os.environ.get('MONGO_PASSWORD'))
    auth = '%s:%s@' % (user, pw)
else:
    auth = ''

MONGO_URI = "mongodb://%s%s" % (auth, uri)
REDIS_URL = os.environ.get('REDIS_URL')
STRIPE_KEY = os.environ.get('STRIPE_API_KEY', 'sk_test_4VgrtV4Mv1yRArMFVUlZ5LyB')
