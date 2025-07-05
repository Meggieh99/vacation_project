from django.contrib import admin
from django.urls import path, include
from vacations.api.views.auth_view import LoginPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vacations/', include('vacations.api.urls.vacation_urls')),
    path('api/users/', include('vacations.api.urls.user_urls')),
    path('api/likes/', include('vacations.api.urls.like_urls')),
    path('', LoginPageView.as_view(), name='home'),
]
