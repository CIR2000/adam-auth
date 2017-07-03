import os

from flask import Flask
from flask_sentinel import ResourceOwnerPasswordCredentials

port = os.environ.get('PORT')
if port:
    # Heroku
    host = '0.0.0.0'
    port = int(port)
else:
    host = '127.0.0.1'
    port = 8000

app = Flask(__name__)
app.config.from_object('settings')

if __name__ == '__main__':
    ResourceOwnerPasswordCredentials(app)
    app.run(ssl_context='adhoc', host=host, port=port)
