from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.apps import apps


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = []
        model = None
        for name, app in apps.app_configs.items():
            try:
                model = apps.get_model(name, model_name='Staff')
                staff = model.objects.filter(staff_person=self.request.user, staff_active=True)
                if staff:
                    result.append([name, staff])
            except Exception as e:
                pass
        context['result'] = result
        return context


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


def self_password_change_done(request):
    return render(request, 'registration/change-password-done.html',)
