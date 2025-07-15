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
        """
        Handle GET request to render the login form.
        """
        return render(request, 'auth/login.html')


class LoginFormHandlerView(View):
    """
    Handle login form submission and manage session.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST request to authenticate the user and start session.
        """
        email: str = request.POST.get('email')
        password: str = request.POST.get('password')

        user: User | None = User.objects.filter(email=email, password=password).first()

        if not user:
               
         register_url = reverse('register-form')
         messages.error(request, f"Email not registered. <a href='{register_url}'>Click here to register</a>.")
         return render(request, 'auth/login.html')


        if user:
            request.session['user_id'] = user.id
            return redirect(reverse('vacation-list'))
        
        messages.error(request, "Invalid email or password.")
        return render(request, 'auth/login.html')
        

   


class LogoutView(View):
    """
    Handle user logout and session cleanup.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handle POST request to flush session and remove CSRF cookie.
        """
        request.session.flush()
        response: HttpResponse = redirect('login-form')
        response.delete_cookie('csrftoken')  # Explicitly remove CSRF token cookie
        return response
