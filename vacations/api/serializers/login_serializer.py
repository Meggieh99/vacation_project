from rest_framework import serializers
from vacations.models import User
from typing import Optional



class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login input validation.
    """

    email: serializers.EmailField = serializers.EmailField()
    password: serializers.CharField = serializers.CharField(
        min_length=4,
        error_messages={
            "min_length": "Password must be at least 4 characters long.",
            "blank": "Password is required."
        }
    )
    

    def validate(self, data: dict) -> dict:
        """
        Check if a user exists with given email and password.
        """
        email: str = data.get('email')
        password: str = data.get('password')

        user: Optional[User] = User.objects.filter(email=email, password=password).first()
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data
