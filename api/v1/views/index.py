#!/usr/bin/python3
'''/status route for Flask web app'''
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

object_count = {
            'amenities': storage.count(Amenity),
            'cities': storage.count(City),
            'places': storage.count(Place),
            'reviews': storage.count(Review),
            'states': storage.count(State),
            'users': storage.count(User)
        }


@app_views.route('/status', strict_slashes=False)
def status():
    '''Return the server status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''Return the count of objects by type'''
    return jsonify(object_count)
