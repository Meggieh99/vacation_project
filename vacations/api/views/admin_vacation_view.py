from django.views import View
from django.urls import reverse
from vacations.models import User, Vacation
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from vacations.api.serializers.vacation_serializer import EditVacationSerializer
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


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
    
class EditVacationFormView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View to display and handle the edit vacation form for admin only.
    """

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request, vacation_id):
        vacation = get_object_or_404(Vacation, id=vacation_id)
        serializer = EditVacationSerializer(vacation)
        return render(request, 'vacations/edit_vacation.html', {'form': serializer.data, 'vacation_id': vacation_id})

    def post(self, request, vacation_id):
        vacation = get_object_or_404(Vacation, id=vacation_id)
        data = request.POST.dict()
        serializer = EditVacationSerializer(vacation, data=data)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Vacation updated successfully.")
            return redirect('admin-vacation-list')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'vacations/edit_vacation.html', {'form': serializer.data, 'errors': serializer.errors})
