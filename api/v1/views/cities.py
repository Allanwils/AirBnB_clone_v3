#!/usr/bin/python3
'''New view for City objects to handle all default RESTful API actions'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    '''Get cities by state'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    '''Get a city with id city_id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''Delete a city'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''Create a city'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    city_data = request.get_json()
    if not city_data.get('name'):
        abort(400, 'Missing name')
    city = City(**city_data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Update a city'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    city_data = request.get_json()
    for key, value in city_data.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
