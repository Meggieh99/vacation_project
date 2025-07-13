from django.urls import path
from vacations.api.views.vacation_list_view import VacationListPageView
from vacations.api.views.vacation_api_view import VacationListView, AddVacationView, EditVacationView, DeleteVacationView
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView

urlpatterns = [
    # Vacation page (HTML)
    path('', VacationListPageView.as_view(), name='vacation-list'),

    # Vacation API
    path('vacations/', VacationListView.as_view(), name='api-vacation-list'),
    path('vacations/add/', AddVacationView.as_view(), name='vacation-add'),
    path('vacations/<int:vacation_id>/edit/', EditVacationView.as_view(), name='vacation-edit'),
    path('vacations/<int:vacation_id>/delete/', DeleteVacationView.as_view(), name='vacation-delete'),
    #  # Like / Unlike endpoints (API)
    path('vacations/<int:vacation_id>/like/', LikeVacationView.as_view(), name='vacation-like'),
    path('vacations/<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name='vacation-unlike'),

]
