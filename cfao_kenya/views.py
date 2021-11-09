import datetime
from calendar import _monthlen
from itertools import chain

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import *

from cfaok_pms.settings import EMAIL_HOST_USER
from .forms import KPIForm, PMSForm, CheckInForm, AssessmentForm, QuestionForm, UserForm, StaffForm, UserEditForm, \
    CategoryForm, LevelForm, LevelMemberForm, QuestionResponseForm
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


# ======================================================================================================================
# Useful functions
# ======================================================================================================================
# One method to list all compile context

def get_staff(user):
    if Staff.objects.filter(staff_person=user):
        return Staff.objects.filter(staff_person=user).first()
    else:
        return None


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

    # Categories up
    categories_up_list = []
    if get_user_level(user):
        all_categories_up(get_user_level(user).level_category, categories_up_list)
    else:
        all_categories_up(None, categories_up_list)
    context['categories_up_list'] = categories_up_list

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


# get_user_level_head
def get_user_level_head(user):
    level = Level.objects.filter(level_head=user)
    if level:
        level = level.first()
    return level


# get_user_level
def get_user_category(user):
    if get_user_level_head(user):
        level_cat = get_user_level_head(user).level_category
    else:
        if get_user_level_head(user):
            all_cat = []
            all_categories_down(get_user_level(user).level_category, all_cat)
            if len(all_cat) > 0:
                level_cat = all_cat[-1]
            else:
                level_cat = None
        else:
            level_cat = None
    return level_cat


# get_level_head
def get_level_head(user):
    if get_user_level(user):
        return get_user_level(user).level_head
    else:
        return None


def all_categories_down(cat, cat_list):
    if cat is None:
        return
    else:
        for category in LevelCategory.objects.all():
            if cat == category.category_parent:
                cat_list.append(category)
                all_categories_down(category, cat_list)


def all_categories_up(cat, cat_list):
    if cat is None:
        return
    else:
        cat_list.append(cat)
        all_categories_up(cat.category_parent, cat_list)


def all_levels_up(level, level_list):
    if level is None:
        return
    else:
        level_list.append(level)
        all_levels_up(level.level_parent, level_list)


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
    if get_user_level(user) and get_staff(user):
        submission_data = SubmissionKPI.objects.filter(submission_level_category=get_staff(user).staff_category,
                                                       submission_pms=pms)
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
    if kpi_weight_check(user, pms) < 100:
        weight_check = True
    else:
        weight_check = False

    return {'date_check': date_check,
            'number_check': number_check,
            'weight_check': weight_check}


def notification_send(request, n_type, sender, receiver, title, msg):
    Notification.objects.create(notification_type=n_type, notification_sender=sender, notification_receiver=receiver,
                                notification_title=title, notification_message=msg, notification_status='Pending')

    messages.success(request, title)


def write_log(user, category, description):
    Logs.objects.create(log_user=user, log_category=category, log_description=description)


def calculate_kpi_score(kpi):
    kpi_score = 0
    kpi_sum = 0
    apr = kpi.kpi_april_score
    may = kpi.kpi_may_score
    jun = kpi.kpi_june_score
    jul = kpi.kpi_july_score
    aug = kpi.kpi_august_score
    sep = kpi.kpi_september_score
    oct = kpi.kpi_october_score
    nov = kpi.kpi_november_score
    dec = kpi.kpi_december_score
    jan = kpi.kpi_january_score
    feb = kpi.kpi_february_score
    mar = kpi.kpi_march_score

    result_dict = {'April': apr, 'May': may, 'June': jun, 'July': jul, 'August': aug, 'September': sep,
                   'October': oct, 'November': nov, 'December': dec, 'January': jan, 'February': feb, 'March': mar}

    if get_user_submission_data(kpi.kpi_user, kpi.kpi_pms):
        month_results = []
        submission = get_user_submission_data(kpi.kpi_user, kpi.kpi_pms)

        if submission.submission_april_results_calculation:
            month_results.append(apr)

        if submission.submission_may_results_calculation:
            month_results.append(may)

        if submission.submission_june_results_calculation:
            month_results.append(jun)

        if submission.submission_july_results_calculation:
            month_results.append(jul)

        if submission.submission_august_results_calculation:
            month_results.append(aug)

        if submission.submission_september_results_calculation:
            month_results.append(sep)

        if submission.submission_october_results_calculation:
            month_results.append(oct)

        if submission.submission_november_results_calculation:
            month_results.append(nov)

        if submission.submission_december_results_calculation:
            month_results.append(dec)

        if submission.submission_january_results_calculation:
            month_results.append(jan)

        if submission.submission_february_results_calculation:
            month_results.append(feb)

        if submission.submission_march_results_calculation:
            month_results.append(mar)

    else:
        month_results = [apr, may, jun, jul, aug, sep, oct, nov, dec, jan, feb, mar]
    month_results = [0 if v is None else v for v in month_results]
    kpi_sum = round(sum(month_results), 2)
    kpi_average = round(kpi_sum/len(month_results), 2)

    if kpi.kpi_function.lower() == 'maximize':
        if kpi.kpi_type.lower() == 'addition':
            kpi_score = (kpi_sum/kpi.kpi_target) * 100
        elif kpi.kpi_type.lower() == 'average':
            kpi_score = (kpi_average/kpi.kpi_target) * 100
        elif kpi.kpi_type.lower() == 'ytd':
            if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                this_month = datetime.date.today().strftime("%B")
                last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                if result_dict[this_month] is None:
                    if result_dict[last_month] is None:
                        kpi_score = (0/kpi.kpi_target) *100
                    else:
                        kpi_score = (result_dict[last_month] / kpi.kpi_target) * 100
                else:
                    kpi_score = (result_dict[this_month]/ kpi.kpi_target) * 100
            else:
                if mar is None:
                    mar = 0
                kpi_score = (mar/kpi.kpi_target) * 100
    elif kpi.kpi_function.lower() == 'minimize':
        if kpi.kpi_type.lower() == 'addition':
            kpi_score = (kpi.kpi_target/kpi_sum) * 100
        elif kpi.kpi_type.lower() == 'average':
            kpi_score = (kpi.kpi_target/kpi_average) * 100
        elif kpi.kpi_type.lower() == 'ytd':
            if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                this_month = datetime.date.today().strftime("%B")
                last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                if result_dict[this_month] is None:
                    if result_dict[last_month] is None:
                        kpi_score = 0
                    else:
                        kpi_score = (kpi.kpi_target/result_dict[last_month]) * 100
                else:
                    kpi_score = (kpi.kpi_target/result_dict[this_month]) * 100
            else:
                if mar is None:
                    mar = 0
                kpi_score = (mar/kpi.kpi_target) * 100

    return kpi_score


