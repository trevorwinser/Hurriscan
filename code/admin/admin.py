from typing import List

from flask import Blueprint, request

from .response import build_response
from .users import User

admin_bp = Blueprint('admin', __name__)

users: list[User] = []

@admin_bp.route('/admin/users', methods=['GET'])
def get_users():
    response = {"users": [u.to_dict() for _, u in enumerate(users)]}
    return build_response(**response), 200

@admin_bp.route('/admin/users', methods=['POST'])
def create_user():
    r = request.get_json()
    user = User(r.get("username"), r.get("password"), r.get("email", "admin@gmail.com"))
    users.append(user)
    return build_response(**user.to_dict()), 201

@admin_bp.route('/admin/users/<username>', methods=['DELETE'])
def del_user_name(username: str):
    for i, user in enumerate(users):
        if user.user_name == username:
            users.pop(i)
            return "deleted", 204
    return "not found", 404

@admin_bp.route('/admin/users/<username>', methods=['PATCH'])
def edit_user_name(username: str):
    for i, user in enumerate(users):
        if user.user_name == username:
            r = request.get_json()
            if(user.password != r.get("oldPassword")):
                return "wrong password", 401
            user.user_name = r.get("newUsername")
            user.password = r.get("newPassword")
            return build_response(**user.to_dict()), 200
    return "not found", 404