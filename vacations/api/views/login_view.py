from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.urls import reverse
from vacations.models import User
from django.views import View


class LoginPageView(TemplateView):
    """
    View for rendering the login form page.
    """
    template_name = 'auth/login.html'


class LoginFormHandlerView(View):
    """
    Handles the login POST request.
    """

    def post(self, request):
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "auth/login.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format.")
            return render(request, "auth/login.html")

        if len(password) < 4:
            messages.error(request, "Password must be at least 4 characters.")
            return render(request, "auth/login.html")

        user = User.objects.filter(email=email, password=password).first()
        if not user:
            messages.error(request, "Invalid email or password.")
            return render(request, "auth/login.html")

        return redirect(reverse("vacation-list"))
