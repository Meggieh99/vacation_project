from django.shortcuts import render, redirect
from django.urls import reverse
from vacations.models import User, Role
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views import View
from django.http import HttpRequest, HttpResponse


class LoginPageView(View):
    """
    Handle GET (display form) and POST (login logic) for the login page.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'auth/login.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, 'auth/login.html')

        # Check password length
        if len(password) < 4:
            messages.error(request, "Password must be at least 4 characters.")
            return render(request, 'auth/login.html')

        # Check credentials
        user = User.objects.filter(email=email, password=password).first()
        if not user:
            messages.error(request, "Invalid email or password.")
            return render(request, 'auth/login.html')

        return redirect(reverse("vacation-list"))


class RegisterPageView(View):
    """
    Render the user registration HTML form page.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'auth/register.html')


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle POST registration form and save new user.
    """
    if request.method == "POST":
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

    return render(request, "auth/register.html")
