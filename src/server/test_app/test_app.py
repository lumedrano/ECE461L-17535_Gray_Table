import unittest
from unittest.mock import patch
from flask import json
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True


    #test case works
    def test_add_user(self):
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

    #test case works
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

    

    #test works, does not have an assertion
    def test_get_user_projects_list(self):
        # Test case 1: Successful projects retrieval
        test_data = {
            'userId': 'test'
        }
        response = self.app.post('/get_user_projects_list', 
                               data=json.dumps(test_data), 
                               content_type='application/json')
        
        print(response.data)

    #test works, does not have assertion
    def test_leave_project(self):
        test_data = {
            'userId': 'test',
            'projectId': '001'
        }
        response = self.app.post('/leave_project', 
                               data=json.dumps(test_data), 
                               content_type='application/json')
        
        print(response.data)

if __name__ == '__main__':
    unittest.main()