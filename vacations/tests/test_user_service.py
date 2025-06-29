from django.test import TestCase
from django.core.management import call_command
from vacations.models import User
from vacations.services import register_user, login_user
from django.core.exceptions import ValidationError

class UserServiceTest(TestCase):
    """
    User registration and login tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_register_user_success(self) -> None:
        """Positive: Register new user."""
        user: User = register_user("Test", "User", "test@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_register_user_existing_email(self) -> None:
        """Negative: Register user with existing email."""
        register_user("Test", "User", "test@example.com", "1234")
        with self.assertRaises(ValidationError):
            register_user("Test2", "User2", "test@example.com", "12345")

    def test_login_user_success(self) -> None:
        """Positive: Login user with correct credentials."""
        register_user("Login", "User", "login@example.com", "pass")
        user: User | None = login_user("login@example.com", "pass")
        self.assertIsNotNone(user)

    def test_login_user_wrong_credentials(self) -> None:
        """Negative: Login user with incorrect credentials."""
        register_user("Login", "User", "login@example.com", "pass")
        user: User | None = login_user("login@example.com", "wrong")
        self.assertIsNone(user)
