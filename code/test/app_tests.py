import unittest
import sqlite3
import requests

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect('hurriscan.db')

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

class TestFlaskApp(unittest.TestCase):
  
    BASE_URL = 'http://127.0.0.1:5000'

    def test_flask_running(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_data_visualization_page(self):
        response = requests.get(f'{self.BASE_URL}/data-visualization')
        self.assertEqual(response.status_code, 200)
       
        self.assertIn('visualization', response.text.lower())  

if __name__ == '__main__':
    unittest.main()
