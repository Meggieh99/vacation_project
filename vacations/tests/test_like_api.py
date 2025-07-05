from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from vacations.models import User, Role, Country, Vacation, Like
from django.core.management import call_command
from datetime import date, timedelta


class LikeAPITest(TestCase):
    """
    Tests for liking and unliking vacations by users.
    """

    def setUp(self) -> None:
        """
        Create test user, country, vacation, and log in the user.
        """
        call_command('init_data')
        self.client = APIClient()

        self.user: User = User.objects.get(email="Dan@example.com")
        self.country: Country = Country.objects.get(name="Israel")
        self.vacation: Vacation = Vacation.objects.create(
            country=self.country,
            description="Barcelona Vacation",
            start_date=date.today() + timedelta(days=3),
            end_date=date.today() + timedelta(days=10),
            price=3000,
            image_filename="barcelona.jpg"
        )

        self.client.force_authenticate(user=self.user)

    def test_like_success(self) -> None:
        """
        Positive: like a vacation.
        """
        url = reverse("vacation-like", args=[self.vacation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Like.objects.filter(user=self.user, vacation=self.vacation).exists())

    def test_like_twice_should_fail(self) -> None:
        """
        Negative: cannot like the same vacation twice.
        """
        Like.objects.create(user=self.user, vacation=self.vacation)
        url = reverse("vacation-like", args=[self.vacation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unlike_success(self) -> None:
        """
        Positive: unlike a vacation after liking it.
        """
        Like.objects.create(user=self.user, vacation=self.vacation)
        url = reverse("vacation-unlike", args=[self.vacation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, vacation=self.vacation).exists())

    def test_unlike_non_liked_vacation(self) -> None:
        """
        Negative: unlike a vacation that was not liked.
        """
        url = reverse("vacation-unlike", args=[self.vacation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
