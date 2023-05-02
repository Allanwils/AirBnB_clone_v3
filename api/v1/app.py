#!/usr/bin/python3
'''Start a Flask web app
'''
import os
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Create CORS instance
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(exception=None):
    '''Close storage on teardown'''
    return jsonify({'error': 'Not found'})
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''Return a 404 status code response'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST')
    port = os.environ.get('HBNB_API_PORT')
    if host and port:
        app.run(host=host, port=port, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
