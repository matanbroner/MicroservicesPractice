# services/users/project/tests/test_users.py

import json
import unittest

from project import db
from project.api.models import User
from utils import add_user

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the User Service"""

    def test_users(self):
        """Ensure the /ping route behaves correct"""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn("pong!", data["message"])
        self.assertIn("success", data["status"])

    def test_add_users(self):
        """Ensure a new user can be added to the database"""
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "matan", "email": "matanbroner@yahoo.com"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn("matanbroner@yahoo.com was added!", data["message"])
            self.assertIn("success", data["status"])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty"""
        with self.client:
            response = self.client.post(
                "/users", data=json.dumps({}), content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_invalid_json_keys(self):
        """ 
        Ensure an error is thrown if the JSON object does not have a username key
        """
        with self.client:
            response = self.client.post(
                "/users",
                data=json.dumps({"email": "matanbroner@gmail.com"}),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid payload.", data["message"])
            self.assertIn("fail", data["status"])

    def test_add_user_duplicate_name(self):
        """Ensure error is thrown if email already exists"""
        with self.client:
            self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "michael", "email": "matanbroner@gmail.com"}
                ),
                content_type="application/json",
            )
            response = self.client.post(
                "/users",
                data=json.dumps(
                    {"username": "michael", "email": "matanbroner@gmail.com"}
                ),
                content_type="application/json",
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn("Sorry. That email already exists.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user(self):
        """Ensure get single users behaves correctly"""
        user = add_user("matan", "matanbroner@gmail.com")
        with self.client:
            response = self.client.get(f"/users/{user.id}")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("matan", data["data"]["username"])
            self.assertIn("matanbroner@gmail.com", data["data"]["email"])
            self.assertIn("success", data["status"])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist.", data["message"])
            self.assertIn("fail", data["status"])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = self.client.get("/users/999")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn("User does not exist.", data["message"])
            self.assertIn("fail", data["status"])

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        add_user("john", "johnsmith@gmail.com")
        add_user("henry", "henrysmith@yahoo.com")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertIn("john", data["data"]["users"][0]["username"])
            self.assertIn("johnsmith@gmail.com", data["data"]["users"][0]["email"])
            self.assertIn("henry", data["data"]["users"][1]["username"])
            self.assertIn("henrysmith@yahoo.com", data["data"]["users"][1]["email"])
            self.assertIn("success", data["status"])

    def test_main_no_users(self):
        """Ensure the main route behaves when no users are added to the DB"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when the users
        are added to the DB"""
        add_user("john", "johnsmith@gmail.com")
        add_user("henry", "henrysmith@yahoo.com")
        with self.client:
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"john", response.data)
            self.assertIn(b"henry", response.data)

    def test_add_main_user(self):
        """
            Ensure a new user can be added to DB via our form
        """
        with self.client:
            response = self.client.post(
                "/",
                data=dict(username="michael", email="michael@gmail.com"),
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"michael", response.data)


if __name__ == "__main__":
    unittest.main()
