from django.urls import path
from vacations.api.views.like_view import LikeVacationView, UnlikeVacationView

urlpatterns = [
#     path('<int:vacation_id>/like/', LikeVacationView.as_view(), name='vacation-like'),
#     path('<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name='vacation-unlike'),
#    #  path('vacations/<int:vacation_id>/like/', LikeVacationView.as_view(), name=""),
#    #  path('vacations/<int:vacation_id>/unlike/', UnlikeVacationView.as_view(), name="vacation-unlike"),
    path('vacations/like/', LikeVacationView.as_view(), name='vacation-like'),
    path('vacations/unlike/', UnlikeVacationView.as_view(), name='vacation-unlike'),

 ]
