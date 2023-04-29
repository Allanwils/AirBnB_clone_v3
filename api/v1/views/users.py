#!/usr/bin/python3
'''New view for User objects to handle all default RESTful API actions'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    '''Get all users'''
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    '''Get a user with id user_id'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Delete a user with id user_id'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Create a user object with id '''
    if not request.is_json:
        abort(400, 'Not a JSON')
    user_data = request.get_json()
    if not user_data.get('email'):
        abort(400, 'Missing email')
    if not user_data.get('password'):
        abort(400, 'Missing password')
    user = User(**user_data)
    storage.new(user)
    storage.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Update a user'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    user_data = request.get_json()
    for key, value in user_data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
