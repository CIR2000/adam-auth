from flask import Flask
from flask.ext.sentinel import ResourceOwnerPasswordCredentials

# still a WIP

app = Flask(__name__)
app.config.from_object('settings')

if __name__ == '__main__':
    ResourceOwnerPasswordCredentials(app)
    app.run(ssl_context='adhoc')