def calculate_overall_kpi_score(user, pms):
    kpis = kpi_list(user, pms)
    results = []
    for kpi in kpis['approved_kpi']:
        weight = kpi.kpi_weight
        score = calculate_kpi_score(kpi)
        weighted_score = (weight * score)/100
        results.append(weighted_score)
    return sum(results)


class NoActivePMS(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(NoActivePMS, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        return context


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
        return '{}'.format(reverse('cfao_kenya:My_KPI_View', kwargs={'pk': self.kwargs['pk']}))

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
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        context = super(MyKPIResults, self).get_context_data()
        if self.request.user.has_perm('cfao_kenya.change_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))

        months = {}
        reveal = {}
        if active_pms():
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
            submission = get_user_submission_data(self.request.user, active_pms())
            if submission:
                months['April'] = submission.submission_april_results
                months['May'] = submission.submission_may_results
                months['June'] = submission.submission_june_results
                months['July'] = submission.submission_july_results
                months['August'] = submission.submission_august_results
                months['September'] = submission.submission_september_results
                months['October'] = submission.submission_october_results
                months['November'] = submission.submission_november_results
                months['December'] = submission.submission_december_results
                months['January'] = submission.submission_january_results
                months['February'] = submission.submission_february_results
                months['March'] = submission.submission_march_results
            else:
                months['April'] = months['May'] = months['June'] = months['July'] = months['August'] = \
                    months['September'] = months['October'] = months['November'] = months['December'] = \
                    months['January'] = months['February'] = months['March'] = 15

            # check if the field result field should show

            # 1. Check if result is approved
            if kpi.kpi_all_results_approve is True:
                reveal['April'] = reveal['May'] = reveal['June'] = reveal['July'] = reveal['August'] = \
                    reveal['September'] = reveal['October'] = reveal['November'] = reveal['December'] = \
                    reveal['January'] = reveal['February'] = reveal['March'] = False
            else:
                today_date = datetime.date.today()
                reveal['April'] = reveal['May'] = reveal['June'] = reveal['July'] = reveal['August'] = \
                    reveal['September'] = reveal['October'] = reveal['November'] = reveal['December'] = \
                    reveal['January'] = reveal['February'] = reveal['March'] = False

                # Check if the result is approved or within the time

                # April Check
                if kpi.kpi_april_score_approve is True:
                    reveal['April'] = False
                else:
                    april_end_month = datetime.date(year=year['April'], month=4, day=_monthlen(year['April'], 4))
                    april_deadline = april_end_month + datetime.timedelta(days=months['April'])

                    if april_end_month <= today_date <= april_deadline:
                        reveal['April'] = True

                # May Check
                if kpi.kpi_may_score_approve is True:
                    reveal['May'] = False
                else:
                    may_end_month = datetime.date(year=year['May'], month=5, day=_monthlen(year['May'], 5))
                    may_deadline = may_end_month + datetime.timedelta(days=months['May'])

                    if may_end_month <= today_date <= may_deadline:
                        reveal['May'] = True

                # June Check
                if kpi.kpi_june_score_approve is True:
                    reveal['June'] = False
                else:
                    june_end_month = datetime.date(year=year['June'], month=6, day=_monthlen(year['June'], 6))
                    june_deadline = june_end_month + datetime.timedelta(days=months['June'])

                    if june_end_month <= today_date <= june_deadline:
                        reveal['June'] = True

                # July Check
                if kpi.kpi_july_score_approve is True:
                    reveal['July'] = False
                else:
                    july_end_month = datetime.date(year=year['July'], month=7, day=_monthlen(year['July'], 7))
                    july_deadline = july_end_month + datetime.timedelta(days=months['July'])

                    if july_end_month <= today_date <= july_deadline:
                        reveal['July'] = True

                # August Check
                if kpi.kpi_august_score_approve is True:
                    reveal['August'] = False
                else:
                    august_end_month = datetime.date(year=year['August'], month=8, day=_monthlen(year['August'], 8))
                    august_deadline = august_end_month + datetime.timedelta(days=months['August'])

                    if august_end_month <= today_date <= august_deadline:
                        reveal['August'] = True

                # September Check
                if kpi.kpi_september_score_approve is True:
                    reveal['September'] = False
                else:
                    september_end_month = datetime.date(year=year['September'], month=9, day=_monthlen(year['September'], 9))
                    september_deadline = september_end_month + datetime.timedelta(days=months['September'])

                    if september_end_month <= today_date <= september_deadline:
                        reveal['September'] = True

                # October Check
                if kpi.kpi_october_score_approve is True:
                    reveal['October'] = False
                else:
                    october_end_month = datetime.date(year=year['October'], month=10, day=_monthlen(year['October'], 10))
                    october_deadline = october_end_month + datetime.timedelta(days=months['October'])

                    if october_end_month <= today_date <= october_deadline:
                        reveal['October'] = True

                # November Check
                if kpi.kpi_november_score_approve is True:
                    reveal['November'] = False
                else:
                    november_end_month = datetime.date(year=year['November'], month=11, day=_monthlen(year['November'], 11))
                    november_deadline = november_end_month + datetime.timedelta(days=months['November'])

                    if november_end_month <= today_date <= november_deadline:
                        reveal['November'] = True

                # December Check
                if kpi.kpi_december_score_approve is True:
                    reveal['December'] = False
                else:
                    december_end_month = datetime.date(year=year['December'], month=12, day=_monthlen(year['December'], 12))
                    december_deadline = december_end_month + datetime.timedelta(days=months['December'])

                    if december_end_month <= today_date <= december_deadline:
                        reveal['December'] = True

                # January Check
                if kpi.kpi_january_score_approve is True:
                    reveal['January'] = False
                else:
                    january_end_month = datetime.date(year=year['January'], month=1, day=_monthlen(year['January'], 1))
                    january_deadline = january_end_month + datetime.timedelta(days=months['January'])

                    if january_end_month <= today_date <= january_deadline:
                        reveal['January'] = True

                # February Check
                if kpi.kpi_february_score_approve is True:
                    reveal['February'] = False
                else:
                    february_end_month = datetime.date(year=year['February'], month=2, day=_monthlen(year['February'], 2))
                    february_deadline = february_end_month + datetime.timedelta(days=months['February'])

                    if february_end_month <= today_date <= february_deadline:
                        reveal['February'] = True

                # March Check
                if kpi.kpi_march_score_approve is True:
                    reveal['March'] = False
                else:
                    march_end_month = datetime.date(year=year['March'], month=3, day=_monthlen(year['March'], 3))
                    march_deadline = march_end_month + datetime.timedelta(days=months['March'])

                    if march_end_month <= today_date <= march_deadline:
                        reveal['March'] = True

        context['reveal'] = reveal
        return context

    def get_initial(self):
        initial = super(MyKPIResults, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_status'] = 'Submitted'

        return initial

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:My_KPI_Results', kwargs={'pk': self.kwargs['pk']}))

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


class KPICategory(DetailView):
    model = LevelCategory

    def get_context_data(self, **kwargs):
        context = super(KPICategory, self).get_context_data()
        categories = get_object_or_404(LevelCategory, category_id=self.kwargs['pk'])
        this_list = []
        all_categories_down(categories, this_list)
        if len(this_list) > 0:
            this_list = this_list[-1]
        context['this_list'] = this_list
        print(this_list)
        level_categories = []
        level_list = []
        if get_user_level(self.request.user):
            all_levels_up(get_user_level(self.request.user), level_list)

        for level in level_list:
            if level.level_category == categories:
                level_categories.append(level)

        context['level_in_category'] = level_categories

        if self.request.user.has_perm('cfao_kenya.list_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))

        return context


class KPICategoryLevel(DetailView):
    model = Level

    def get_context_data(self, **kwargs):
        context = super(KPICategoryLevel, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        level = get_object_or_404(Level, level_id=self.kwargs['pk'])

        if self.request.user.has_perm('cfao_kenya.list_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        if active_pms():
            context = merge_dict(context, kpi_list(level.level_head, active_pms()))
            kpi_results = []
            for kpi in context['approved_kpi']:
                kpi_results.append([kpi, calculate_kpi_score(kpi)])
            context['kpi_results'] = kpi_results
            context['kpi_overall_results'] = calculate_overall_kpi_score(self.request.user, active_pms())


        return context


class KPICategoryLevelOne(DetailView):
    model = KPI

    def get_context_data(self, **kwargs):
        context = super(KPICategoryLevelOne, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        context['level'] = get_object_or_404(Level, level_id=self.kwargs['lev_id'])
        if self.request.user.has_perm('cfao_kenya.view_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        return context


class KPICategoryLevelOneResults(UpdateView):
    model = KPI
    form_class = KPIForm

    def get_context_data(self, **kwargs):
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        calculate_kpi_score(kpi)

        context = super(KPICategoryLevelOneResults, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        context['level'] = get_object_or_404(Level, level_id=self.kwargs['lev_id'])
        if self.request.user.has_perm('cfao_kenya.change_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context = merge_dict(global_context(self.request.user), context)

        months = {}
        reveal = {}
        if active_pms():
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
            submission = get_user_submission_data(self.request.user, active_pms())
            if submission:
                months['April'] = submission.submission_april_results
                months['May'] = submission.submission_may_results
                months['June'] = submission.submission_june_results
                months['July'] = submission.submission_july_results
                months['August'] = submission.submission_august_results
                months['September'] = submission.submission_september_results
                months['October'] = submission.submission_october_results
                months['November'] = submission.submission_november_results
                months['December'] = submission.submission_december_results
                months['January'] = submission.submission_january_results
                months['February'] = submission.submission_february_results
                months['March'] = submission.submission_march_results
            else:
                months['April'] = months['May'] = months['June'] = months['July'] = months['August'] = \
                    months['September'] = months['October'] = months['November'] = months['December'] = \
                    months['January'] = months['February'] = months['March'] = 15

            # check if the field result field should show

            # 1. Check if result is approved
            if kpi.kpi_all_results_approve is True:
                reveal['April'] = reveal['May'] = reveal['June'] = reveal['July'] = reveal['August'] = \
                    reveal['September'] = reveal['October'] = reveal['November'] = reveal['December'] = \
                    reveal['January'] = reveal['February'] = reveal['March'] = False
            else:
                today_date = datetime.date.today()
                reveal['April'] = reveal['May'] = reveal['June'] = reveal['July'] = reveal['August'] = \
                    reveal['September'] = reveal['October'] = reveal['November'] = reveal['December'] = \
                    reveal['January'] = reveal['February'] = reveal['March'] = False

                # Check if the result is approved or within the time

                # April Check
                if kpi.kpi_april_score_approve is True:
                    reveal['April'] = False
                else:
                    april_end_month = datetime.date(year=year['April'], month=4, day=_monthlen(year['April'], 4))
                    april_deadline = april_end_month + datetime.timedelta(days=months['April'])

                    if april_end_month <= today_date <= april_deadline:
                        reveal['April'] = True

                # May Check
                if kpi.kpi_may_score_approve is True:
                    reveal['May'] = False
                else:
                    may_end_month = datetime.date(year=year['May'], month=5, day=_monthlen(year['May'], 5))
                    may_deadline = may_end_month + datetime.timedelta(days=months['May'])

                    if may_end_month <= today_date <= may_deadline:
                        reveal['May'] = True

                # June Check
                if kpi.kpi_june_score_approve is True:
                    reveal['June'] = False
                else:
                    june_end_month = datetime.date(year=year['June'], month=6, day=_monthlen(year['June'], 6))
                    june_deadline = june_end_month + datetime.timedelta(days=months['June'])

                    if june_end_month <= today_date <= june_deadline:
                        reveal['June'] = True

                # July Check
                if kpi.kpi_july_score_approve is True:
                    reveal['July'] = False
                else:
                    july_end_month = datetime.date(year=year['July'], month=7, day=_monthlen(year['July'], 7))
                    july_deadline = july_end_month + datetime.timedelta(days=months['July'])

                    if july_end_month <= today_date <= july_deadline:
                        reveal['July'] = True

                # August Check
                if kpi.kpi_august_score_approve is True:
                    reveal['August'] = False
                else:
                    august_end_month = datetime.date(year=year['August'], month=8, day=_monthlen(year['August'], 8))
                    august_deadline = august_end_month + datetime.timedelta(days=months['August'])

                    if august_end_month <= today_date <= august_deadline:
                        reveal['August'] = True

                # September Check
                if kpi.kpi_september_score_approve is True:
                    reveal['September'] = False
                else:
                    september_end_month = datetime.date(year=year['September'], month=9, day=_monthlen(year['September'], 9))
                    september_deadline = september_end_month + datetime.timedelta(days=months['September'])

                    if september_end_month <= today_date <= september_deadline:
                        reveal['September'] = True

                # October Check
                if kpi.kpi_october_score_approve is True:
                    reveal['October'] = False
                else:
                    october_end_month = datetime.date(year=year['October'], month=10, day=_monthlen(year['October'], 10))
                    october_deadline = october_end_month + datetime.timedelta(days=months['October'])

                    if october_end_month <= today_date <= october_deadline:
                        reveal['October'] = True

                # November Check
                if kpi.kpi_november_score_approve is True:
                    reveal['November'] = False
                else:
                    november_end_month = datetime.date(year=year['November'], month=11, day=_monthlen(year['November'], 11))
                    november_deadline = november_end_month + datetime.timedelta(days=months['November'])

                    if november_end_month <= today_date <= november_deadline:
                        reveal['November'] = True

                # December Check
                if kpi.kpi_december_score_approve is True:
                    reveal['December'] = False
                else:
                    december_end_month = datetime.date(year=year['December'], month=12, day=_monthlen(year['December'], 12))
                    december_deadline = december_end_month + datetime.timedelta(days=months['December'])

                    if december_end_month <= today_date <= december_deadline:
                        reveal['December'] = True

                # January Check
                if kpi.kpi_january_score_approve is True:
                    reveal['January'] = False
                else:
                    january_end_month = datetime.date(year=year['January'], month=1, day=_monthlen(year['January'], 1))
                    january_deadline = january_end_month + datetime.timedelta(days=months['January'])

                    if january_end_month <= today_date <= january_deadline:
                        reveal['January'] = True

                # February Check
                if kpi.kpi_february_score_approve is True:
                    reveal['February'] = False
                else:
                    february_end_month = datetime.date(year=year['February'], month=2, day=_monthlen(year['February'], 2))
                    february_deadline = february_end_month + datetime.timedelta(days=months['February'])

                    if february_end_month <= today_date <= february_deadline:
                        reveal['February'] = True

                # March Check
                if kpi.kpi_march_score_approve is True:
                    reveal['March'] = False
                else:
                    march_end_month = datetime.date(year=year['March'], month=3, day=_monthlen(year['March'], 3))
                    march_deadline = march_end_month + datetime.timedelta(days=months['March'])

                    if march_end_month <= today_date <= march_deadline:
                        reveal['March'] = True

        context['reveal'] = reveal
        return context

    def get_initial(self):
        initial = super(KPICategoryLevelOneResults, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_status'] = 'Submitted'

        return initial

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:My_KPI_Results', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(KPICategoryLevelOneResults, self).form_valid(form)
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        write_log(self.request.user, 'KPI', 'KPI ' + str(kpi.kpi_title) + ' results edited')
        notification_send(self.request, 'KPI', self.request.user, get_level_head(self.request.user), 'KPI results fed',
                          str(self.request.user.get_full_name) + ' Has edited ' + str(kpi.kpi_title) + ' ')

        return HttpResponseRedirect(reverse('cfao_kenya:My_KPI_Results', kwargs={'pk': self.kwargs['pk']}))


class KPICategoryResults(DetailView):
    model = LevelCategory

    def get_context_data(self, **kwargs):
        context = super(KPICategoryResults, self).get_context_data()

        categories = get_object_or_404(LevelCategory, category_id=self.kwargs['pk'])
        level_categories = []
        level_list = []
        if get_user_level(self.request.user):
            all_levels_up(get_user_level(self.request.user), level_list)

        for level in level_list:
            if level.level_category == categories:
                level_categories.append(level)

        context['level_in_category'] = level_categories

        if self.request.user.has_perm('cfao_kenya.list_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        context['date_check'] = datetime.datetime.now()
        if active_pms():
            context = merge_dict(context, kpi_list(self.request.user, active_pms()))
            kpi_results = []
            for kpi in context['approved_kpi']:
                kpi_results.append([kpi, calculate_kpi_score(kpi)])
            context['kpi_results'] = kpi_results
        return context


class KPICategoryLevelEdit(UpdateView):
    model = KPI
    form_class = KPIForm

    def get_context_data(self, **kwargs):
        context = super(KPICategoryLevelEdit, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        context['level'] = get_object_or_404(Level, level_id=self.kwargs['lev_id'])
        if self.request.user.has_perm('cfao_kenya.change_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        return context

    def get_initial(self):
        initial = super(KPICategoryLevelEdit, self).get_initial()
        initial['kpi_user'] = self.request.user
        initial['kpi_pms'] = active_pms()
        initial['kpi_status'] = 'Submitted'

        return initial

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:KPI_Category_Level_One', kwargs={'cat_id': self.kwargs['cat_id'],
                                                                                'lev_id': self.kwargs['lev_id'],
                                                                                'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(KPICategoryLevelEdit, self).form_valid(form)
        kpi = get_object_or_404(KPI, kpi_id=self.kwargs['pk'])
        write_log(self.request.user, 'KPI', 'KPI ' + str(kpi.kpi_title) + ' Edited')
        notification_send(self.request, 'KPI', self.request.user, get_level_head(self.request.user), 'KPI Edited',
                          str(self.request.user.get_full_name) + ' Has edited ' + str(kpi.kpi_title) + ' ')

        return HttpResponseRedirect(reverse('cfao_kenya:KPI_Category_Level_One', kwargs={
            'cat_id': self.kwargs['cat_id'], 'lev_id': self.kwargs['lev_id'], 'pk': self.kwargs['pk']}))


class KPICategoryLevelDelete(DeleteView):
    model = KPI

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:KPI_Category_Level', kwargs={'cat_id': self.kwargs['cat_id'],
                                                                            'pk': self.kwargs['lev_id']}))

    def get_context_data(self, **kwargs):
        context = super(KPICategoryLevelDelete, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        context['level'] = get_object_or_404(Level, level_id=self.kwargs['lev_id'])
        if self.request.user.has_perm('cfao_kenya.delete_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context = merge_dict(context, global_context(self.request.user))
        return context


class KPICategoryLevelNew(CreateView):
    form_class = KPIForm

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:KPI_Category_Level', kwargs={'cat_id': self.kwargs['cat_id'],
                                                                            'pk': self.kwargs['lev_id']}))

    def get_context_data(self, **kwargs):
        context = super(KPICategoryLevelNew, self).get_context_data()
        context['levelcategory'] = get_object_or_404(LevelCategory, category_id=self.kwargs['cat_id'])
        context['level'] = get_object_or_404(Level, level_id=self.kwargs['lev_id'])
        if self.request.user.has_perm('cfao_kenya.add_level_up_kpi'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context = merge_dict(context, global_context(self.request.user))
        level_head = get_object_or_404(Level, level_id=self.kwargs['lev_id']).level_head
        if active_pms():
            context = merge_dict(context, kpi_submission_checks(level_head, active_pms()))
            context = merge_dict(context, kpi_list(level_head, active_pms()))
            context['number_kpis'] = kpi_number_check(level_head, active_pms())
            context['sum_weight'] = kpi_weight_check(level_head, active_pms())
            context['submission_data'] = get_user_submission_data(level_head, active_pms())
        return context

    def get_initial(self):
        initial = super(KPICategoryLevelNew, self).get_initial()
        level_head = get_object_or_404(Level, level_id=self.kwargs['lev_id']).level_head
        initial['kpi_user'] = level_head
        initial['kpi_pms'] = active_pms()
        initial['kpi_submit_date'] = datetime.datetime.now()

        return initial

    def form_valid(self, form):
        super(KPICategoryLevelNew, self).form_valid(form)
        level_head = get_object_or_404(Level, level_id=self.kwargs['lev_id']).level_head
        write_log(self.request.user, 'KPI', 'KPI Submitted')
        notification_send(self.request, 'KPI', level_head, get_level_head(level_head), 'KPI Submitted',
                          str(self.request.user.get_full_name) + ' has  submitted a KPI for your approval')

        return HttpResponseRedirect(reverse('cfao_kenya:KPI_Category_Level', kwargs={'cat_id': self.kwargs['cat_id'],
                                                                            'pk': self.kwargs['lev_id']}))


def admin_permission_check(permission, user):
    staff_account = get_staff(user)
    if staff_account:
        if user.has_perm(permission) and staff_account.staff_active and staff_account.staff_superuser:
            return True
        else:
            return False
    else:
        return False

# Admin todo Move all Admin views to somewhere else
# Views todo Verify permissions for every View


class AdminDashboard(ListView):
    model = PMS

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminDashboard, self).get_context_data()
        context['users'] = Staff.objects.all()
        context['users_active'] = Staff.objects.filter(staff_active=True)
        context['pms'] = PMS.objects.all()
        context['pms_active'] = PMS.objects.filter(pms_active=True)
        context['levels'] = Level.objects.all()
        context['categories'] = LevelCategory.objects.all()

        context['page_permission'] = admin_permission_check('view_pms', self.request.user)

        return context


class AdminDashboardPMSCreate(CreateView):
    form_class = PMSForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminDashboardPMSCreate, self).get_context_data()
        context['pms'] = PMS.objects.all()
        context['page_permission'] = admin_permission_check('add_pms', self.request.user)

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_PMS_Create',))


class AdminDashboardPMSView(DetailView):
    model = PMS

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminDashboardPMSView, self).get_context_data()
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['page_permission'] = admin_permission_check('view_pms', self.request.user)

        return context


class AdminDashboardPMSEdit(UpdateView):
    model = PMS
    form_class = PMSForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminDashboardPMSEdit, self).get_context_data()
        context['page_permission'] = admin_permission_check('change_pms', self.request.user)

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_PMS_Edit', kwargs={'pk': self.kwargs['pk']}))


class AdminDashboardPMSDelete(DeleteView):
    model = PMS

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminDashboardPMSDelete, self).get_context_data()
        context['page_permission'] = admin_permission_check('delete_pms', self.request.user)

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Home'))


class AdminUser(ListView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUser, self).get_context_data()
        context['users'] = User.objects.all()
        context['users_active'] = User.objects.filter(is_active=True)
        context['staff'] = Staff.objects.all()
        context['staff_active'] = Staff.objects.filter(staff_active=True)
        user_list = []
        for user in context['users']:
            user_list.append([user, Staff.objects.filter(staff_person=user)])

        context['user_list'] = user_list

        context['page_permission'] = admin_permission_check('view_users', self.request.user)

        return context


class AdminUserCreate(CreateView):
    form_class = UserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['users'] = User.objects.all()
        user_list = []
        for user in context['users']:
            user_list.append([user, Staff.objects.filter(staff_person=user)])

        context['user_list'] = user_list

        return context

    def get_success_url(self):
        pk = User.objects.latest('id').pk
        return '{}'.format(reverse('cfao_kenya:Admin_Staff_Create', kwargs={'pk': pk}))


class AdminUserEdit(UpdateView):
    model = User
    form_class = UserEditForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['users'] = User.objects.all()
        user_list = []
        for user in context['users']:
            user_list.append([user, Staff.objects.filter(staff_person=user)])

        context['user_list'] = user_list

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Users_View', kwargs={'pk': self.kwargs['pk']}))


class AdminUserDelete(DeleteView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.user_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['user'] = get_object_or_404(User, id=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Users',))


class AdminStaffCreate(CreateView):
    form_class = StaffForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminStaffCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['user'] = get_object_or_404(User, id=self.kwargs['pk'])
        context['users'] = User.objects.all()
        user_list = []
        for user in context['users']:
            user_list.append([user, Staff.objects.filter(staff_person=user)])

        context['user_list'] = user_list

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Users_View', kwargs={'pk': self.kwargs['pk']}))

    def get_initial(self):
        initial = super(AdminStaffCreate, self).get_initial()
        initial['staff_person'] = get_object_or_404(User, id=self.kwargs['pk'])
        return initial


class AdminStaffEdit(UpdateView):
    model = Staff
    form_class = StaffForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminStaffEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))

        context['user'] = get_object_or_404(User, id=get_object_or_404(Staff, staff_id=self.kwargs['pk']).staff_person.id)
        if self.request.user.has_perm('cfao_kenya.staff_edit'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Users_View', kwargs={'pk': get_object_or_404(Staff, staff_id=self.kwargs['pk']).staff_person.id}))


class AdminStaffDelete(DeleteView):
    model = Staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminStaffDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.staff_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['staff'] = get_object_or_404(Staff, staff_id=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Users',))



class AdminUserView(DetailView):
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminUserView, self).get_context_data()
        context['user'] = get_object_or_404(User, id=self.kwargs['pk'])
        context['staff_accounts'] = Staff.objects.filter(staff_person_id=self.kwargs['pk'])
        context['page_permission'] = admin_permission_check('view_users', self.request.user)


        return context


class AdminCategory(ListView):
    context_object_name = 'Category'
    model = LevelCategory

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminCategory, self).get_context_data()
        context['page_permission'] = admin_permission_check('view_category', self.request.user)
        return context


class AdminCategoryCreate(CreateView):
    form_class = CategoryForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminCategoryCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.category_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['Category'] = LevelCategory.objects.all()
        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Category', ))


class AdminCategoryView(DetailView):
    model = LevelCategory
    context_object_name = 'Category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminCategoryView, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.category_view'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context


class AdminCategoryEdit(UpdateView):
    model = LevelCategory
    form_class = CategoryForm
    context_object_name = 'Category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminCategoryEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.category_change'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Category_View', kwargs={'pk': self.kwargs['pk']}))


class AdminCategoryDelete(DeleteView):
    model = LevelCategory
    context_object_name = 'Category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminCategoryDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.category_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Category', ))


# Levels


class AdminLevel(ListView):
    context_object_name = 'Level'
    model = Level

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevel, self).get_context_data()
        context['page_permission'] = admin_permission_check('view_level', self.request.user)
        return context


class AdminLevelCreate(CreateView):
    form_class = LevelForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevelCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.level_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['Level'] = Level.objects.all()
        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Level', ))


class AdminLevelView(DetailView):
    model = Level
    context_object_name = 'Level'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevelView, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.level_view'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['level_members'] = LevelMembers.objects.filter(level_member_level_id=self.kwargs['pk'])

        return context


class AdminLevelEdit(UpdateView):
    model = Level
    form_class = LevelForm
    context_object_name = 'Level'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevelEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.level_change'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Level_View', kwargs={'pk': self.kwargs['pk']}))


class AdminLevelDelete(DeleteView):
    model = Level
    context_object_name = 'Level'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevelDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.level_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Level', ))


def level_member_status(request, pk, mem_id):
    level_member = get_object_or_404(LevelMembers, level_member_id=mem_id)
    if level_member.level_member_active is True:
        level_member.level_member_active = False
        level_member.save()
    else:
        level_member.level_member_active = True
        level_member.save()

    return HttpResponseRedirect(reverse('cfao_kenya:Admin_Level_View', kwargs={'pk': pk}))


def level_member_remove(request, pk, mem_id):
    get_object_or_404(LevelMembers, level_member_id=mem_id).delete()
    return HttpResponseRedirect(reverse('cfao_kenya:Admin_Level_View', kwargs={'pk': pk}))


class AdminLevelMemberCreate(CreateView):
    form_class = LevelMemberForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminLevelMemberCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.level_member_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['Level'] = get_object_or_404(Level, level_id=self.kwargs['pk'])
        context['level_members'] = LevelMembers.objects.filter(level_member_level_id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Level_Member_Create', kwargs={'pk': self.kwargs['pk']}))

    def get_initial(self):
        initial = super(AdminLevelMemberCreate, self).get_initial()
        initial['level_member_level'] = get_object_or_404(Level, level_id=self.kwargs['pk'])
        return initial


class AdminAssessment(ListView):
    context_object_name = 'Assessment'

    def get_queryset(self):
        return Assessment.objects.filter(assessment_pms=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessment, self).get_context_data()
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['page_permission'] = admin_permission_check('view_assessment', self.request.user)

        return context


class AdminAssessmentCreate(CreateView):
    form_class = AssessmentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['Assessment'] = Assessment.objects.filter(assessment_pms=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment', kwargs={'pk': self.kwargs['pk']}))

    def get_initial(self):
        initial = super(AdminAssessmentCreate, self).get_initial()
        initial['assessment_pms'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        return initial


class AdminAssessmentView(DetailView):
    model = Assessment
    pk_url_kwarg = 'aid'
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentView, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_view'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])

        context['questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'])
        context['top_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'], question_direction='Top')
        context['bottom_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'], question_direction='Bottom')

        return context


class AdminAssessmentEdit(UpdateView):
    model = Assessment
    pk_url_kwarg = 'aid'
    form_class = AssessmentForm
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_change'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment_View', kwargs={'pk': self.kwargs['pk'], 'aid': self.kwargs['aid']}))


