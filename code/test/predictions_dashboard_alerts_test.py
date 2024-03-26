import pytest
from app import app, send_alert

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predictions_dashboard_alerts(client):
    response = client.post ('/predictions-dashboard/alerts', data = dict(north_america = 'on'), follow_redirects=True)
    assert response.status_code == 200
