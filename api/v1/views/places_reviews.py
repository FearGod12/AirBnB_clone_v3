#!/usr/bin/python3
""" View for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_places(place_id):
    """ Retrieves the list of all reviews objects in place"""
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            reviews = place.reviews
            return jsonify([review.to_dict() for review in reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a review object for a place"""
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            new_review = request.get_json(silent=True)
            if not new_review:
                abort(400, "Not a JSON")
            if "user_id" not in new_review:
                abort(400, "Missing user_id")
            if storage.get(User, new_review['user_id']) is None:
                abort(404)
            if 'text' not in new_review:
                abort(400, "Missing text")
            new_review["place_id"] = place_id
            review = Review(**new_review)
            storage.new(review)
            storage.save()
            return jsonify(review.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a recview object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
