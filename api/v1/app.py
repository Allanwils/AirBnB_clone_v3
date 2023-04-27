#!/usr/bin/python3
'''Start a Flask web app
'''
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception=None):
    '''Close storage on teardown
    '''
    storage.close()


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST')
    port = os.environ.get('HBNB_API_PORT')
    if host and port:
        app.run(host=host, port=port)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
