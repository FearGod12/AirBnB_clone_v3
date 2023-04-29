#!/usr/bin/python3
""" View for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_of_cities(city_id):
    """ Retrieves the list of all Places objects in a city"""
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            places = city.places
            return jsonify([place.to_dict() for place in places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a place object
    """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place():
    """ Creates a Place object """
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            new_place = request.get_json(silent=True)
            if not new_place:
                abort(400, "Not a JSON")
            if "user_id" not in new_place:
                abort(400, "Missing user_id")
            if storage.get('User', new_place['uer_id']) is None:
                abort(404)
            if 'name' not in new_place:
                abort(400, "Missing name")
            place = Place(**new_place)
            storage.new(place)
            storage.save()
            return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
