#!/usr/bin/python3
'''/status route for Flask web app'''
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    '''Return the server status'''
    return jsonify({'status': 'OK'})
