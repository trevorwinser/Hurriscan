import pytest
from flask import Flask
import json
#from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_initial_data_route(client):
    response = client.get('/map-filter-data')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  
    
def test_map_filter_data_route(client):
    response = client.get('/map-filter-data?month=12&year=89')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  
    
def test_map_filter_temperature_route(client):
    response = client.get('/map-filter-data?minTemperature=20&maxTemperature=30')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)  