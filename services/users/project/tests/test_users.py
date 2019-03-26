# services/users/project/tests/test_users.py

import json
import unittest

from project import db
from project.api.models import User

from project.tests.base import BaseTestCase

class TestUserService(BaseTestCase):
    """Tests for the User Service"""

    def test_users(self):
        """Ensure the /ping route behaves correct"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_users(self):
        """Ensure a new user can be added to the database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'matan',
                    'email': 'matanbroner@yahoo.com'
                }),
                content_type='application/json',
            )
            data= json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('matanbroner@yahoo.com was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                '/users',
                data = json.dumps({}),
                content_type = 'application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    
    def test_add_user_invalid_json_keys(self):
        """ 
        Ensure an error is thrown if the JSON object does not have a username key
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'matanbroner@gmail.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_name(self):
        """Ensure error is thrown if email already exists"""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'matanbroner@gmail.com'
                    }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'matanbroner@gmail.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single users behaves correctly"""
        user = User(username='matan', email='matanbroner@gmail.com')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('matan', data['data']['username'])
            self.assertIn('matanbroner@gmail.com', data['data']['email'])
            self.assertIn('success', data['status'])

if __name__ == '__main__':
    unittest.main()