#!/usr/bin/python3
'''view for State objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from flask import jsonify, Flask, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    '''return all states when method is GET
    creates a new state when method is POST'''
    if request.method == 'GET':
        all_states = storage.all('State').values()
        return jsonify([state.to_dict() for state in all_states])
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        if data.get('name') is None:
            return jsonify({"error": "Missing name"}), 400
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_with_id(state_id):
    '''returns the state with the specified id when method is GET
    deletes the state with speicified id when method is delete
    and updates the state with the specified id when ethod is PUT'''
    state_by_id = storage.get(State, state_id)
    if state_by_id is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state_by_id.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state_by_id)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state_by_id, key, value)
        state_by_id.save()
        return jsonify(state_by_id.to_dict()), 200
