from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from vacations.models import User, Role


class UserAPITest(TestCase):
    """
    Tests for user registration and login endpoints.
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')

        # Create roles safely
        self.admin_role, _ = Role.objects.get_or_create(name='admin')
        self.user_role, _ = Role.objects.get_or_create(name='user')

    def test_register_success(self) -> None:
        """
        Positive: register with valid data.
        """
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "1234"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_register_existing_email(self) -> None:
        """
        Negative: register with existing email.
        """
        User.objects.get_or_create(
            first_name="Old", last_name="User",
            email="existing@example.com", password="pass",
            role=self.user_role
        )
        data = {
            "first_name": "New",
            "last_name": "User",
            "email": "existing@example.com",
            "password": "1234"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self) -> None:
        """
        Positive: login with correct credentials.
        """
        User.objects.get_or_create(
            first_name="Login", last_name="User",
            email="login@example.com", password="1234",
            role=self.user_role
        )
        data = {"email": "login@example.com", "password": "1234"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user_id", response.data)

    def test_login_fail(self) -> None:
        """
        Negative: login with wrong password.
        """
        User.objects.get_or_create(
            first_name="Login", last_name="User",
            email="loginfail@example.com", password="1234",
            role=self.user_role
        )
        data = {"email": "loginfail@example.com", "password": "wrong"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
