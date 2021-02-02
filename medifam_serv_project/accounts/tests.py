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

    def _assert_400_request(self, data, msg=""):
        response = self.client.post(self.create_url, data, format="json")

        # Assert that we received an 400 status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=msg)
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
        self._assert_400_request(short_user_pass_data, "password too short")

    def test_password_provided(self):
        """
        Description:
        -----------
        Always must provide a password.
        """
        no_pass_user = {
            "username": "foo",
            "email": "email@example.com",
            "password": "",
        }
        self._assert_400_request(no_pass_user, "Must require password")

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
        self._assert_400_request(
            alpha_only,
            "Must fail to create an user with letters only password.",
        )

        # Test with a numeric only password
        num_only = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "12345678..",
        }
        self._assert_400_request(
            num_only,
            "Must fail to create an user with numeric only password.",
        )

        # Test with no UpperCase
        no_upper = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "noupper123..",
        }
        self._assert_400_request(
            no_upper,
            "Must fail to create an user with no upper case password.",
        )

        # Test no non-alphanumeric

        no_nonalpha = {
            "username": "foo",
            "email": "foo@example.com",
            "password": "Noupper123",
        }
        self._assert_400_request(
            no_nonalpha,
            "Must fail to create an user with alphanumeric only password.",
        )

    # TESTS FOR USER SANITY
    def test_user_provided(self):
        """
        Description:
        -----------
        Username must be provided.
        """
        no_username = {
            "username": "",
            "email": "foo@example.com",
            "password": "Complex*&.123",
        }
        self._assert_400_request(no_username, "Must fail username null creation.")

    def test_username_exists(self):
        """
        Description:
        -----------
        Username uniquelly identifies an user, so it must be unique
        in the DB.
        """
        existent_user = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "MyComplexPass123&.ss",
        }
        self._assert_400_request(existent_user, "Must fail if user exists.")

    # TEST FOR EMAIL SANITY
    def test_email_exists(self):
        """
        Description:
        -----------
        An email also uniquelly identifies an user, this must be unique across
        the db.
        """
        existent_email_user = {
            "username": "foo",
            "email": "test@example.com",
            "password": "MyComplexPass123&.ss",
        }
        self._assert_400_request(existent_email_user, "Must fail if email exists.")

    def test_email_valid(self):
        """
        Description:
        -----------
        Validates that email is well-formed.
        """
        invalid_email = {
            "username": "foo",
            "email": "testing",
            "password": "MyComplexPass123&.ss",
        }
        self._assert_400_request(
            invalid_email,
            "Email must conforms to '<account>@<server>'",
        )

    def test_emails_provided(self):
        """
        Description:
        ------------
        Email is a required field.
        """
        invalid_email = {
            "username": "foo",
            "email": "",
            "password": "MyComplexPass123&.ss",
        }
        self._assert_400_request(invalid_email, "Fail if email is not provided.")

    def test_login_user(self):
        "Make sure we can login an existing user"
        pass
