import os

from flask import Flask
from flask_sentinel import ResourceOwnerPasswordCredentials

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
ResourceOwnerPasswordCredentials(app)

if __name__ == '__main__':
    app.run(host=host, port=port, ssl_context=context)
