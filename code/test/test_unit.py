""" import pytest
from code.app import app, db  # Import the app directly


@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    # Set up the test database if necessary
    with app.app_context():
        db.create_all()

    yield app.test_client()  # this provides the test client for the test functions

    # Teardown the database if necessary
    with app.app_context():
        db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Home Page' in response.data
 """