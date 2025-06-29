from django.test import TestCase
from django.core.management import call_command
from vacations.models import Vacation, Country
from vacations.services import add_vacation, get_all_vacations
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class VacationServiceTest(TestCase):
    """
    Vacation CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')
        self.country: Country = Country.objects.first()
        Vacation.objects.all().delete()

    def test_add_vacation_success(self) -> None:
        """Positive: Add valid vacation."""
        vacation: Vacation = add_vacation(
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
        vacations: list[Vacation] = get_all_vacations()
        self.assertEqual(len(vacations), 1)
