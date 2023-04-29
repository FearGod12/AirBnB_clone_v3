#!/usr/bin/python3
'''view for City objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from flask import jsonify, Flask, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_cities(state_id):
    '''return all cities linked to a state when method is GET
    creates a new city when method is POST'''
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)

    cities = state_by_id.cities
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in cities])

    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None or type(data) != dict:
            return jsonify({"error": "Not a JSON"}), 400
        if data.get('name') is None:
            return jsonify({"error": "Missing name"}), 400
        data["state_id"] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_with_id(city_id):
    '''returns the city with the specified id when method is GET
    deletes the city with speicified id when method is delete
    and updates the city with the specified id when method is PUT'''
    city_by_id = storage.get(City, city_id)
    if city_by_id is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city_by_id.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city_by_id)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city_by_id, key, value)
        city_by_id.save()
        return jsonify(city_by_id.to_dict()), 200
