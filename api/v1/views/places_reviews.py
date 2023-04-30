#!/usr/bin/python3
'''New view for Review objects to handle all default RESTful API actions'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_place_reviews(place_id):
    '''Get all reviews of a place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    '''Get a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    '''Delete a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    '''Create a review object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    review_data = request.get_json()
    if not review_data.get('user_id'):
        abort(400, 'Missing user_id')
    user = storage.get(User, place.user_id)
    if not user:
        abort(404)
    if not user_data.get('text'):
        abort(400, 'Missing text')
    review = Review(**review_data)
    storage.new(review)
    storage.save()
    return (jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Update a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    review_data = request.get_json()
    for key, value in review_data.items():
        if key not in ('id', 'user_id', 'place_id', 'created_at', 'updated_at'):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
