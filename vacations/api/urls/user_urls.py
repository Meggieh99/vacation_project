from django.urls import path
from vacations.api.views.user_view import RegisterView, LoginView
from vacations.api.views.auth_view import RegisterPageView, LoginPageView

urlpatterns: list = [
    # API endpoints
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),

    # HTML form pages
    path('register/form/', RegisterPageView.as_view(), name='register-form'),
    path('', LoginPageView.as_view(), name='login-form'),  # default route
]
