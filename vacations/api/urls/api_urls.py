from django.urls import path
from vacations.api.views.user_view import RegisterView, LoginView

urlpatterns: list = [
    path('register/', RegisterView.as_view(), name='api-user-register'),
    path('login/', LoginView.as_view(), name='api-user-login'),
]
