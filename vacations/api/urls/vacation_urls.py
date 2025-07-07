from django.urls import path
from vacations.api.views.vacation_list_view import VacationListPageView
from vacations.api.views.vacation_api_view import VacationListView, AddVacationView, EditVacationView, DeleteVacationView

urlpatterns = [
    # HTML Page for displaying vacations after login/register
    path('', VacationListPageView.as_view(), name='vacation-list'),
    
   
    # API endpoints for vacations
    path('api/vacations/', VacationListView.as_view(), name='api-vacation-list'), 
    path('api/vacations/add/', AddVacationView.as_view(), name='vacation-add'),
    path('api/vacations/<int:vacation_id>/edit/', EditVacationView.as_view(), name='vacation-edit'),
    path('api/vacations/<int:vacation_id>/delete/', DeleteVacationView.as_view(), name='vacation-delete'),
    
]
