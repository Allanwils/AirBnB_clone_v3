#!/usr/bin/python3
'''New view for City objects to handle all default RESTful API actions'''
from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    states = storage.all(State).values()
    state_ids = []
    for state in states:
        state_ids.append(state.id)
    if state_id not in state_ids:
        abort(404)
    cities = storage.all(City).values()
    return jsonify([city.to_dict() for city in cities if city.state_id == state_id])

