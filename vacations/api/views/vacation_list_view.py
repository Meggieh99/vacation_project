from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


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
