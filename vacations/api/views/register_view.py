from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views import View
from django.contrib import messages
from vacations.models import User, Role


class RegisterPageView(View):
    """
    Renders the user registration HTML form page and handles form submission.
    """

    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not all([first_name, last_name, email, password]):
            messages.error(request, "All fields are required.")
            return render(request, "auth/register.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "auth/register.html")

        if len(password) < 4:
            messages.error(request, "Password must be at least 4 characters.")
            return render(request, "auth/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")
            return render(request, "auth/register.html")

        role = Role.objects.get(name="user")

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role
        )

        return redirect(reverse("vacation-list"))
