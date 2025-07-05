from django.urls import path
from vacations.api.views.vacation_view import (
    VacationListView, AddVacationView, EditVacationView, DeleteVacationView
)
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView

urlpatterns = [
    path('vacations/', VacationListView.as_view(), name="vacation-list"),
    path('vacations/add/', AddVacationView.as_view(), name="vacation-add"),
    path('vacations/<int:vacation_id>/edit/', EditVacationView.as_view(), name="vacation-edit"),
    path('vacations/<int:vacation_id>/delete/', DeleteVacationView.as_view(), name="vacation-delete"),
    
]
