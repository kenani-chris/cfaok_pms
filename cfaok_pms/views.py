from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django import template
from django.contrib.auth.models import Group
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

