from django.test import TestCase
from django.core.management import call_command
from vacations.models import Role
from vacations.services import add_role
from django.core.exceptions import ValidationError

class RoleServiceTest(TestCase):
    """
    Role CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_add_role_success(self) -> None:
        """Positive: Add role."""
        role: Role = add_role("moderator")
        self.assertIsNotNone(role)

    def test_add_role_duplicate(self) -> None:
        """Negative: Add duplicate role."""
        add_role("moderator")
        with self.assertRaises(ValidationError):
            add_role("moderator")
