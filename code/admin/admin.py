from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

users = []

@admin_bp.route('/admin/users', methods=['GET'])
def get_users():
    return users, 200

@admin_bp.route('/admin/users', methods=['POST'])
def create_user():
    users.append(f"User {len(users) + 1}")
    return "created", 201

@admin_bp.route('/admin/users/<name>', methods=['POST'])
def create_user_name(name: str):
    users.append(f"User {name}")
    return "created", 201

@admin_bp.route('/admin/users', methods=['DELETE'])
def del_user():
    users.pop()
    return "deleted", 204

@admin_bp.route('/admin/users/<key>', methods=['DELETE'])
def del_user_index(key: str):
    users.pop(int(key))
    return "deleted", 204
