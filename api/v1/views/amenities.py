#!/usr/bin/python3
"""Handles all default RESTFul API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects or creates a new Amenity"""
    if request.method == 'GET':
        amenities = storage.all(Amenity).values()
        return jsonify([amenity.to_dict() for amenity in amenities])

    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if data.get('name') is None:
            return jsonify({"error": "Missing name"}), 400
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_with_id(amenity_id):
    """Retrieves, deletes, or updates a Amenity object"""
    amenity_by_id = storage.get(Amenity, amenity_id)
    if amenity_by_id is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity_by_id.to_dict())

    elif request.method == 'DELETE':
        storage.delete(amenity_by_id)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity_by_id, key, value)
        amenity_by_id.save()
        return jsonify(amenity_by_id.to_dict()), 200
