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
    Runs once before any tests. Applies migrations and loads initial data.
    """
    call_command('migrate')
    call_command('init_data')


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
        Role.objects.get_or_create(name="user")

    # Positive test: Register a new user
    def test_register_user_success(self) -> None:
        user = register_user("Test", "User", "test@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@example.com")

    # Negative test: Register user with existing email
    def test_register_user_existing_email(self) -> None:
        register_user("Test", "User", "test@example.com", "1234")
        with self.assertRaises(Exception):
            register_user("Test2", "User2", "test@example.com", "12345")

    # Positive test: Login with correct credentials
    def test_login_user_success(self) -> None:
        user = register_user("Login", "User", "login@example.com", "pass")
        authenticated_user = login_user("login@example.com", "pass")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(user.id, authenticated_user.id)

    # Negative test: Login with wrong password
    def test_login_user_wrong_credentials(self) -> None:
        register_user("Login", "User", "login@example.com", "pass")
        self.assertIsNone(login_user("login@example.com", "wrong"))


class LikeServiceTest(TestCase):
    """
    Like/unlike functionality tests.
    """

    def setUp(self) -> None:
        self.role = Role.objects.get_or_create(name="user")[0]
        self.user = User.objects.create(
            first_name="Like", last_name="Tester",
            email="like@example.com", password="1234",
            role=self.role
        )
        country = Country.objects.create(name="Testland")
        self.vacation = Vacation.objects.create(
            country=country,
            description="Test vacation",
            start_date="2025-01-01",
            end_date="2025-01-10",
            price=2000,
            image_filename="test.jpg"
        )

    # Positive test: Add like
    def test_add_like_success(self) -> None:
        like = add_like(self.user.id, self.vacation.id)
        self.assertIsNotNone(like)

    # Negative test: Add like twice
    def test_add_like_duplicate(self) -> None:
        add_like(self.user.id, self.vacation.id)
        with self.assertRaises(Exception):
            add_like(self.user.id, self.vacation.id)

    # Positive test: Remove existing like
    def test_remove_like_success(self) -> None:
        add_like(self.user.id, self.vacation.id)
        remove_like(self.user.id, self.vacation.id)
        self.assertFalse(Like.objects.filter(user=self.user, vacation=self.vacation).exists())

    # Negative test: Remove non-existing like (should not fail)
    def test_remove_like_nonexistent(self) -> None:
        remove_like(self.user.id, self.vacation.id)
        self.assertTrue(True)


class VacationServiceTest(TestCase):
    """
    Vacation CRUD tests.
    """

    def setUp(self) -> None:
        self.country = Country.objects.create(name="TestCountry")

    # Positive test: Add valid vacation
    def test_add_vacation_success(self) -> None:
        vacation = add_vacation(
            self.country.id, "Test Vacation", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "test.jpg"
        )
        self.assertIsNotNone(vacation)

    # Negative test: Add vacation with invalid price
    def test_add_vacation_invalid_price(self) -> None:
        with self.assertRaises(ValidationError):
            add_vacation(
                self.country.id, "Bad Vacation", date.today() + timedelta(days=1),
                date.today() + timedelta(days=10), -100, "bad.jpg"
            )

    # Negative test: Add vacation with end date before start date
    def test_add_vacation_invalid_dates(self) -> None:
        with self.assertRaises(ValidationError):
            add_vacation(
                self.country.id, "Bad Vacation", date.today() + timedelta(days=10),
                date.today() + timedelta(days=1), 1000, "bad.jpg"
            )

    # Positive test: Update vacation successfully
    def test_update_vacation_success(self) -> None:
        vacation = add_vacation(
            self.country.id, "Test Vacation", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "test.jpg"
        )
        updated = update_vacation(
            vacation.id, "Updated Vacation", date.today() + timedelta(days=2),
            date.today() + timedelta(days=12), 6000
        )
        self.assertEqual(updated.description, "Updated Vacation")

    # Negative test: Update vacation with invalid price
    def test_update_vacation_invalid_price(self) -> None:
        vacation = add_vacation(
            self.country.id, "Test Vacation", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "test.jpg"
        )
        with self.assertRaises(ValidationError):
            update_vacation(
                vacation.id, "Test Vacation", date.today() + timedelta(days=1),
                date.today() + timedelta(days=10), 15000
            )

    # Positive test: Delete vacation
    def test_delete_vacation_success(self) -> None:
        vacation = add_vacation(
            self.country.id, "Test Vacation", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "test.jpg"
        )
        delete_vacation(vacation.id)
        self.assertFalse(Vacation.objects.filter(id=vacation.id).exists())

    # Positive test: Get all vacations
    def test_get_all_vacations(self) -> None:
        add_vacation(
            self.country.id, "Vacation A", date.today() + timedelta(days=1),
            date.today() + timedelta(days=10), 5000, "a.jpg"
        )
        add_vacation(
            self.country.id, "Vacation B", date.today() + timedelta(days=2),
            date.today() + timedelta(days=11), 6000, "b.jpg"
        )
        vacations = get_all_vacations()
        self.assertEqual(len(vacations), 2)
        self.assertLessEqual(vacations[0].start_date, vacations[1].start_date)


class CountryServiceTest(TestCase):
    """
    Country CRUD tests.
    """

    # Positive test: Add country
    def test_add_country_success(self) -> None:
        country = add_country("NewLand")
        self.assertIsNotNone(country)
        self.assertEqual(country.name, "NewLand")

    # Negative test: Add duplicate country
    def test_add_country_duplicate(self) -> None:
        add_country("NewLand")
        with self.assertRaises(ValidationError):
            add_country("NewLand")

    # Positive test: Delete country
    def test_delete_country_success(self) -> None:
        country = add_country("ToDelete")
        delete_country(country.id)
        self.assertFalse(Country.objects.filter(id=country.id).exists())

    # Positive test: Get all countries
    def test_get_all_countries(self) -> None:
        add_country("A")
        add_country("B")
        countries = get_all_countries()
        self.assertGreaterEqual(len(countries), 2)


class RoleServiceTest(TestCase):
    """
    Role CRUD tests.
    """

    # Positive test: Add role
    def test_add_role_success(self) -> None:
        role = add_role("moderator")
        self.assertIsNotNone(role)
        self.assertEqual(role.name, "moderator")

    # Negative test: Add duplicate role
    def test_add_role_duplicate(self) -> None:
        add_role("moderator")
        with self.assertRaises(ValidationError):
            add_role("moderator")

    # Positive test: Get all roles
    def test_get_all_roles(self) -> None:
        add_role("r1")
        add_role("r2")
        roles = get_all_roles()
        self.assertGreaterEqual(len(roles), 2)
