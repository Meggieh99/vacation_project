from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from vacations.models import User, Role, Country, Vacation
from datetime import date, timedelta
from django.core.management import call_command


class AdminVacationAPITest(TestCase):
    """
    Tests for admin vacation management: add, edit, delete.
    """

    def setUp(self) -> None:
        """
        Create admin user and sample country.
        """
        call_command('init_data')

        self.client = APIClient()
        self.admin_role: Role = Role.objects.get(name='admin')
        self.user_role: Role = Role.objects.get(name='user')

        self.admin: User = User.objects.filter(email="admin@example.com").first()
        self.client.force_authenticate(user=self.admin)

        self.country: Country = Country.objects.create(name="Greece")

        self.vacation: Vacation = Vacation.objects.create(
            country=self.country,
            description="Athens Trip",
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=6),
            price=1800,
            image_filename="athens.jpg"
        )

        self.add_url = reverse('vacation-add')
        self.edit_url = reverse('vacation-edit', kwargs={"vacation_id": self.vacation.id})
        self.delete_url = reverse('vacation-delete', kwargs={"vacation_id": self.vacation.id})

    def test_add_vacation_success(self) -> None:
        """
        Positive: admin adds a valid vacation.
        """
        data = {
            "country": self.country.id,
            "description": "Santorini",
            "start_date": date.today() + timedelta(days=10),
            "end_date": date.today() + timedelta(days=14),
            "price": 3000,
            "image_filename": "santorini.jpg"
        }
        response = self.client.post(self.add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vacation.objects.filter(description="Santorini").exists())
