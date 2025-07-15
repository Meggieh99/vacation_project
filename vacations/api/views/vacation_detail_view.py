from django.shortcuts import get_object_or_404, render, redirect
from vacations.models import Vacation
from django.views import View
from django.contrib import messages


class VacationDetailView(View):
    """
    Display full vacation details. Requires user to be logged in.
    Shows a flash message and redirects to login page if the user is not authenticated.
    """


    def get(self, request, vacation_id: int):
        user_id = request.session.get("user_id")

        if not user_id:
            messages.error(request, "You must be logged in to view vacation details.")
            return redirect("vacation-list")

        vacation = get_object_or_404(Vacation, id=vacation_id)
        return render(request, "vacations/vacation_detail.html", {"vacation": vacation})