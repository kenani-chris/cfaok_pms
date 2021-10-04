import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from .forms import KPIForm
from .models import *
from django.utils import timezone

now = timezone.now()
# ======================================================================================================================
# Useful functions
# ======================================================================================================================
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


# Get Active PMS
def active_pms():
    if PMS.objects.filter(pms_active=True):
        return PMS.objects.filter(pms_active=True).first()


def merge_dict(dict1, dict2):
    return dict1 | dict2


# get_user_level
def get_user_level(user):
    level = LevelMembers.objects.filter(level_member_user=user, level_member_active=True)
    if level:
        level = level.first()
        level = level.level_member_level
    return level


# get_user_level
def get_level_head(user):
    if get_user_level(user):
        return get_user_level(user).level_head
    else:
        return None


# KPI Approval flow
def get_approval_flow(user, pms):
    if get_user_level(user):
        if ApprovalLevelsKPI.objects.filter(level_pms=pms):
            approval_flow = {}
            for approval in ApprovalLevelsKPI.objects.filter(level_pms=pms):
                approval_flow[approval.level_category: approval.approval_type]
            return approval_flow
        else:
            return None

    else:
        return None


# get_user_level
def get_user_submission_data(user, pms):
    if get_user_level(user):
        submission_data = SubmissionKPI.objects.filter(submission_level_category=get_user_level(user).level_category, submission_pms=pms)
        if submission_data:
            return submission_data.first()
        else:
            return None
    else:
        return None


def kpi_list(user, pms):
    context = {'approved_kpi': KPI.objects.filter(kpi_user=user, kpi_pms=pms, kpi_status='Approved'),
               'pending_kpi': KPI.objects.filter(kpi_user=user, kpi_pms=pms, kpi_status='Pending'),
               'submitted_kpi': KPI.objects.filter(kpi_user=user, kpi_pms=pms, kpi_status='Submitted'),
               'rejected_kpi': KPI.objects.filter(kpi_user=user, kpi_pms=pms, kpi_status='Rejected')}

    return context


def kpi_number_check(user, pms):
    kpi_count = 0
    if kpi_list(user, pms):
        kpis = kpi_list(user, pms)
        kpi_count = kpis['approved_kpi'].count() + kpis['pending_kpi'].count() + kpis['submitted_kpi'].count()

    return kpi_count


def kpi_weight_check(user, pms):
    kpis = kpi_list(user, pms)

    weight = 0

    for kpi in (kpis['approved_kpi']):
        weight += kpi.kpi_weight

    for kpi in (kpis['pending_kpi']):
        weight += kpi.kpi_weight

    for kpi in (kpis['submitted_kpi']):
        weight += kpi.kpi_weight

    return weight


def kpi_submission_checks(user, pms):

    date_check = number_check = True

    if get_user_submission_data(user, pms):
        submission_start = get_user_submission_data(user, pms).submission_start_date
        submission_end = get_user_submission_data(user, pms).submission_end_date

        # check dates
        if (now >= submission_start) and (now <= submission_end):
            date_check = True
        else:
            date_check = False

        # KPI no Checks
        submission_min = get_user_submission_data(user, pms).submission_minimum_number
        submission_max = get_user_submission_data(user, pms).submission_maximum_number

        if kpi_number_check(user, pms) < submission_max:
            number_check = True
        else:
            number_check = False

    # check weight
    if kpi_weight_check(user, pms)<100:
        weight_check = True
    else:
        weight_check = False

    return {'date_check': date_check,
            'number_check': number_check,
            'weight_check': weight_check}


def notification_send(request, type, sender, receiver, title, msg):
    Notification.objects.create(notification_type=type, notification_sender=sender, notification_receiver=receiver,
                                notification_title=title, notification_message=msg, notification_status='Pending')

    messages.success(request, title)


def write_log(user, category, description):
    Logs.objects.create(log_user=user, log_category=category, log_description=description)


class Dashboard(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        return context


class MyKPI(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MyKPI, self).get_context_data()

        if self.request.user.has_perm('cfao_kenya.view_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        context['date_check'] = datetime.datetime.now()
        if active_pms():
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
        return context


class MyKPICreate(CreateView):
    form_class = KPIForm
    success_url = reverse_lazy('cfao_kenya:My_KPI_Create')

    def get_context_data(self, **kwargs):
        context = super(MyKPICreate, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.add_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        if active_pms():
            context = merge_dict(context, kpi_submission_checks(self.request.user, active_pms()))
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
            context['number_kpis'] = kpi_number_check(self.request.user, active_pms())
            context['sum_weight'] = kpi_weight_check(self.request.user, active_pms())
            context['submission_data'] = get_user_submission_data(self.request.user, active_pms())
        return context

    def get_initial(self):
        initial = super(MyKPICreate, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_submit_date'] = datetime.datetime.now()

        return initial

    def form_valid(self, form):
        super(MyKPICreate, self).form_valid(form)

        write_log(self.request.user, 'KPI', 'KPI Submitted')
        notification_send(self.request, 'KPI', self.request.user, get_level_head(self.request.user), 'KPI Submitted',
                          str(self.request.user.get_full_name) + ' has  submitted a KPI for your approval')

        return HttpResponseRedirect(reverse('cfao_kenya:My_KPI_Create'))


class MyKPIView(DetailView):
    model = KPI

    def get_context_data(self, **kwargs):
        context = super(MyKPIView, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.view_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        return context


class MyKPIEdit(UpdateView):
    model = KPI
    form_class = KPIForm

    def get_context_data(self, **kwargs):
        context = super(MyKPIEdit, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.change_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        return context

    def get_initial(self):
        initial = super(MyKPIEdit, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_status'] = 'Submitted'

        return initial

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:My_KPI_View',  kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(MyKPIEdit, self).form_valid(form)
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        write_log(self.request.user, 'KPI', 'KPI ' + str(kpi.kpi_title) + ' Edited')
        notification_send(self.request, 'KPI', self.request.user, get_level_head(self.request.user), 'KPI Edited',
                          str(self.request.user.get_full_name) + ' Has edited ' + str(kpi.kpi_title) + ' ')

        return HttpResponseRedirect(reverse('cfao_kenya:My_KPI_View', kwargs={'pk': self.kwargs['pk']}))


class MyKPIDelete(DeleteView):
    model = KPI
    success_url = reverse_lazy('cfao_kenya:My_KPI')

    def get_context_data(self, **kwargs):
        context = super(MyKPIDelete, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.delete_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context = merge_dict(context, global_context(self.request.user))
        return context


class MyKPIResults(UpdateView):
    model = KPI
    form_class = KPIForm

    def get_context_data(self, **kwargs):
        context = super(MyKPIResults, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.change_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        return context

    def get_initial(self):
        initial = super(MyKPIResults, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_status'] = 'Submitted'

        return initial

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:My_KPI_Results',  kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(MyKPIResults, self).form_valid(form)
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        write_log(self.request.user, 'KPI', 'KPI ' + str(kpi.kpi_title) + ' results edited')
        notification_send(self.request, 'KPI', self.request.user, get_level_head(self.request.user), 'KPI results fed',
                          str(self.request.user.get_full_name) + ' Has edited ' + str(kpi.kpi_title) + ' ')

        return HttpResponseRedirect(reverse('cfao_kenya:My_KPI_Results', kwargs={'pk': self.kwargs['pk']}))


class MyKPIResultsList(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MyKPIResultsList, self).get_context_data()

        if self.request.user.has_perm('cfao_kenya.view_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        context['date_check'] = datetime.datetime.now()
        if active_pms():
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
        return context

