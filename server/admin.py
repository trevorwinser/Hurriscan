from flask import Blueprint, request, jsonify
import sqlite3

admin_bp = Blueprint('admin', __name__)

# Function to establish connection with SQLite database
def get_db_connection():
    conn = sqlite3.connect('hurriscan.db')
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/admin/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User;")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users), 200

@admin_bp.route('/admin/users', methods=['POST'])
def create_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    r = request.get_json()
    cursor.execute('''
        INSERT INTO User (username, password, email)
        VALUES (?, ?, ?)
    ''', (r.get("username"), r.get("password"), r.get("email", "admin@gmail.com")))
    conn.commit()
    conn.close()
    return "User created successfully", 201

@admin_bp.route('/admin/users/<username>', methods=['DELETE'])
def del_user_name(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE username = ?;", (username,))
    conn.commit()
    conn.close()
    return "User deleted successfully", 204

@admin_bp.route('/admin/users/<username>', methods=['PATCH'])
def edit_user_name(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    r = request.get_json()
    cursor.execute("SELECT * FROM User WHERE username = ?;", (username,))
    user = cursor.fetchone()
    if user:
        if user["password"] == r.get("oldPassword"):
            cursor.execute('''
                UPDATE User 
                SET username = ?, password = ?
                WHERE username = ?;
            ''', (r.get("newUsername"), r.get("newPassword"), username))
            conn.commit()
            conn.close()
            return "User updated successfully", 200
        else:
            conn.close()
            return "Wrong password", 401
    else:
        conn.close()
        return "User not found", 404
