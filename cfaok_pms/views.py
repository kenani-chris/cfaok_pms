from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_safe
from django.views.generic import TemplateView
from Site.models import Staff


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staffAccounts'] = Staff.objects.filter(staff_active=True, staff_person=self.request.user)
        return context


@require_POST
def self_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('self_change_user_password_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change-password.html', {
        'form': form
    })


@require_safe
def self_password_change_done(request):
    return render(request, 'registration/change-password-done.html',)


def lockout(request, credentials):
    return render(request, 'registration/locked_out.html', )
