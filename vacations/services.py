from typing import Optional
from django.core.exceptions import ValidationError
from vacations.models import User, Vacation, Like, Role

def register_user(first_name: str, last_name: str, email: str, password: str) -> User:
    """
    Registers a new user after validation checks.
    
    :raises ValidationError: If email already exists or password is too short.
    """
    if len(password) < 4:
        raise ValidationError("Password must be at least 4 characters long.")
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists.")
    user_role = Role.objects.get(name='user')
    return User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        role=user_role
    )

def login_user(email: str, password: str) -> Optional[User]:
    """
    Authenticates a user by email and password.
    
    :return: User object if credentials match, None otherwise.
    """
    return User.objects.filter(email=email, password=password).first()

def add_like(user_id: int, vacation_id: int) -> Like:
    """
    Adds a like from a user to a vacation.
    
    :raises ValidationError: If Like already exists.
    """
    if Like.objects.filter(user_id=user_id, vacation_id=vacation_id).exists():
        raise ValidationError("Like already exists.")
    return Like.objects.create(user_id=user_id, vacation_id=vacation_id)

def remove_like(user_id: int, vacation_id: int) -> None:
    """
    Removes a like from a user to a vacation.
    """
    Like.objects.filter(user_id=user_id, vacation_id=vacation_id).delete()
