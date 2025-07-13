from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from vacations.models import User
from django.http import HttpRequest, HttpResponse



class LoginPageView(View):
    """
    Render the login form.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """Display login page."""
        return render(request, 'auth/login.html')


class LoginFormHandlerView(View):
    """
    Process login form submission and manage session.
    """

    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            return redirect(reverse('vacation-list'))

        return render(request, 'auth/login.html', {
            'error_message': 'Invalid email or password'
        })
    
class LogoutView(View):
    """
    Log the user out and redirect to login form.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        request.session.flush()
        return redirect('login-form')
   
    
