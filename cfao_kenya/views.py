from django.views.generic import *

from .forms import KPIForm
from .models import *
import os
from cfao_kenya import *


# One method to list all compile context
def global_context(user):
    context = {}
    # company contexts
    if CompanyProfile.objects.filter(company_profile_active=True):
        context['company'] = CompanyProfile.objects.filter(company_profile_active=True).first()

    # staff
    if Staff.objects.filter(staff_active=True):
        context['staff'] = Staff.objects.filter(staff_active=True, staff_person=user).first()

    # pms
    if PMS.objects.filter(pms_active=True):
        context['pms'] = PMS.objects.filter(pms_active=True).first()

    # level head
    if Level.objects.filter(level_head=user):
        context['level_head'] = Level.objects.filter(level_head=user).first()

    return context


def merge_dict(dict1, dict2):
    return dict1 | dict2


class Dashboard(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        return context


class MyKPI(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MyKPI, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        return context


class MyKPICreate(CreateView):
    form_class = KPIForm

    def get_context_data(self, **kwargs):
        context = super(MyKPICreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        return context
