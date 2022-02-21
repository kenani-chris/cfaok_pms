import datetime
from itertools import chain

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import *

from cfaok_pms.settings import EMAIL_HOST_USER
from .forms import *
from .models import *
from django.utils import timezone

now = timezone.now()

year = {
    'April': datetime.datetime.now().year,
    'May': datetime.datetime.now().year,
    'June': datetime.datetime.now().year,
    'July': datetime.datetime.now().year,
    'August': datetime.datetime.now().year,
    'September': datetime.datetime.now().year,
    'October': datetime.datetime.now().year,
    'November': datetime.datetime.now().year,
    'December': datetime.datetime.now().year,
    'January': datetime.datetime.now().year + 1,
    'February': datetime.datetime.now().year + 1,
    'March': datetime.datetime.now().year + 1,
    }

def get_staff(user):
    if Staff.objects.filter(staff_person=user):
        return Staff.objects.filter(staff_person=user).first()
    else:
        return None



class Dashboard(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data()

        kpi_results = []
        context['kpi_results'] = kpi_results

        return context



