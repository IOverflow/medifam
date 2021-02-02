from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
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

    def _assert_400_request(self, data):
        response = self.client.post(self.create_url, data, format="json")

        # Assert that we received an 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that no user was created
        self.assertEqual(User.objects.count(), 1)

    def test_create_user(self):
        """
        Description:
        -----------
        Make sure we can create a new user and a valid token is created with it.
        """
        user_data = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "*7&12.<>$passAcc",
        }

        response = self.client.post(self.create_url, user_data, format="json")

        # Make sure we create the user
        self.assertEqual(User.objects.count(), 2)

        # Assert that we received a status code 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Uppon creation we want to receive the username and email
        # NOT THE PASSWORD
        self.assertEqual(response.data["username"], user_data["username"])
        self.assertEqual(response.data["email"], user_data["email"])
        self.assertFalse("*7&12.<>$passAcc" in response.data)

    # Test for password sanity
    def test_long_password(self):
        """
        Description:
        -----------
        Test that passwords cannot contain less than 8 characters.
        """
        short_user_pass_data = {
            "username": "foo",
            "email": "email@example.com",
            "password": "pass",
        }

        response = self.client.post(
            self.create_url,
            short_user_pass_data,
            format="json",
        )

        # Test that we received status code 411 (Short)
        self.assertEqual(response.status_code, status.HTTP_411_LENGTH_REQUIRED)
        self.assertEqual(User.objects.all(), 1)

    def test_password_complexity(self):
        """
        Description:
        -----------
        Password must contain at least:
        - A numeric character
        - A non-alphanumeric character
        - An UpperCase letter
        """
        alpha_only = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "Alphaonly",
        }
        self._assert_400_request(alpha_only)

        # Test with a numeric only password
        num_only = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "12345678..",
        }
        self._assert_400_request(num_only)

        # Test with no UpperCase
        no_upper = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "noupper123..",
        }
        self._assert_400_request(no_upper)

        # Test no non-alphanumeric

        no_nonalpha = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "Noupper123",
        }
        self._assert_400_request(no_nonalpha)

    def test_login_user(self):
        "Make sure we can login an existing user"
        pass
