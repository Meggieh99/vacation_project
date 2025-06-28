from django.test import TestCase
from vacations.models import User, Role, Like, Vacation, Country
from vacations.services import (
    register_user, login_user, add_like, remove_like,
    add_vacation, update_vacation, delete_vacation, get_all_vacations,
    add_country, get_all_countries, delete_country,
    add_role, get_all_roles
)
from django.core.management import call_command
from datetime import date, timedelta
from django.core.exceptions import ValidationError
import unittest

def setUpModule() -> None:
    """
    Applies migrations once at the beginning.
    """
    call_command('migrate')

def test_all() -> None:
    """
    Run all tests using unittest loader.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='tests.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class UserServiceTest(TestCase):
    """
    User registration and login tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_register_user_success(self) -> None:
        """Positive: Register new user."""
        user = register_user("Test", "User", "test@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    def test_register_user_existing_email(self) -> None:
        """Negative: Register user with existing email."""
        register_user("Test", "User", "test@example.com", "1234")
        with self.assertRaises(Exception):
            register_user("Test2", "User2", "test@example.com", "12345")

    def test_login_user_success(self) -> None:
        """Positive: Login user with correct credentials."""
        register_user("Login", "User", "login@example.com", "pass")
        user = login_user("login@example.com", "pass")
        self.assertIsNotNone(user)

    def test_login_user_wrong_credentials(self) -> None:
        """Negative: Login user with incorrect credentials."""
        register_user("Login", "User", "login@example.com", "pass")
        user = login_user("login@example.com", "wrong")
        self.assertIsNone(user)

class LikeServiceTest(TestCase):
    """
    Like/unlike functionality tests.
    """

    def setUp(self) -> None:
        call_command('init_data')
        self.user = User.objects.first()
        self.vacation = Vacation.objects.first()

    def test_add_like_success(self) -> None:
        """Positive: Add like."""
        like = add_like(self.user.id, self.vacation.id)
        self.assertIsNotNone(like)

    def test_add_like_duplicate(self) -> None:
        """Negative: Add duplicate like."""
        add_like(self.user.id, self.vacation.id)
        with self.assertRaises(Exception):
            add_like(self.user.id, self.vacation.id)

class VacationServiceTest(TestCase):
    """
    Vacation CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')
        self.country = Country.objects.first()
        Vacation.objects.all().delete()

    def test_add_vacation_success(self) -> None:
        """Positive: Add valid vacation."""
        vacation = add_vacation(
            self.country.id, "Test Vacation", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "test.jpg"
        )
        self.assertIsNotNone(vacation)

    def test_add_vacation_invalid_price(self) -> None:
        """Negative: Add vacation with invalid price."""
        with self.assertRaises(ValidationError):
            add_vacation(
                self.country.id, "Bad Vacation", date.today() + timedelta(days=1),
                date.today() + timedelta(days=10), -100, "bad.jpg"
            )

    def test_get_all_vacations(self) -> None:
        """Positive: Get all vacations."""
        add_vacation(
            self.country.id, "Vacation A", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "a.jpg"
        )
        vacations = get_all_vacations()
        self.assertEqual(len(vacations), 1)

class CountryServiceTest(TestCase):
    """
    Country CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_add_country_success(self) -> None:
        """Positive: Add country."""
        country = add_country("NewLand")
        self.assertIsNotNone(country)

    def test_add_country_duplicate(self) -> None:
        """Negative: Add duplicate country."""
        add_country("NewLand")
        with self.assertRaises(ValidationError):
            add_country("NewLand")

class RoleServiceTest(TestCase):
    """
    Role CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_add_role_success(self) -> None:
        """Positive: Add role."""
        role = add_role("moderator")
        self.assertIsNotNone(role)

    def test_add_role_duplicate(self) -> None:
        """Negative: Add duplicate role."""
        add_role("moderator")
        with self.assertRaises(ValidationError):
            add_role("moderator")
