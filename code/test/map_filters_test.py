import pytest
from flask import Flask
import json

app = Flask(__name__)

@pytest.fixture
def client():
    app.config['TESTINGG'] = True
    with app.test_client() as client:
        yield client

def test_initial_data_route(client):
    response = client.get('/initial-data')
    assert response.status_code == 200

def test_map_filter_data_route(client):
    response = client.get('/map-filter-data?month=1&year=89')
    assert response.status_code == 200

def test_map_filter_temperature_route(client):
    response = client.get('/map-filter-data?minTemperature=20&maxTemperature=30')
    assert response.status_code == 200
