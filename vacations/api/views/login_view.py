from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from vacations.models import User
from django.http import HttpRequest, HttpResponse
from django.contrib import messages


class LoginPageView(View):
    """
    Display the login form page.
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'auth/login.html')


class LoginFormHandlerView(View):
    """
    Handle login form submission and manage session.
    """
    def post(self, request: HttpRequest) -> HttpResponse:
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')

        user: User | None = User.objects.filter(email=email, password=password).first()

        if not user:
            register_url = reverse('register-form')
            messages.error(request, f"Email not registered. <a href='{register_url}'>Click here to register</a>.")
            return render(request, 'auth/login.html')

        # store user id in session
        request.session['user_id'] = user.id

        # redirect to appropriate page
        if user.role.name.lower() == 'admin':
            return redirect(reverse('admin-vacation-list'))

        return redirect(reverse('vacation-list'))


class LogoutView(View):
    """
    Handle user logout and session cleanup.
    """
    def post(self, request: HttpRequest) -> HttpResponse:
        request.session.flush()
        response: HttpResponse = redirect('login-form')
        response.delete_cookie('csrftoken')  # delete csrf token
        return response
