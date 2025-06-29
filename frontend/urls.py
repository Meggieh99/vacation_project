from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('vacations/', views.vacations_page, name='vacations'),
    path('logout/', views.logout_view, name='logout'),
]
