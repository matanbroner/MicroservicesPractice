# services/users/project/tests/test_user_model.py

import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from utils import add_user

from sqlalchemy.exc import IntegrityError

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user("justatest", "test@test.com", "pass1")
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.active)
        self.assertTrue(user.password)

    def test_add_user_duplicate_username(self):
        user = add_user("justatest", "test@test.com", "pass1")
        duplicate_user = User(
            username='justatest',
            email='test2@test.com',
            password='pass1'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user("justatest", "test@test.com", "pass1")
        duplicate_user = User(
            username='justatest2',
            email='test@test.com',
            password='pass1'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_to_json(self):
        user = add_user("justatest", "test@test.com", "pass1")
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user("john", "john@test.com", "pass1")
        user_two = add_user("mark", "mark@test.com", "pass3")
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'pass1')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
    
    def test_decode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'pass1')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(user.decode_auth_token(auth_token), user.id)

if __name__ == '__main__':
    unittest.main()

