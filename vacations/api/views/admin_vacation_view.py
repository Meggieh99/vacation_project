from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from vacations.models import User, Vacation
from django.http import HttpRequest, HttpResponse

class AdminVacationListView(View):
    """
    View for displaying vacations to Admin users only.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect(reverse('login-form'))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse('login-form'))

        # check if user is admin
        if user.role.name.lower() != 'admin':
            return HttpResponse("Unauthorized", status=403)

        # get all vacations
        vacations = Vacation.objects.all().order_by('start_date')

        context = {
            'vacations': vacations,
            'user': user
        }

        return render(request, 'vacations/admin_vacation_list.html', context)
