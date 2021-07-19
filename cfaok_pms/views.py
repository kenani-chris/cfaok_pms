from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import template
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import TemplateView

from cfao_kenya.views import send_mail


@login_required
def home(request):
    context = {
        '': 'that'
    }
    return render(request, 'home.html', context)


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()


def change_user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('change_user_password_done'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


class PasswordChangeDone(TemplateView):
    template_name = 'registration/password_change_done.html'


'''
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class HomeView(TemplateView):
    template_name = '../re'
    model = pms
    form_class = PasswordChangeForm'''
