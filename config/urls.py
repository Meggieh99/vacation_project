from django.contrib import admin
from django.urls import path, include
from vacations.api.views.login_view import LoginPageView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints (like, vacations, auth API)
    path('api/', include('vacations.api.urls.api_urls')),
    path('api/', include('vacations.api.urls.vacation_urls')),  # includes /vacations/like, etc.

    # HTML Template Views (login, register, vacation page)
    path('', include('vacations.api.urls.user_urls')),
    path('vacations/', include('vacations.api.urls.vacation_urls')),  # vacation list HTML

    # Default route
    path('', LoginPageView.as_view(), name='home'),
]
