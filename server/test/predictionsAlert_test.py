import unittest
from flask_testing import TestCase
from flask import Flask, jsonify
from server import predictions 

class TestSendAlert(TestCase):
    def create_app(self):
        predictions.config['TESTING'] = True
        return predictions
    
    def test_send_alert(self):
        with app.test_client() as client:
            response = client.post('/predictions-dashboard/send-text-alert', json={
                'humidity': '78.44519694524953',
                'temperature': '29.045276650193742',
                'airPressure': '28.028054617682667',
                'risk': 'High'
            })
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['message'], 'Alert sent')

if __name__ == '__main__':
    unittest.main()