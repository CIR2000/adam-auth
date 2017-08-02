import os
import stripe
from redis import StrictRedis
from datetime import datetime

from flask import Flask, abort, request
from pymongo import MongoClient

port = os.environ.get('PORT')
if port:
    host = '0.0.0.0'
    port = int(port)
    context = None  # ssl provided by the heroku host
else:
    host = '127.0.0.1'
    port = 8000
    context = ('server.crt', 'server.key')

app = Flask(__name__)
app.config.from_object('settings')

mongo = MongoClient(app.config['MONGO_URI'])
db = mongo['adam-auth']
redis = StrictRedis(app.config['REDIS_URL'])
stripe.api_key = app.config['STRIPE_KEY']


@app.route(
    '/validate/',
    methods=['POST']
)
def validate():
    payload = request.get_json()
    username = payload['username']
    password = payload['password']
    role = payload['role']
    apikey = payload['apikey']
    method = payload['method']

    validate_api_key(apikey)
    validate_user(username, password, role, method)

    return '', 200


def validate_user(username, password, role, method):
    lookup = {
        'users.username': username,
        'users.password': password,
        'users.role': 'admin' if not role else role,
        '_deleted': False
    }
    if method in ('POST', 'PATCH', 'PUT', 'DELETE'):
        lookup['can_write'] = True

    user = db['customer'].find_one(lookup)
    if not user:
        abort(401, 'User unknown, or invalid credentials')

    validate_subscription(user['stripe']['subscription_id'])


def validate_api_key(key):
    if key is None:
        abort(400, 'API Key is missing')

    if not redis.get(key):
        user = db['customer'].find_one({'api_key': key})
        if not user:
            abort(401, 'API Key invalid or unknown')

    validate_subscription(user['stripe']['subscription_id'])


def validate_subscription(self, id):
    if not redis.get(id):
        sub = get_subscription(id)
        if sub['status'] in ('past_due', 'canceled', 'unpaid'):
            abort(403, 'Subscription is {}'.format(sub['status']))

        expiration = datetime.fromtimestamp(sub.current_period_end)
        redis.set(id, id, expiration-datetime.now())


def get_subscription(subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
    except stripe.error.InvalidRequestError as e:
        error = e.json_body['error']
        if 'id' in error['param'] and 'No such subscription' in \
                error['message']:
            abort(404, 'Subscription not found.')
        else:
            abort(400, str(e))

    return subscription


if __name__ == '__main__':
    app.run(host=host, port=port, ssl_context=context)
