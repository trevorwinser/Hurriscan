# test_admin_routes.py
from flask import Flask
import pytest
import json

# Import the Flask Blueprint and create an instance of the Flask app
from .admin import admin_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(admin_bp)
    with app.test_client() as client:
        yield client

def test_get_users(client):
    # Make a GET request to /admin/users
    response = client.get('/admin/users')
    assert response.status_code == 200

    # Ensure the response contains the expected data
    data = json.loads(response.data)
    assert 'users' in data
    assert isinstance(data['users'], list)

def test_create_user(client):
    # Make a POST request to /admin/users with JSON data
    new_user_data = {"username": "test_user", "password": "test_password", "email": "test@example.com"}
    response = client.post('/admin/users', json=new_user_data)
    assert response.status_code == 201

    # Ensure the response contains the newly created user's data
    data = json.loads(response.data)
    assert 'username' in data
    assert data['username'] == new_user_data['username']

def test_del_user_name(client):
    # Make a DELETE request to /admin/users/<username>
    username = "test_user"
    response = client.delete(f'/admin/users/{username}')
    assert response.status_code == 204

def test_edit_user_name(client):
    # Make a PATCH request to /admin/users/<username> with JSON data
    username = "test_user"
    edit_data = {"oldPassword": "test_password", "newUsername": "new_test_user", "newPassword": "new_test_password"}
    response = client.patch(f'/admin/users/{username}', json=edit_data)
    assert response.status_code == 200

    # Ensure the response contains the edited user's data
    data = json.loads(response.data)
    assert 'username' in data
    assert data['username'] == edit_data['newUsername']
