#!/usr/bin/python3
""" View for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


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
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object """
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            new_place = request.get_json(silent=True)
            if not new_place:
                abort(400, "Not a JSON")
            if "user_id" not in new_place:
                abort(400, "Missing user_id")
            if storage.get(User, new_place['user_id']) is None:
                abort(404)
            if 'name' not in new_place:
                abort(400, "Missing name")
            new_place["city_id"] = city_id
            place = Place(**new_place)
            storage.new(place)
            storage.save()
            return jsonify(place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """ Searches for Place objects based on request body """
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    # Get lists of states, cities, and amenities from request data
    states = request_data.get("states", [])
    cities = request_data.get("cities", [])
    amenities = request_data.get("amenities", [])

    # Get all places if no search criteria provided
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Get places based on states and cities
    state_ids = set()
    city_ids = set(cities)
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            state_ids.add(state.id)
            for city in state.cities:
                city_ids.add(city.id)

    places = []
    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                if place not in places:
                    places.append(place)

    # Get places based on amenities
    if amenities:
        places_with_amenities = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if set(amenities).issubset(set(place_amenities)):
                places_with_amenities.append(place)
        places = places_with_amenities

    return jsonify([place.to_dict() for place in places])


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """ Searches for Place objects based on request body """
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    # Get lists of states, cities, and amenities from request data
    states = request_data.get("states", [])
    cities = request_data.get("cities", [])
    amenities = request_data.get("amenities", [])

    # Get all places if no search criteria provided
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Get places based on states and cities
    state_ids = set()
    city_ids = set(cities)
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            state_ids.add(state.id)
            for city in state.cities:
                city_ids.add(city.id)

    places = []
    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city:
            for place in city.places:
                if place not in places:
                    places.append(place)

    # Get places based on amenities
    if amenities:
        places_with_amenities = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if set(amenities).issubset(set(place_amenities)):
                places_with_amenities.append(place)
        places = places_with_amenities

    return jsonify([place.to_dict() for place in places])
