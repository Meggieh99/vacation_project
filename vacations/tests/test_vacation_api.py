from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from vacations.models import User, Role, Country, Vacation


class VacationAPITest(TestCase):
    """
    Tests for public vacation API.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.role_user, _ = Role.objects.get_or_create(name='user')
        self.user = User.objects.get_or_create(
            first_name="Guest", last_name="User",
            email="guest@example.com", password="1234",
            role=self.role_user
        )
        self.client.force_authenticate(user=self.user)

        self.country, _ = Country.objects.get_or_create(name="Italy")

    def test_get_vacations_success(self) -> None:
        """
        Positive: get all vacations successfully.
        """
        Vacation.objects.create(
            description="Ancient city.",
            price=1200,
            start_date="2025-08-01",
            end_date="2025-08-10",
            country=self.country,
        )
        url = reverse("vacation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_vacation_like_count_and_status(self) -> None:
        """
        Positive: response includes like_count and liked_by_user.
        """
        vacation = Vacation.objects.create(
            description="Water city.",
            price=1300,
            start_date="2025-09-01",
            end_date="2025-09-10",
            country=self.country,
        )
        url = reverse("vacation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("like_count", response.data[0])
        self.assertIn("liked_by_user", response.data[0])
