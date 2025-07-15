from django.contrib import admin
from django.urls import path, include
from vacations.api.views.login_view import LoginPageView


urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('vacations.api.urls.api_urls')),
    path('api/', include('vacations.api.urls.vacation_urls')),

    # HTML endpoints 
    path('', include('vacations.api.urls.vacation_urls')),

    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('vacations.api.urls.user_urls')),
    path('', LoginPageView.as_view(), name='home'),
]