class AdminAssessmentDelete(DeleteView):
    model = Assessment
    pk_url_kwarg = 'aid'
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.assessment_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment', kwargs={'pk': self.kwargs['pk']}))


class AdminAssessmentQuestionCreate(CreateView):
    form_class = QuestionForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentQuestionCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.question_create'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['Assessment'] = get_object_or_404(Assessment, assessment_id=self.kwargs['aid'])

        context['questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'])
        context['top_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                            question_direction='Top')
        context['bottom_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                               question_direction='Bottom')

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment_Question_Create', kwargs={'pk': self.kwargs['pk'], 'aid': self.kwargs['aid']}))

    def get_initial(self):
        initial = super(AdminAssessmentQuestionCreate, self).get_initial()
        initial['question_assessment'] = get_object_or_404(Assessment, assessment_id=self.kwargs['aid'])
        return initial


class AdminAssessmentQuestionEdit(UpdateView):
    model = Questions
    form_class = QuestionForm
    pk_url_kwarg = 'qid'
    context_object_name = 'Question'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentQuestionEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.question_edit'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['Assessment'] = get_object_or_404(Assessment, assessment_id=self.kwargs['aid'])

        context['questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'])
        context['top_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                            question_direction='Top')
        context['bottom_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                               question_direction='Bottom')

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment_Question_Edit', kwargs={'pk': self.kwargs['pk'], 'aid': self.kwargs['aid'], 'qid': self.kwargs['qid']}))


class AdminAssessmentQuestionDelete(DeleteView):
    model = Questions
    pk_url_kwarg = 'qid'
    context_object_name = 'Question'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentQuestionDelete, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.question_delete'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['Assessment'] = get_object_or_404(Assessment, assessment_id=self.kwargs['aid'])

        context['questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'])
        context['top_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                            question_direction='Top')
        context['bottom_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'],
                                                               question_direction='Bottom')

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:Admin_Assessment_View', kwargs={'pk': self.kwargs['pk'], 'aid': self.kwargs['aid']}))


class AdminAssessmentQuestion(DetailView):
    model = Questions
    pk_url_kwarg = 'qid'
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdminAssessmentQuestion, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.question_view'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False
        context['pms_select'] = get_object_or_404(PMS, pms_id=self.kwargs['pk'])
        context['Assessment'] = get_object_or_404(Assessment, assessment_id=self.kwargs['aid'])

        context['top_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'], question_direction='Top')
        context['bottom_questions'] = Questions.objects.filter(question_assessment_id=self.kwargs['aid'], question_direction='Bottom')

        return context


class MyCheckIn(ListView):
    model = CheckIn
    context_object_name = 'CheckIn'

    def get_queryset(self):
        return CheckIn.objects.filter(checkIn_user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyCheckIn, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        ci = CheckIn.objects.filter(checkIn_user=self.request.user)
        context['approved_ci'] = ci.filter(checkIn_status='Approved')
        context['pending_ci'] = ci.filter(checkIn_status='Pending')
        context['rejected_ci'] = ci.filter(checkIn_status='Rejected')
        if self.request.user.has_perm('cfao_kenya.view_checkin'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context


class MyCheckInCreate(CreateView):
    form_class = CheckInForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyCheckInCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        if self.request.user.has_perm('cfao_kenya.add_checkin'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        if CheckIn.objects.filter(checkIn_user=self.request.user, checkIn_month=datetime.date.today().strftime('%B')):
            context['done'] = True
        else:
            context['done'] = False
        context['CheckIn'] = CheckIn.objects.filter(checkIn_user=self.request.user)

        return context

    def get_success_url(self):
        return '{}'.format(reverse('cfao_kenya:My_CheckIn',))

    def get_initial(self):
        initial = super(MyCheckInCreate, self).get_initial()
        initial['checkIn_pms'] = active_pms()
        initial['checkIn_user'] = self.request.user
        initial['checkIn_submit_date'] = datetime.datetime.now()
        initial['checkIn_month'] = datetime.date.today().strftime('%B')
        return initial


class MyCheckInView(DetailView):
    model = CheckIn
    context_object_name = 'CheckIn'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyCheckInView, self).get_context_data()
        context['page_permission'] = admin_permission_check('view_pms', self.request.user)
        if self.request.user.has_perm('cfao_kenya.view_checkin'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context


class MyCheckInEdit(UpdateView):
    model = CheckIn
    form_class = CheckInForm
    context_object_name = 'CheckIn'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyCheckInEdit, self).get_context_data()
        context['page_permission'] = admin_permission_check('view_pms', self.request.user)
        if self.request.user.has_perm('cfao_kenya.change_checkin'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
       return '{}'.format(reverse('cfao_kenya:My_CheckIn_View', kwargs={'pk': self.kwargs['pk']}))


class MyCheckInDelete(DeleteView):
    model = CheckIn
    context_object_name = 'CheckIn'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyCheckInDelete, self).get_context_data()
        context['page_permission'] = admin_permission_check('view_pms', self.request.user)
        if self.request.user.has_perm('cfao_kenya.delete_checkin'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context

    def get_success_url(self):
       return '{}'.format(reverse('cfao_kenya:My_CheckIn',))


class AssessmentList(ListView):
    model = Assessment
    context_object_name = 'Assessment'

    def get_queryset(self):
        return Assessment.objects.filter(assessment_pms=active_pms())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssessmentList, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        assessment = Assessment.objects.filter(assessment_pms=active_pms())
        context['assessment_current'] = assessment.filter(assessment_start_date__lte=datetime.date.today(), assessment_end_date__gte=datetime.date.today())
        context['assessment_future'] = assessment.filter(assessment_start_date__gt=datetime.date.today())
        context['assessment_past'] = assessment.filter(assessment_end_date__lt=datetime.date.today())
        if self.request.user.has_perm('cfao_kenya.view_assessment'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        return context


class AssessmentView(DetailView):
    model = Assessment
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssessmentView, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        assessment = get_object_or_404(Assessment, assessment_id=self.kwargs['pk'])
        if assessment.assessment_start_date <= datetime.date.today() <= assessment.assessment_end_date:
            context['assessment_status'] = True
        else:
            context['assessment_status'] = False

        if self.request.user.has_perm('cfao_kenya.view_assessment'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        all_questions = Questions.objects.filter(question_assessment_id=self.kwargs['pk'])
        if all_questions:
            context['questions'] = all_questions
            context['top_questions'] = all_questions.filter(question_direction='Top')
            context['bottom_questions'] = all_questions.filter(question_direction='Bottom')

        level_members = []
        level_heads = []

        # Get subordinate staff
        if Level.objects.filter(level_head=self.request.user):
            for level in Level.objects.filter(level_head=self.request.user):
                if LevelMembers.objects.filter(level_member_level=level, level_member_active=True):
                    for records in LevelMembers.objects.filter(level_member_level=level, level_member_active=True):
                        level_members.append(records)

        # Get Team Leaders
        if LevelMembers.objects.filter(level_member_user=self.request.user, level_member_active=True):
            for level in LevelMembers.objects.filter(level_member_user=self.request.user, level_member_active=True):
                level_heads.append(level.level_member_level)

        context['level_heads'] = level_heads
        context['level_members'] = level_members


        return context


class AssessmentViewMember(DetailView):
    model = Assessment
    context_object_name = 'Assessment'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssessmentViewMember, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))
        assessment = get_object_or_404(Assessment, assessment_id=self.kwargs['pk'])
        member = get_object_or_404(User, id=self.kwargs['uid'])
        if assessment.assessment_start_date <= datetime.date.today() <= assessment.assessment_end_date:
            context['assessment_status'] = True
        else:
            context['assessment_status'] = False

        question_responses = []
        questions = Questions.objects.filter(question_assessment_id=self.kwargs['pk'], question_direction=self.kwargs['dir'])
        completed = 0

        if questions.count():
            for question in questions:
                response = QuestionResponses.objects.filter(response_question_id=question.question_id, response_user=self.request.user,
                                                            response_evaluated=member)
                if response:
                    question_responses.append([question, response, 'Done'])
                    completed = completed + 1
                else:
                    question_responses.append([question, None, 'Not Done'])
            completed = completed / questions.count()
        else:
            completed = 0

        if self.request.user.has_perm('cfao_kenya.add_question_response'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['question_responses'] = question_responses
        context['completed'] = completed
        context['member'] = member

        return context


class AssessmentViewMemberResponseCreate(CreateView):
    form_class = QuestionResponseForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssessmentViewMemberResponseCreate, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))

        assessment = get_object_or_404(Assessment, assessment_id=self.kwargs['pk'])
        member = get_object_or_404(User, id=self.kwargs['uid'])
        direction = self.kwargs['dir']
        question = get_object_or_404(Questions, question_id=self.kwargs['qid'])

        if assessment.assessment_start_date <= datetime.date.today() <= assessment.assessment_end_date:
            context['assessment_status'] = True
        else:
            context['assessment_status'] = False

        response = QuestionResponses.objects.filter(response_question_id=question.question_id,
                                                    response_user=self.request.user, response_evaluated=member)
        if response:
            completed = True
        else:
            completed = False

        if self.request.user.has_perm('cfao_kenya.add_question_response'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['Assessment'] = assessment
        context['completed'] = completed
        context['question'] = question
        context['member'] = member

        return context

    def get_initial(self):
        initial = super(AssessmentViewMemberResponseCreate, self).get_initial()
        initial['response_user'] = self.request.user
        initial['response_evaluated'] = get_object_or_404(User, id=self.kwargs['uid'])
        initial['response_question'] = get_object_or_404(Questions, question_id=self.kwargs['qid'])

        return initial

    def get_success_url(self):
       return '{}'.format(reverse('cfao_kenya:Assessment_View_Member', kwargs={'pk': self.kwargs['pk'], 'uid': self.kwargs['uid'], 'dir': self.kwargs['dir']}))


class AssessmentViewMemberResponseEdit(UpdateView):
    pk_url_kwarg = 'qrid'
    model = QuestionResponses
    form_class = QuestionResponseForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AssessmentViewMemberResponseEdit, self).get_context_data()
        context = merge_dict(context, global_context(self.request.user))

        assessment = get_object_or_404(Assessment, assessment_id=self.kwargs['pk'])
        member = get_object_or_404(User, id=self.kwargs['uid'])
        direction = self.kwargs['dir']
        response = get_object_or_404(QuestionResponses, response_id=self.kwargs['qrid'])

        if assessment.assessment_start_date <= datetime.date.today() <= assessment.assessment_end_date:
            context['assessment_status'] = True
        else:
            context['assessment_status'] = False

        if self.request.user.has_perm('cfao_kenya.add_question_response'):
            context['page_permission'] = True
        else:
            context['page_permission'] = False

        context['Assessment'] = assessment
        context['member'] = member

        return context

    def get_success_url(self):
       return '{}'.format(reverse('cfao_kenya:Assessment_View_Member', kwargs={'pk': self.kwargs['pk'], 'uid': self.kwargs['uid'], 'dir': self.kwargs['dir']}))


