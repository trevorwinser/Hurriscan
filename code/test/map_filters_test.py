import pytest
from flask import Flask
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_initial_data_route(client):
    response = client.get('/initial-data')
    assert response.status_code == 200
    # Add more assertions to check the response data if needed

def test_map_filter_data_route(client):
    response = client.get('/map-filter-data?month=1&year=89')
    assert response.status_code == 200
    # Add more assertions to check the response data if needed

def test_map_filter_temperature_route(client):
    response = client.get('/map-filter-data?minTemperature=20&maxTemperature=30')
    assert response.status_code == 200
    # Add more assertions to check the response data if needed
