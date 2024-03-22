import os
import pytest
from flask import Flask
from login import create_app  # Replace 'yourapp' with the name of your Flask app package
from login.auth import auth 
from flask_sqlalchemy import SQLAlchemy
from login import db





@pytest.fixture
def app():
    app = create_app()
    
    
   
   
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page(client):
    
    response = client.get('/login')
    assert response.status_code == 200
    

def test_login_functionality(client):
    
    response = client.post('/login', data=dict(
        email='lakshay@gmail.com', 
        password='12345678'
    ), follow_redirects=True)
    assert response.status_code == 200
    # Check for a success indicator, e.g., a flash message or redirect to a dashboard




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