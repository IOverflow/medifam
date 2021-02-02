from django.contrib.auth.models import User
from django.urls.base import reverse
from rest_framework import response, status
from rest_framework.test import APITestCase


class AccountTest(APITestCase):
    def setUp(self) -> None:
        # Originally create an user
        self.test_user = User.objects.create_user(
            "testuser",
            "test@example.com",
            "password",
        )

        # URL for registering a new user
        self.create_url = reverse("account-create")

    def test_create_user(self):
        "Make sure we can create a new user and a valid token is created with it"
        user_data = {"username": "foo", "email": "foo@example.com", "password": "pass"}

        response = self.client.post(self.create_url, user_data, format="json")

        # Make sure we create the user
        self.assertEqual(User.objects.count(), 2)

        # Assert that we received a status code 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Uppon creation we want to receive the username and email
        # NOT THE PASSWORD
        self.assertEqual(response.data["username"], user_data["username"])
        self.assertEqual(response.data["email"], user_data["email"])
        self.assertFalse("password" in response.data)
