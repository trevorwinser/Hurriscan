from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load initial data from JSON file
with open('users.json', 'r') as file:
    users = json.load(file)

@app.route('/admin/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/admin/users', methods=['POST'])
def create_user():
    data = request.get_json()
    users.append(data)
    update_json_file(users)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/admin/users/<username>', methods=['DELETE'])
def delete_user(username):
    for user in users:
        if user.get('username') == username:  # Assuming 'username' is the key for the username in user data
            users.remove(user)
            update_json_file(users)
            return jsonify({"message": f"Deleted user: {username}"}), 204
    return jsonify({"message": "User not found"}), 404

def update_json_file(data):
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    print("Current users:")
    print(users)  # This will print the current content of the users list
    app.run(debug=True)
