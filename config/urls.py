from django.contrib import admin
from django.urls import path, include
from vacations.api.views.login_view import LoginPageView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API URLs
    path('api/', include('vacations.api.urls.api_urls')),
    path('', include('vacations.api.urls.user_urls')),

    # HTML Template views (auth & vacations)
   #  path('auth/', include('vacations.api.urls.user_urls')),         # login/register
    path('vacations/', include('vacations.api.urls.vacation_urls')),  # vacation list, etc.

    # Default route
    path('', LoginPageView.as_view(), name='home'),
]
