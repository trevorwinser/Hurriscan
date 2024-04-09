import os
import pytest
from flask import Flask
from ..routing import create_app  # Replace 'yourapp' with the name of your Flask app package
from ..routing.auth import auth 
from flask_sqlalchemy import SQLAlchemy
from ..routing import user





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
    response = client.post('/login', data={'username': 'User1', 'password': 'wrong_password'})
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



def test_login_authorization(client):
    response = client.get('/', follow_redirects=False)
    
    # Check that the response is a redirect (status code 302)
    assert response.status_code == 302
    
    # Verify that the Location header is pointing to the login page.
    # This assumes your login page URL is something like '/login'
    assert '/login' in response.headers['Location']
    
    
    #Testing for an anonymous user accessing the admin page
    response = client.get('/admin', follow_redirects=False)
    
   
    assert response.status_code == 302

    assert '/login' in response.headers['Location']
    


#Testing that a user that is currently logged in but NOT an Admin gets redirected to the Home Page when try try to access localhost/admin
def test_admin_authorization(client):
    user.currentUsername = "User1"
    response = client.get('/admin', follow_redirects=False)
    user.currentUsername = ""
    
    assert response.status_code == 302
    
    assert '/' in response.headers['Location']
    

def test_correct_admin_authorization(client):
    user.currentUsername = "Admin1"
    user.isAdmin = True

    response = client.get('/admin', follow_redirects = False)
    
    user.currentUsername = ""
    user.isAdmin = False
    
    assert response.status_code == 200
