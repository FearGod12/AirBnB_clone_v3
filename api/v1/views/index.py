#!/usr/bin/python3
""" Index file of the API V1."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON file with the status of the API"""
    return jsonify(status="OK")
