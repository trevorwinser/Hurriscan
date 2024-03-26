import os
import pytest
from flask import Flask
from routing import create_app  # Replace 'yourapp' with the name of your Flask app package
from routing.auth import auth 
from flask_sqlalchemy import SQLAlchemy





@pytest.fixture
def app():
    app = create_app()
    
    
   
   
    

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page(client):
    
    response = client.get('/login')
    assert response.status_code == 200
    

def test_login_functionality(client):
    
    response = client.post('/login', data=dict(
        username = 'lakshayd',
        password='12345678'
    ), follow_redirects=True)
    assert response.status_code == 200
    # Check for a success indicator, e.g., a flash message or redirect to a dashboard

    

def test_bad_login_incorrect_password(client):
    # Simulate incorrect password scenario
    response = client.post('/login', data={'username': 'lakshayd', 'password': 'wrong_password'})
    assert b'Incorrect Password, Try Again.' in response.data

def test_bad_login_invalid_username(client):
    # Simulate invalid username scenario
    response = client.post('/login', data={'username': 'nonexistent_user', 'password': 'any_password'})
    assert b'Invalid Username.' in response.data




def test_registration_functionality(client):
    response = client.post('/sign-up', data={
            'email': 'test@gmail.com',
            'password1': '12345678',
            'passsword2': '12345678',
            'firstName': 'test',
            'lastName' : 'McTest',
            'dob': '2024-01-01'
        }, follow_redirects=True)
    
    assert response.status_code == 200



'''

email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        dob = request.form.get('dob')'''