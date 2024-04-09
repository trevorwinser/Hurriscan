import pytest
from flask import Flask
import json
from routing import create_app
from routing import user

@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()

def test_initial_data_route(client):
    user.currentUsername = "User1"
    response = client.get('/map-filter-data')
    user.currentUsername = ""
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  
    
    
def test_map_filter_data_route(client):
    user.currentUsername = "User1"
    response = client.get('/map-filter-data?month=12&year=89')
    user.currentUsername = ""
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  
    
def test_map_filter_temperature_route(client):
    user.currentUsername = "User1"
    response = client.get('/map-filter-data?minTemperature=20&maxTemperature=30')
    user.currentUsername = ""
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  