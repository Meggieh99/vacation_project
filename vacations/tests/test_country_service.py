from django.test import TestCase
from django.core.management import call_command
from vacations.models import Country
from vacations.services import add_country
from django.core.exceptions import ValidationError

class CountryServiceTest(TestCase):
    """
    Country CRUD tests.
    """

    def setUp(self) -> None:
        call_command('init_data')

    def test_add_country_success(self) -> None:
        """Positive: Add country."""
        country: Country = add_country("NewLand")
        self.assertIsNotNone(country)

    def test_add_country_duplicate(self) -> None:
        """Negative: Add duplicate country."""
        add_country("NewLand")
        with self.assertRaises(ValidationError):
            add_country("NewLand")
