import os

SENTINEL_MONGO_DBNAME = 'adam-oauth'
DEBUG = True

redis_url = os.environ.get('REDIS_URL')
if redis_url:
    SENTINEL_REDIS_URL = redis_url
