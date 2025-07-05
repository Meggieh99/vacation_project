from django.urls import path
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView

urlpatterns = [
    path('vacations/<int:vacation_id>/like/', LikeVacationView.as_view(), name="vacation-like"),
    path('vacations/<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name="vacation-unlike"),
]
