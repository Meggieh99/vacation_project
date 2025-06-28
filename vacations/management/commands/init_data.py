from django.core.management.base import BaseCommand
from vacations.models import Role, User, Country, Vacation
from datetime import date

class Command(BaseCommand):
    """
    Custom Django management command to populate the database with initial data.
    """

    help = "Populate the database with initial required data."

    def handle(self, *args, **kwargs) -> None:
        """
        Populates initial data including roles, users, countries, and vacations.
        """

        # Create roles
        admin_role, _ = Role.objects.get_or_create(name="admin")
        user_role, _ = Role.objects.get_or_create(name="user")

        # Create users
        User.objects.get_or_create(
            first_name="Admin",
            last_name="Manager",
            email="admin@example.com",
            password="adminpass",
            role=admin_role
        )

        User.objects.get_or_create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="johnpass",
            role=user_role
        )

        # Create countries
        country_names = ["Israel", "USA", "France", "Germany",
                         "Italy", "Spain", "Canada", "Brazil", "Japan", "Mexico"]
        country_objs = [
            Country.objects.get_or_create(name=name)[0] for name in country_names
        ]

        # Create vacations
        vacations_data = [
            ("Beach in Tel Aviv", 0, date(2025, 7, 10), date(2025, 7, 20), 2500, "tel_aviv.jpg"),
            ("New York City Trip", 1, date(2025, 8, 1), date(2025, 8, 10), 3500, "nyc.jpg"),
            ("Paris Adventure", 2, date(2025, 9, 5), date(2025, 9, 15), 3000, "paris.jpg"),
            ("Berlin History Tour", 3, date(2025, 10, 10), date(2025, 10, 20), 2700, "berlin.jpg"),
            ("Rome Exploration", 4, date(2025, 11, 1), date(2025, 11, 10), 3200, "rome.jpg"),
            ("Barcelona Highlights", 5, date(2025, 12, 15), date(2025, 12, 25), 2800, "barcelona.jpg"),
            ("Canadian Rockies", 6, date(2026, 1, 10), date(2026, 1, 20), 4000, "rockies.jpg"),
            ("Brazil Carnival", 7, date(2026, 2, 15), date(2026, 2, 25), 4500, "brazil.jpg"),
            ("Tokyo Cherry Blossoms", 8, date(2026, 3, 20), date(2026, 3, 30), 5000, "tokyo.jpg"),
            ("Mexico City Culture", 9, date(2026, 4, 5), date(2026, 4, 15), 3300, "mexico.jpg"),
            ("Dead Sea Relaxation", 0, date(2026, 5, 1), date(2026, 5, 10), 2200, "deadsea.jpg"),
            ("Miami Beach", 1, date(2026, 6, 10), date(2026, 6, 20), 3600, "miami.jpg"),
        ]

        for desc, country_idx, start, end, price, img in vacations_data:
            Vacation.objects.get_or_create(
                country=country_objs[country_idx],
                description=desc,
                start_date=start,
                end_date=end,
                price=price,
                image_filename=img
            )

        self.stdout.write(self.style.SUCCESS('Data populated successfully.'))
