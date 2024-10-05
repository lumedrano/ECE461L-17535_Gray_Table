import unittest
from unittest.mock import patch
from flask import json
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    def test_add_user(self):
        # Mock the database interaction

        # Define test data
        test_data = {
            'username': 'testuser',
            'userId': 'testuser123',
            'password': 'password123'
        }

        # Send POST request to /add_user
        response = self.app.post('/add_user', data=json.dumps(test_data), content_type='application/json')

        # Verify response data and status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User added successfully.')

    def test_login(self):
        # Define test data
        test_data = {
            'username': 'testuser',
            'userId': 'testuser123',
            'password': 'password123'
        }

        # Send POST request to /login
        response = self.app.post('/login', data=json.dumps(test_data), content_type='application/json')

        # Verify response data and status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Login Successful!')

if __name__ == '__main__':
    unittest.main()
