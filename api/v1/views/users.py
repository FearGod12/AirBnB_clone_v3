#!/usr/bin/python3
"""Handles all default RESTFul API actions for User objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects or creates a new User"""
    if request.method == 'GET':
        users = storage.all(User).values()
        return jsonify([user.to_dict() for user in users])

    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'email' not in data:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in data:
            return jsonify({"error": "Missing password"}), 400
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_with_id(user_id):
    """Retrieves, deletes, or updates a User object"""
    user_by_id = storage.get(User, user_id)
    if user_by_id is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user_by_id.to_dict())

    elif request.method == 'DELETE':
        storage.delete(user_by_id)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user_by_id, key, value)
        user_by_id.save()
        return jsonify(user_by_id.to_dict()), 200
