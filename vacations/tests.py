from django.test import TestCase
from vacations.models import User, Role
from vacations.services import register_user, login_user

class UserServiceTest(TestCase):
    def setUp(self) -> None:
        Role.objects.create(name="user")

    def test_register_user_success(self) -> None:
        user = register_user("Test", "User", "test@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_register_user_existing_email(self) -> None:
        register_user("Test", "User", "test@example.com", "1234")
        with self.assertRaises(Exception):
            register_user("Test2", "User2", "test@example.com", "12345")

    def test_login_user_success(self) -> None:
        user = register_user("Login", "User", "login@example.com", "pass")
        authenticated_user = login_user("login@example.com", "pass")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(user.id, authenticated_user.id)

    def test_login_user_wrong_credentials(self) -> None:
        register_user("Login", "User", "login@example.com", "pass")
        self.assertIsNone(login_user("login@example.com", "wrong"))
