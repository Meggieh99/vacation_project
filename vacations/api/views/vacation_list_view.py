from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from vacations.models import Vacation, Like
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect



class VacationListPageView(TemplateView):
    """
    Render vacation list page. Accessible only if user is logged in via session.
    """

    template_name = 'vacations/vacation_list.html'

    def dispatch(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login-form')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Add all vacations (with like info) to the context.
        """
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')

        vacations = Vacation.objects.all().order_by('start_date')

        # add info about like count ו־ liked_by_user
        vacation_data = []
        for vacation in vacations:
            vacation_data.append({
                'id': vacation.id,
                'country': vacation.country.name,
                'description': vacation.description,
                'start_date': vacation.start_date,
                'end_date': vacation.end_date,
                'price': vacation.price,
                'image_filename': vacation.image_filename,
                'like_count': Like.objects.filter(vacation_id=vacation.id).count(),
                'liked_by_user': Like.objects.filter(vacation_id=vacation.id, user_id=user_id).exists()
            })

        context['vacations'] = vacation_data
        return context
   