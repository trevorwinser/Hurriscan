from flask import Flask
import pytest
import json

from admin import admin_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(admin_bp)
    with app.test_client() as client:
        yield client

def test_get_users(client):
    response = client.get('/admin/users')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'users' in data
    assert isinstance(data['users'], list)

def test_create_user(client):
    new_user_data = {"username": "test_user", "password": "test_password", "email": "test@example.com"}
    response = client.post('/admin/users', json=new_user_data)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert 'username' in data
    assert data['username'] == new_user_data['username']

def test_del_user_name(client):
    username = "test_user"
    response = client.delete(f'/admin/users/{username}')
    assert response.status_code == 204

def test_edit_user_name(client):
    username = "test_user"
    edit_data = {"oldPassword": "test_password", "newUsername": "new_test_user", "newPassword": "new_test_password"}
    response = client.patch(f'/admin/users/{username}', json=edit_data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'username' in data
    assert data['username'] == edit_data['newUsername']
