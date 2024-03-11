from flask import request, jsonify


def build_response(**kwargs):
    accept_type = request.headers.get("accept", "application/json")
    if accept_type in ["application/json", "*/*"]:
        return jsonify(**kwargs)
