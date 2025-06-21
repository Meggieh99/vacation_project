from django.db import models

class Role(models.Model):
    """
    Represents a role in the system (e.g., admin, user).
    """
    name = models.CharField(max_length=50, unique=True)

class User(models.Model):
    """
    Represents a user in the system.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

class Country(models.Model):
    """
    Represents a country where vacations are located.
    """
    name = models.CharField(max_length=50, unique=True)

class Vacation(models.Model):
    """
    Represents a vacation with its details.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_filename = models.CharField(max_length=255)

class Like(models.Model):
    """
    Represents a like from a user on a vacation.
    Ensures a user can like a vacation only once.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vacation = models.ForeignKey(Vacation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'vacation')
