from django.test import TestCase
from django.core.management import call_command
from vacations.models import User, Vacation, Like
from vacations.services import add_like
from django.core.exceptions import ValidationError

class LikeServiceTest(TestCase):
    """
    Like/unlike functionality tests.
    """

    def setUp(self) -> None:
        call_command('init_data')
        self.user: User = User.objects.first()
        self.vacation: Vacation = Vacation.objects.first()

    def test_add_like_success(self) -> None:
        """Positive: Add like."""
        like: Like = add_like(self.user.id, self.vacation.id)
        self.assertIsNotNone(like)

    def test_add_like_duplicate(self) -> None:
        """Negative: Add duplicate like."""
        add_like(self.user.id, self.vacation.id)
        with self.assertRaises(ValidationError):
            add_like(self.user.id, self.vacation.id)
