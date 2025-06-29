from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import VacationViewSet, CountryViewSet, UserViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'vacations', VacationViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'users', UserViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
