import os
from email.mime.image import MIMEImage
from pathlib import Path

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views import generic
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.views.generic import *
from itertools import chain
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from .permissions import is_member_company
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin


def get_active_pms():
    if pms.objects.filter(pms_status='Active').count() != 1:
        return None
    else:
        return pms.objects.get(pms_status='Active')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class HomeView(TemplateView):
    template_name = 'index.html'
    model = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
            context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
            context['user_is_md'] = self.request.user.staff_person.staff_md
            context['user_is_tl'] = self.request.user.staff_person.staff_head_team
            context['user_team'] = self.request.user.staff_person.staff_team
            context['user_bu'] = self.request.user.staff_person.staff_bu
        else:
            context['pms'] = pms.objects.get(pms_status='Active')
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class NoActivePmsView(TemplateView):
    template_name = 'no_active_pms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            context['pms'] = pms.objects.get(pms_status='Active')
        return context


# =====================================================================================================================
#                                                 INDIVIDUAL KPI
# =====================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class IndividualKpiView(ListView):
    model = individual_Kpi
    template_name = 'Individual_Kpi/mykpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user, individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class SubmitKpiView(CreateView):
    form_class = SubmitKpiForm
    template_name = 'Individual_Kpi/submitkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user, individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_initial(self):
        initial = super(SubmitKpiView, self).get_initial()
        initial['individual_kpi_pms'] = pms.objects.get(pms_status='Active')
        initial['individual_kpi_user'] = self.request.user
        initial['individual_kpi_submit_date'] = datetime.date.today()
        initial['individual_kpi_last_edit'] = datetime.date.today()
        initial['individual_kpi_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Individual_Kpi_Submit'))

    def form_valid(self, form):
        super(SubmitKpiView, self).form_valid(form)
        user_team = get_object_or_404(staff, pk=self.request.user.id)
        user_team = user_team.staff_team
        e_message = ""
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
                e_message = 'you have one KPI from ' + self.request.user.get_full_name() + ' that requires your approval'
            else:
                team_leader = None
                e_message = 'Your KPI has been submitted successfully but i keep on failing contacting your immediate ' \
                          'supervisor.<br>Please raise the issue with HR for support'
        else:
            team_leader = None
            e_message = 'Your KPI has been submitted successfully but i keep on failing contacting your immediate ' \
                      'supervisor.<br>Please raise the issue with HR for support'

        send_email_pms('KPI Approval', team_leader, self.request.user, e_message)

        messages.success(self.request, 'KPI submit successful')

        return HttpResponseRedirect(reverse('Individual_Kpi_Submit'))


def send_email_pms(subject, receiver1, receiver2, e_message):
    if receiver1 is None:
        to_email = [receiver2.email]
        name = receiver2.get_full_name()
    else:
        to_email = [receiver1.email, receiver2.email]
        name = receiver1.get_full_name()

    body_html = '''
        <html>
            <body>
                <br>Dear '''+name+''',
                <br>
                <br>
                ''' + e_message + '''
                Kind regards,
                <br>
                <br>
                <hr>
                <b>Do not reply to this message, for it is system Generated</b>
                <hr>
                <br>
                Kind regards,
                <br>
                Notifier, PMS
                <br>
                A solution of CFAO Kenya Limited<br>
                <img src='cid:logo.png' />
            </body>
        </html>'''

    from_email = settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives(
        subject,
        body_html,
        from_email=from_email,
        to=to_email
    )

    msg.mixed_subtype = 'related'
    msg.attach_alternative(body_html, "text/html")
    img_dir = 'static/images'
    image = 'cfao_kenya_sign.jpg'
    file_path = os.path.join(img_dir, image)
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', 'logo.png')
        img.add_header('Content-Disposition', 'inline', filename=image)
    msg.attach(img)
    msg.send()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackKpiView(ListView):
    model = individual_Kpi
    template_name = 'Individual_Kpi/trackkpi.html'
    active_pms = pms

    def get_queryset(self):
        if get_active_pms() is None:
            return None
        else:
            return individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                 individual_kpi_pms=get_active_pms())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditKpiView(UpdateView):
    model = individual_Kpi
    form_class = SubmitKpiForm
    template_name = 'Individual_Kpi/one_individual_kpi_edit.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_success_url(self):
        return '{}'.format(reverse('kpi-detail', kwargs={"pk":self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class DetailKpiView(DetailView):
    model = individual_Kpi
    template_name = 'Individual_Kpi/one_individual_kpi.html'
    active_pms = pms

    def get_queryset(self):
        if get_active_pms() is None:
            return None
        else:
            return individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                 individual_kpi_pms=get_active_pms())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class KpiResultView(ListView):
    model = individual_Kpi
    template_name = 'Individual_Kpi/kpiresults.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class KpiResultUpdateView(UpdateView):
    model = individual_Kpi
    form_class = IndividualKpiResultsForm
    template_name = 'Individual_Kpi/one_individual_kpi_update.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            today = datetime.date.today()
            day = int(today.strftime('%d'))
            month = today.strftime('%B').lower()
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            submit_date = int(active_pms.pms_individual_submit_results_date)

            result_kpi = get_object_or_404(individual_Kpi, pk=self.kwargs['pk'])

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7, 'november': 8,
                      'december': 9, 'january': 10, 'february': 11, 'march': 12}

            if result_kpi.individual_kpi_april_score_approve == 'Approved':
                april = 'hidden'
            else:
                if months[month] <= months['april']:
                    april = 'reveal'
                elif (months[month] - months['april']) == 1:
                    if day <= submit_date:
                        april = 'reveal'
                    else:
                        april = 'hidden'
                else:
                    april = 'hidden'
            
            if result_kpi.individual_kpi_may_score_approve == 'Approved':
                may = 'hidden'
            else:
                if months[month] <= months['may']:
                    may = 'reveal'
                elif (months[month] - months['may']) == 1:
                    if day <= submit_date:
                        may = 'reveal'
                    else:
                        may = 'hidden'
                else:
                    may = 'hidden'
            
            if result_kpi.individual_kpi_june_score_approve == 'Approved':
                june = 'hidden'
            else:
                if months[month] <= months['june']:
                    june = 'reveal'
                elif (months[month] - months['june']) == 1:
                    if day <= submit_date:
                        june = 'reveal'
                    else:
                        june = 'hidden'
                else:
                    june = 'hidden'
                    
            if result_kpi.individual_kpi_july_score_approve == 'Approved':
                july = 'hidden'
            else:
                if months[month] <= months['july']:
                    july = 'reveal'
                elif (months[month] - months['july']) == 1:
                    if day <= submit_date:
                        july = 'reveal'
                    else:
                        july = 'hidden'
                else:
                    july = 'hidden'
                    
            if result_kpi.individual_kpi_august_score_approve == 'Approved':
                august = 'hidden'
            else:
                if months[month] <= months['august']:
                    august = 'reveal'
                elif (months[month] - months['august']) == 1:
                    if day <= submit_date:
                        august = 'reveal'
                    else:
                        august = 'hidden'
                else:
                    august = 'hidden'
            
            if result_kpi.individual_kpi_september_score_approve == 'Approved':
                september = 'hidden'
            else:
                if months[month] <= months['september']:
                    september = 'reveal'
                elif (months[month] - months['september']) == 1:
                    if day <= submit_date:
                        september = 'reveal'
                    else:
                        september = 'hidden'
                else:
                    september = 'hidden'
                    
            if result_kpi.individual_kpi_october_score_approve == 'Approved':
                october = 'hidden'
            else:
                if months[month] <= months['october']:
                    october = 'reveal'
                elif (months[month] - months['october']) == 1:
                    if day <= submit_date:
                        october = 'reveal'
                    else:
                        october = 'hidden'
                else:
                    october = 'hidden'
            
            if result_kpi.individual_kpi_november_score_approve == 'Approved':
                november = 'hidden'
            else:
                if months[month] <= months['november']:
                    november = 'reveal'
                elif (months[month] - months['november']) == 1:
                    if day <= submit_date:
                        november = 'reveal'
                    else:
                        november = 'hidden'
                else:
                    november = 'hidden'
            
            if result_kpi.individual_kpi_december_score_approve == 'Approved':
                december = 'hidden'
            else:
                if months[month] <= months['december']:
                    december = 'reveal'
                elif (months[month] - months['december']) == 1:
                    if day <= submit_date:
                        december = 'reveal'
                    else:
                        december = 'hidden'
                else:
                    december = 'hidden'
            
            if result_kpi.individual_kpi_january_score_approve == 'Approved':
                january = 'hidden'
            else:
                if months[month] <= months['january']:
                    january = 'reveal'
                elif (months[month] - months['january']) == 1:
                    if day <= submit_date:
                        january = 'reveal'
                    else:
                        january = 'hidden'
                else:
                    january = 'hidden'
            
            if result_kpi.individual_kpi_february_score_approve == 'Approved':
                february = 'hidden'
            else:
                if months[month] <= months['february']:
                    february = 'reveal'
                elif (months[month] - months['february']) == 1:
                    if day <= submit_date:
                        february = 'reveal'
                    else:
                        february = 'hidden'
                else:
                    february = 'hidden'
            
            if result_kpi.individual_kpi_march_score_approve == 'Approved':
                march = 'hidden'
            else:
                if months[month] <= months['march']:
                    march = 'reveal'
                elif (months[month] - months['march']) == 1:
                    if day <= submit_date:
                        march = 'reveal'
                    else:
                        march = 'hidden'
                else:
                    march = 'hidden'
                    
            context['april'] = april
            context['may'] = may
            context['june'] = june
            context['july'] = july
            context['august'] = august
            context['september'] = september
            context['october'] = october
            context['november'] = november
            context['december'] = december
            context['january'] = january
            context['february'] = february
            context['march'] = march

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def form_valid(self, form):
        super(KpiResultUpdateView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('Individual_Kpi_Result_Update', kwargs={"pk":self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('Individual_Kpi_Result_Update', kwargs={"pk":self.kwargs["pk"]}))


# ======================================================================================================================
#                                           STAFF KPI
# ======================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiListView(ListView):
    model = individual_Kpi
    template_name = 'Staff_Kpi/staffkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            tl = context['user_is_tl']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if tl is not None:
                team_members = staff.objects.filter(staff_team=tl).exclude(staff_person=self.request.user)
                team_members_kpi = []

                for member in team_members:
                    kpi = individual_Kpi.objects.filter(individual_kpi_user=member.staff_person,
                                                        individual_kpi_pms=active_pms)
                    approved1_kpi = kpi.filter(individual_kpi_status='Approved 1')
                    approved2_kpi = kpi.filter(individual_kpi_status='Approved 2')
                    pending_kpi = kpi.filter(individual_kpi_status='Pending')
                    edit_kpi = kpi.filter(individual_kpi_status='Edit')
                    rejected1_kpi = kpi.filter(individual_kpi_status='Rejected 1')
                    rejected2_kpi = kpi.filter(individual_kpi_status='Rejected 2')

                    required_count = pms.pms_individual_kpi_number
                    submitted_count = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + \
                                      edit_kpi.count() + rejected1_kpi.count()
                    rejected_count = rejected2_kpi.count()
                    pending_count = pending_kpi.count() + rejected1_kpi.count() + edit_kpi.count()

                    team_members_kpi.append([member.staff_person.get_full_name(), member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
            else:
                team_members = None
                context['team_members'] = team_members
                context['team_members_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiPendingListView(ListView):
    model = individual_Kpi
    template_name = 'Staff_Kpi/approvekpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            tl = context['user_is_tl']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if tl is not None:
                team_members = staff.objects.filter(staff_team=tl).exclude(staff_person=self.request.user)
                team_members_kpi = []

                for member in team_members:
                    kpi = individual_Kpi.objects.filter(individual_kpi_user=member.staff_person,
                                                        individual_kpi_pms=active_pms)
                    approved1_kpi = kpi.filter(individual_kpi_status='Approved 1')
                    approved2_kpi = kpi.filter(individual_kpi_status='Approved 2')
                    pending_kpi = kpi.filter(individual_kpi_status='Pending')
                    edit_kpi = kpi.filter(individual_kpi_status='Edit')
                    rejected1_kpi = kpi.filter(individual_kpi_status='Rejected 1')
                    rejected2_kpi = kpi.filter(individual_kpi_status='Rejected 2')

                    required_count = pms.pms_individual_kpi_number
                    submitted_count = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + \
                                      edit_kpi.count() + rejected1_kpi.count()
                    rejected_count = rejected2_kpi.count()
                    pending_count = pending_kpi.count() + rejected1_kpi.count() + edit_kpi.count()

                    team_members_kpi.append([member, member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
            else:
                team_members = None
                context['team_members'] = team_members
                context['team_members_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiApproveView(DetailView):
    model = User
    template_name = 'Staff_Kpi/one_individual_approve_kpi.html'
    active_pms = pms
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.kwargs['pk'],
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@login_required
def approve_individual_kpi(request, pk, kpi_id):
    staff_person = get_object_or_404(staff, id=request.user.id)
    user_is_bu_head = staff_person.staff_head_bu
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    kpi = individual_Kpi.objects.get(individual_kpi_id=kpi_id)

    if user_is_bu_head is not None or user_is_md == 'Yes':
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[2][0],
            individual_kpi_bu_leader_approval=request.user.id,
            individual_kpi_approval2_date=datetime.date.today(),
        )
        messages.success(request, 'KPI Approved successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved"
        send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    elif user_is_tl is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[1][0],
            individual_kpi_team_leader_approval=request.user.id,
            individual_kpi_approval1_date=datetime.date.today(),
        )

        messages.success(request, 'KPI Approved successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved and is escalated for second level " \
                                                         "approval"
        send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


@login_required
def reject_individual_kpi(request, pk, kpi_id):
    staff_person = get_object_or_404(staff, id=request.user.id)
    user_is_bu_head = staff_person.staff_head_bu
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    kpi = individual_Kpi.objects.get(individual_kpi_id=kpi_id)

    if user_is_bu_head is not None or user_is_md is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[0][0],
            individual_kpi_bu_leader_approval=request.user.id,
        )

        messages.success(request, 'KPI Rejected successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been Rejected<br> KPI status has changed to" \
                                                         " <b>Pending</b> to allow you to edit the KPI approval"
        send_email_pms('KPI Rejected', User.objects.get(id=pk), request.user, message)
    elif user_is_tl is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[0][0], individual_kpi_team_leader_approval=request.user.id)

        messages.success(request, 'KPI Rejected successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been Rejected<br> KPI status has changed to" \
                                                         " <b>Pending</b> to allow you to edit the KPI approval"
        send_email_pms('KPI Rejected', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


@login_required
def approve_individual_kpi_score(request, pk, kpi_id, month):
    staff_person = get_object_or_404(staff, id=request.user.id)
    user_is_bu_head = staff_person.staff_head_bu
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    kpi = individual_Kpi.objects.get(individual_kpi_id=kpi_id)

    if user_is_bu_head is not None or user_is_md == 'Yes':
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[2][0],
            individual_kpi_bu_leader_approval=request.user.id,
            individual_kpi_approval2_date=datetime.date.today(),
        )
        messages.success(request, 'KPI Approved successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved"
        send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    elif user_is_tl is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[1][0],
            individual_kpi_team_leader_approval=request.user.id,
            individual_kpi_approval1_date=datetime.date.today(),
        )

        messages.success(request, 'KPI Approved successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved and is escalated for second level " \
                                                         "approval"
        send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackKpiListView(ListView):
    model = individual_Kpi
    template_name = 'Staff_Kpi/trackkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            tl = context['user_is_tl']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if tl is not None:
                team_members = staff.objects.filter(staff_team=tl).exclude(staff_person=self.request.user)
                team_members_kpi = []

                for member in team_members:
                    kpi = individual_Kpi.objects.filter(individual_kpi_user=member.staff_person,
                                                        individual_kpi_pms=active_pms)
                    approved1_kpi = kpi.filter(individual_kpi_status='Approved 1')
                    approved2_kpi = kpi.filter(individual_kpi_status='Approved 2')
                    pending_kpi = kpi.filter(individual_kpi_status='Pending')
                    edit_kpi = kpi.filter(individual_kpi_status='Edit')
                    rejected1_kpi = kpi.filter(individual_kpi_status='Rejected 1')
                    rejected2_kpi = kpi.filter(individual_kpi_status='Rejected 2')

                    required_count = pms.pms_individual_kpi_number
                    submitted_count = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + \
                                      edit_kpi.count() + rejected1_kpi.count()
                    rejected_count = rejected2_kpi.count()
                    pending_count = pending_kpi.count() + rejected1_kpi.count() + edit_kpi.count()

                    team_members_kpi.append([member, member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
            else:
                team_members = None
                context['team_members'] = team_members
                context['team_members_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackKpiOneListView(ListView):
    model = individual_Kpi
    template_name = 'Staff_Kpi/trackkpi_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['staff'] = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=context['staff'], individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = active_pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiTrackOneView(DetailView):
    model = User
    template_name = 'Staff_Kpi/trackkpi_staff_one.html'
    active_pms = pms
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = individual_Kpi.objects.filter(individual_kpi_user=self.kwargs['pk'],
                                                individual_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(individual_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(individual_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(individual_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(individual_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(individual_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(individual_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@login_required
def staff_trackkpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        kpi_approved_count = 0
        kpi_pending_count = 0
        kpi_zero_count = 0
        staff_n_kpi = None
        if team_members is not None:
            for member in team_members:
                staff_approved1_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                    individual_kpi_pms=active_pms,
                                                                    individual_kpi_status='Approved 1').count()
                staff_approved2_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                    individual_kpi_pms=active_pms,
                                                                    individual_kpi_status='Approved 2').count()
                staff_pending_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                  individual_kpi_pms=active_pms,
                                                                  individual_kpi_status='Pending').count()
                total_kpi = staff_approved1_kpi + staff_approved2_kpi + staff_pending_kpi

                staff_n_kpi = [staff_n_kpi,
                               [member.staff_person.id, member.staff_person.get_full_name, member.staff_person.email,
                                member.staff_Pf_Number, staff_approved1_kpi, staff_approved2_kpi, staff_pending_kpi,
                                total_kpi]]

                if staff_approved2_kpi > 0:
                    kpi_approved_count = + 1

                if staff_pending_kpi > 0:
                    kpi_pending_count = + 1

                if total_kpi < 1:
                    kpi_zero_count = + 1
        else:
            staff_n_kpi = None
    else:
        team_members = None

    no_of_bu = bu.objects.all().count()

    if active_pms is not None:
        all_kpi = individual_Kpi.objects.filter(individual_kpi_user=request.user, individual_kpi_pms=active_pms)
        if all_kpi is not None:
            approved1_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status='Approved 1')
            approved2_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status='Approved 2')
            pending_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Pending")
            edit_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Edit")
            rejected1_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Rejected 1")
            rejected2_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Rejected 2")
            total_submitted = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + edit_kpi.count()
            total_pending = approved1_kpi.count() + pending_kpi.count()
            total_rejected = rejected1_kpi.count() + rejected2_kpi.count()
            percent_submitted = total_submitted / active_pms.pms_individual_kpi_number * 100
        else:
            approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
    else:
        all_kpi = approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

    # Get team Leader
    user_team = request.user.staff_person.staff_team
    if user_team is not None:
        team_leader = staff.objects.filter(staff_head_team=user_team)
        if team_leader:
            team_leader = team_leader.get()
        else:
            team_leader = None
    else:
        team_leader = None

    context = {
        'my_kpi': all_kpi,
        'staff_n_kpi': staff_n_kpi,
        'team_members': team_members,
        'active_pms': active_pms,
        'approved1_kpi': approved1_kpi,
        'approved2_kpi': approved2_kpi,
        'pending_kpi': pending_kpi,
        'edit_kpi': edit_kpi,
        'rejected1_kpi': rejected1_kpi,
        'rejected2_kpi': rejected2_kpi,
        'total_submitted': total_submitted,
        'percent_submitted': percent_submitted,
        'total_pending': total_pending,
        'total_rejected': total_rejected,
        'team_leader': team_leader,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Kpi/trackkpi.html', context)


@login_required
def staff_trackkpi_staff(request, pk):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        kpi_approved_count = 0
        kpi_pending_count = 0
        kpi_zero_count = 0
        staff_n_kpi = None
        if team_members is not None:
            for member in team_members:
                staff_approved1_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                    individual_kpi_pms=active_pms,
                                                                    individual_kpi_status='Approved 1').count()
                staff_approved2_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                    individual_kpi_pms=active_pms,
                                                                    individual_kpi_status='Approved 2').count()
                staff_pending_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                  individual_kpi_pms=active_pms,
                                                                  individual_kpi_status='Pending').count()
                total_kpi = staff_approved1_kpi + staff_approved2_kpi + staff_pending_kpi

                staff_n_kpi = [staff_n_kpi,
                               [member.staff_person.id, member.staff_person.get_full_name, member.staff_person.email,
                                member.staff_Pf_Number, staff_approved1_kpi, staff_approved2_kpi, staff_pending_kpi,
                                total_kpi]]

                if staff_approved2_kpi > 0:
                    kpi_approved_count = + 1

                if staff_pending_kpi > 0:
                    kpi_pending_count = + 1

                if total_kpi < 1:
                    kpi_zero_count = + 1
        else:
            staff_n_kpi = None
    else:
        team_members = None

    no_of_bu = bu.objects.all().count()

    if active_pms is not None:
        all_kpi = individual_Kpi.objects.filter(individual_kpi_user=pk, individual_kpi_pms=active_pms)
        if all_kpi is not None:
            approved1_kpi = all_kpi.filter(individual_kpi_status='Approved 1')
            approved2_kpi = all_kpi.filter(individual_kpi_status='Approved 2')
            pending_kpi = all_kpi.filter(individual_kpi_status="Pending")
            edit_kpi = all_kpi.filter(individual_kpi_status="Edit")
            rejected1_kpi = all_kpi.filter(individual_kpi_status="Rejected 1")
            rejected2_kpi = all_kpi.filter(individual_kpi_status="Rejected 2")
            total_submitted = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + edit_kpi.count()
            total_pending = approved1_kpi.count() + pending_kpi.count()
            total_rejected = rejected1_kpi.count() + rejected2_kpi.count()
            percent_submitted = total_submitted / active_pms.pms_individual_kpi_number * 100
            required_kpi = active_pms.pms_individual_kpi_number
        else:
            approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
    else:
        all_kpi = approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

    # Get team Leader
    user_team = request.user.staff_person.staff_team
    if user_team is not None:
        team_leader = staff.objects.filter(staff_head_team=user_team)
        if team_leader:
            team_leader = team_leader.get()
        else:
            team_leader = None
    else:
        team_leader = None

    staffp = User.objects.filter(id=pk).get()

    context = {
        'staff': staffp,
        'my_kpi': all_kpi,
        'required_kpi': required_kpi,
        'staff_n_kpi': staff_n_kpi,
        'team_members': team_members,
        'active_pms': active_pms,
        'approved1_kpi': approved1_kpi,
        'approved2_kpi': approved2_kpi,
        'pending_kpi': pending_kpi,
        'edit_kpi': edit_kpi,
        'rejected1_kpi': rejected1_kpi,
        'rejected2_kpi': rejected2_kpi,
        'total_submitted': total_submitted,
        'percent_submitted': percent_submitted,
        'total_pending': total_pending,
        'total_rejected': total_rejected,
        'team_leader': team_leader,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Kpi/trackkpi_staff.html', context)


@login_required
def staff_trackkpi_staff_one(request, pk, kpi_id):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if active_pms is not None:
        all_kpi = individual_Kpi.objects.filter(individual_kpi_id=kpi_id)
    else:
        all_kpi = None

    staffp = User.objects.filter(id=pk).get()

    context = {
        'staff': staffp,
        'my_kpi': all_kpi,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'user_bu': user_bu,
        'no_of_bu': no_of_bu,
    }
    return render(request, 'Staff_Kpi/trackkpi_staff_one.html', context)


@login_required
def staff_kpiresults(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        kpi_approved_count = 0
        kpi_pending_count = 0
        kpi_zero_count = 0
        staff_n_kpi = None
        if team_members is not None:
            for member in team_members:
                staff_approved2_kpi = individual_Kpi.objects.filter(individual_kpi_user=member.id,
                                                                    individual_kpi_pms=active_pms,
                                                                    individual_kpi_status='Approved 2')
                staff_n_kpi = [staff_n_kpi,
                               [member.staff_person.id, member.staff_person.get_full_name, member.staff_person.email,
                                member.staff_Pf_Number, staff_approved2_kpi]]
        else:
            staff_n_kpi = None
    else:
        team_members = None

    no_of_bu = bu.objects.all().count()

    if active_pms is not None:
        all_kpi = individual_Kpi.objects.filter(individual_kpi_user=request.user, individual_kpi_pms=active_pms)
        if all_kpi is not None:
            approved1_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status='Approved 1')
            approved2_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status='Approved 2')
            pending_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Pending")
            edit_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Edit")
            rejected1_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Rejected 1")
            rejected2_kpi = all_kpi.filter(individual_kpi_user=request.user, individual_kpi_status="Rejected 2")
            total_submitted = approved1_kpi.count() + approved2_kpi.count() + pending_kpi.count() + edit_kpi.count()
            total_pending = approved1_kpi.count() + pending_kpi.count()
            total_rejected = rejected1_kpi.count() + rejected2_kpi.count()
            percent_submitted = total_submitted / active_pms.pms_individual_kpi_number * 100
        else:
            approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
    else:
        all_kpi = approved1_kpi = approved2_kpi = pending_kpi = edit_kpi = rejected1_kpi = rejected2_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

    # Get team Leader
    user_team = request.user.staff_person.staff_team
    if user_team is not None:
        team_leader = staff.objects.filter(staff_head_team=user_team)
        if team_leader:
            team_leader = team_leader.get()
        else:
            team_leader = None
    else:
        team_leader = None

    context = {
        'my_kpi': all_kpi,
        'staff_n_kpi': staff_n_kpi,
        'team_members': team_members,
        'active_pms': active_pms,
        'approved1_kpi': approved1_kpi,
        'approved2_kpi': approved2_kpi,
        'pending_kpi': pending_kpi,
        'edit_kpi': edit_kpi,
        'rejected1_kpi': rejected1_kpi,
        'rejected2_kpi': rejected2_kpi,
        'total_submitted': total_submitted,
        'percent_submitted': percent_submitted,
        'total_pending': total_pending,
        'total_rejected': total_rejected,
        'team_leader': team_leader,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Kpi/kpiresults.html', context)


# =====================================================================================================================
#                                                 BU KPI
# =====================================================================================================================
@login_required
def bu_Kpi(request):
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md is None:
        pass
    elif user_is_bu_head is not None:
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(bu_kpi_status='Approved')
                pending_kpi = all_kpi.filter(bu_kpi_status="Pending")
                edit_kpi = all_kpi.filter(bu_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(bu_kpi_status="Rejected")

                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.pms_individual_kpi_number * 100

            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,

        }
        return render(request, 'Bu_Kpi/bukpi.html', context)

    else:
        pass


@login_required
def bu_Submit_Kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is None:
        pass
    elif user_is_bu_head is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(bu_kpi_status='Approved')
                pending_kpi = all_kpi.filter(bu_kpi_status="Pending")
                edit_kpi = all_kpi.filter(bu_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(bu_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        if request.method == 'POST' and total_submitted < active_pms.bu_individual_kpi_number:
            form = submit_bu_kpi_form(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.bu_kpi_bu = user_is_bu_head
                post.bu_kpi_bu_user = request.user
                post.bu_kpi_pms_id = active_pms
                post.save()
                form = submit_bu_kpi_form()
                messages.success(request, 'KPI submission success')

                if team_leader is not None:
                    send_mail(
                        subject='KPI Submitted',
                        message='Dear ' + team_leader.staff_person.get_full_name() + ' '
                                + request.user.get_full_name() +
                                'Has just submitted a KPI for your approval',
                        recipient_list=[team_leader.staff_person.email, request.user.email],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )
                else:
                    send_mail(
                        subject='KPI Submitted',
                        message='Your KPI has been submitted successfully but i keep on failing contacting your '
                                'immediate supervisor.<br>Please raise the issue with HR for support',
                        recipient_list=[request.user.email, ],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )

                # return HttpResponseRedirect('')
                return HttpResponseRedirect(reverse("BU_Kpi_Submit"))
        else:
            form = submit_bu_kpi_form()

        context = {
            'form': form,
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Bu_Kpi/submitkpi.html', context)
    else:
        pass


@login_required
def bu_track_kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is None:
        pass
    elif user_is_bu_head is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(bu_kpi_status='Approved')
                pending_kpi = all_kpi.filter(bu_kpi_status="Pending")
                edit_kpi = all_kpi.filter(bu_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(bu_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Bu_Kpi/trackkpi.html', context)
    else:
        pass


@login_required
def bu_edit_kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is None:
        pass
    elif user_is_bu_head is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(bu_kpi_status='Approved')
                pending_kpi = all_kpi.filter(bu_kpi_status="Pending")
                edit_kpi = all_kpi.filter(bu_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(bu_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Bu_Kpi/editkpi.html', context)
    else:
        pass


@login_required
def bu_kpi_result(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is None:
        pass
    elif user_is_bu_head is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(bu_kpi_status='Approved')
                pending_kpi = all_kpi.filter(bu_kpi_status="Pending")
                edit_kpi = all_kpi.filter(bu_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(bu_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Bu_Kpi/kpiresults.html', context)
    else:
        pass


class BU_Kpi_Detail_View(generic.DetailView):
    model = bu_kpi
    template_name = 'Bu_Kpi/one_individual_kpi.html'

    def get_context_data(self, **kwargs):

        context = super(BU_Kpi_Detail_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
            context['user_is_md'] = self.request.user.staff_person.staff_md
            context['user_is_tl'] = self.request.user.staff_person.staff_head_team
            context['user_bu'] = self.request.user.staff_person.staff_bu

            if context['user_is_bu_head'] is not None:
                all_kpi = bu_kpi.objects.filter(bu_kpi_bu=context['user_is_bu_head'], bu_kpi_pms_id=active_pms)
                context['active_pms'] = active_pms
                context['approved_kpi'] = all_kpi.filter(bu_kpi_status='Approved')
                context['pending_kpi'] = all_kpi.filter(bu_kpi_status="Pending")
                context['edit_kpi'] = all_kpi.filter(bu_kpi_status="Edit")
                context['rejected_kpi'] = all_kpi.filter(bu_kpi_status="Rejected")
                context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + context[
                    'edit_kpi'].count()
                context['total_pending'] = context['pending_kpi'].count()
                context['total_rejected'] = context['rejected_kpi'].count()
                context['percent_submitted'] = context['total_submitted'] / context[
                    'active_pms'].bu_individual_kpi_number * 100

                # Get team Leader
                user_team = self.request.user.staff_person.staff_team
                return context


class BU_Edit_Kpi_View(UpdateView):
    model = bu_kpi
    form_class = edit_bu_kpi_form
    template_name = "Bu_Kpi/one_individual_kpi_edit.html"

    def form_valid(self, form):
        messages.success(self.request, "KPI Edited successfully")
        super().form_valid(form)
        return HttpResponseRedirect(reverse("BU_Kpi_Edit_One", kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, *args, **kwargs):
        kpi = get_object_or_404(bu_kpi, pk=self.kwargs['pk'])
        return kpi

    def get_success_url(self, *args, **kwargs):
        return reverse("BU_Kpi_Edit_One", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(BU_Edit_Kpi_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        # Check Level
        user_is_bu_head = self.request.user.staff_person.staff_head_bu
        user_is_md = self.request.user.staff_person.staff_md
        user_is_tl = self.request.user.staff_person.staff_head_team
        user_bu = self.request.user.staff_person.staff_bu

        no_of_bu = bu.objects.all().count()
        if user_is_md is None:
            pass
        elif user_is_bu_head is not None:

            # Active PMS
            active_pms = pms.objects.filter(pms_status='Active')
            active_pms = active_pms.get()

            if active_pms is not None:
                all_kpi = bu_kpi.objects.filter(bu_kpi_bu=user_is_bu_head, bu_kpi_pms_id=active_pms)

                if all_kpi is not None:
                    context['active_pms'] = active_pms
                    context['approved_kpi'] = all_kpi.filter(bu_kpi_status='Approved')
                    context['pending_kpi'] = all_kpi.filter(bu_kpi_status="Pending")
                    context['edit_kpi'] = all_kpi.filter(bu_kpi_status="Edit")
                    context['rejected_kpi'] = all_kpi.filter(bu_kpi_status="Rejected")
                    context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                                 context['edit_kpi'].count()
                    context['total_pending'] = context['pending_kpi'].count()
                    context['total_rejected'] = context['rejected_kpi'].count()
                    context['percent_submitted'] = context['total_submitted'] / context[
                        'active_pms'].pms_individual_kpi_number * 100
                    context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                    context['user_is_md'] = self.request.user.staff_person.staff_md
                    context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                    context['user_bu'] = self.request.user.staff_person.staff_bu
                    context['no_of_bu'] = bu.objects.all().count()

                    # Get team Leader
                    user_team = self.request.user.staff_person.staff_team
                    return context


class BU_Kpi_Result_Update(UpdateView):
    model = bu_kpi
    form_class = BU_Kpi_Results_Form
    template_name = "Bu_Kpi/one_individual_kpi_update.html"

    def form_valid(self, form):
        if super().form_valid(form):
            messages.success(self.request, "KPI Edited successfully")
        return HttpResponseRedirect(reverse("BU_Kpi_Result_Update", kwargs={'pk': self.kwargs['pk']}))

    def get_queryset(self):
        return bu_kpi.objects.filter(bu_kpi_id=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        return reverse("BU_Kpi_Result_Update", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(BU_Kpi_Result_Update, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        all_kpi = individual_Kpi.objects.filter(individual_kpi_user=self.request.user, individual_kpi_pms=active_pms)

        context['my_kpi'] = individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                          individual_kpi_pms=active_pms)

        context['active_pms'] = active_pms
        context['approved1_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                  individual_kpi_status='Approved 1')
        context['approved2_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                  individual_kpi_status='Approved 2')
        context['pending_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user, individual_kpi_status="Pending")
        context['edit_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user, individual_kpi_status="Edit")
        context['rejected1_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                  individual_kpi_status="Rejected 1")
        context['rejected2_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                  individual_kpi_status="Rejected 2")
        context['total_submitted'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + context[
            'pending_kpi'].count() + context['edit_kpi'].count()
        context['total_pending'] = context['approved1_kpi'].count() + context['pending_kpi'].count()
        context['total_rejected'] = context['rejected1_kpi'].count() + context['rejected2_kpi'].count()
        context['percent_submitted'] = context['total_submitted'] / context[
            'active_pms'].pms_individual_kpi_number * 100
        context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
        context['user_is_md'] = self.request.user.staff_person.staff_md
        context['user_is_tl'] = self.request.user.staff_person.staff_head_team
        context['user_bu'] = self.request.user.staff_person.staff_bu
        context['no_of_bu'] = bu.objects.all().count()

        # Get team Leader
        user_team = self.request.user.staff_person.staff_team
        return context


# =====================================================================================================================
#                                                 Company KPI
# =====================================================================================================================
@login_required
def company_Kpi(request):
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md is not None:
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(company_kpi_status='Approved')
                pending_kpi = all_kpi.filter(company_kpi_status="Pending")
                edit_kpi = all_kpi.filter(company_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(company_kpi_status="Rejected")

                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.pms_individual_kpi_number * 100

            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,

        }
        return render(request, 'Company_Kpi/companykpi.html', context)

    else:
        pass


@login_required
def company_Submit_Kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is not None:
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(company_kpi_status='Approved')
                pending_kpi = all_kpi.filter(company_kpi_status="Pending")
                edit_kpi = all_kpi.filter(company_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(company_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        if request.method == 'POST' and total_submitted < active_pms.bu_individual_kpi_number:
            form = submit_company_kpi_form(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.company_kpi_user = request.user
                post.company_kpi_pms_id = active_pms
                post.save()
                form = submit_company_kpi_form()
                messages.success(request, 'KPI submission success')

                if team_leader is not None:
                    send_mail(
                        subject='KPI Submitted',
                        message='Dear ' + team_leader.staff_person.get_full_name() + ' '
                                + request.user.get_full_name() +
                                'Has just submitted a KPI for your approval',
                        recipient_list=[team_leader.staff_person.email, request.user.email],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )
                else:
                    send_mail(
                        subject='KPI Submitted',
                        message='Your KPI has been submitted successfully but i keep on failing contacting your '
                                'immediate supervisor.<br>Please raise the issue with HR for support',
                        recipient_list=[request.user.email, ],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )

                # return HttpResponseRedirect('')
                return HttpResponseRedirect(reverse("Company_Kpi_Submit"))
        else:
            form = submit_company_kpi_form()

        context = {
            'form': form,
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Company_Kpi/submitkpi.html', context)
    else:
        pass


@login_required
def company_track_kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(company_kpi_status='Approved')
                pending_kpi = all_kpi.filter(company_kpi_status="Pending")
                edit_kpi = all_kpi.filter(company_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(company_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Company_Kpi/trackkpi.html', context)
    else:
        pass


@login_required
def company_edit_kpi(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is not None:
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(company_kpi_status='Approved')
                pending_kpi = all_kpi.filter(company_kpi_status="Pending")
                edit_kpi = all_kpi.filter(company_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(company_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Company_Kpi/editkpi.html', context)
    else:
        pass


@login_required
def company_kpi_result(request):
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    if user_is_md is not None:

        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                approved_kpi = all_kpi.filter(company_kpi_status='Approved')
                pending_kpi = all_kpi.filter(company_kpi_status="Pending")
                edit_kpi = all_kpi.filter(company_kpi_status="Edit")
                rejected_kpi = all_kpi.filter(company_kpi_status="Rejected")
                total_submitted = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                total_pending = pending_kpi.count()
                total_rejected = rejected_kpi.count()
                percent_submitted = total_submitted / active_pms.bu_individual_kpi_number * 100
            else:
                approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            all_kpi = approved_kpi = pending_kpi = edit_kpi = rejected_kpi = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        context = {
            'my_kpi': all_kpi,
            'active_pms': active_pms,
            'approved_kpi': approved_kpi,
            'pending_kpi': pending_kpi,
            'edit_kpi': edit_kpi,
            'rejected_kpi': rejected_kpi,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'team_leader': team_leader,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Company_Kpi/kpiresults.html', context)
    else:
        pass


class Company_Kpi_Detail_View(generic.DetailView):
    model = company_kpi
    template_name = 'Company_Kpi/one_individual_kpi.html'

    def get_context_data(self, **kwargs):

        context = super(Company_Kpi_Detail_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
            context['user_is_md'] = self.request.user.staff_person.staff_md
            context['user_is_tl'] = self.request.user.staff_person.staff_head_team
            context['user_bu'] = self.request.user.staff_person.staff_bu

            if context['user_is_md'] is not None:
                all_kpi = bu_kpi.objects.filter(bu_kpi_bu=context['user_is_bu_head'], bu_kpi_pms_id=active_pms)
                context['active_pms'] = active_pms
                context['approved_kpi'] = all_kpi.filter(bu_kpi_status='Approved')
                context['pending_kpi'] = all_kpi.filter(bu_kpi_status="Pending")
                context['edit_kpi'] = all_kpi.filter(bu_kpi_status="Edit")
                context['rejected_kpi'] = all_kpi.filter(bu_kpi_status="Rejected")
                context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + context[
                    'edit_kpi'].count()
                context['total_pending'] = context['pending_kpi'].count()
                context['total_rejected'] = context['rejected_kpi'].count()
                context['percent_submitted'] = context['total_submitted'] / context[
                    'active_pms'].bu_individual_kpi_number * 100
                context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                context['user_is_md'] = self.request.user.staff_person.staff_md
                context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                context['user_bu'] = self.request.user.staff_person.staff_bu
                context['no_of_bu'] = bu.objects.all().count()

                # Get team Leader
                user_team = self.request.user.staff_person.staff_team
                return context
            else:
                pass


class Company_Edit_Kpi_View(UpdateView):
    model = company_kpi
    form_class = edit_company_kpi_form
    template_name = "Company_Kpi/one_individual_kpi_edit.html"

    def form_valid(self, form):
        messages.success(self.request, "KPI Edited successfully")
        super().form_valid(form)
        return HttpResponseRedirect(reverse("Company_Kpi_Edit_One", kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, *args, **kwargs):
        kpi = get_object_or_404(company_kpi, pk=self.kwargs['pk'])
        return kpi

    def get_success_url(self, *args, **kwargs):
        return reverse("Company_Kpi_Edit_One", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(Company_Edit_Kpi_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        # Check Level
        user_is_bu_head = self.request.user.staff_person.staff_head_bu
        user_is_md = self.request.user.staff_person.staff_md
        user_is_tl = self.request.user.staff_person.staff_head_team
        user_bu = self.request.user.staff_person.staff_bu

        no_of_bu = bu.objects.all().count()
        if user_is_md is not None:

            # Active PMS
            active_pms = pms.objects.filter(pms_status='Active')
            active_pms = active_pms.get()

            if active_pms is not None:
                all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

                if all_kpi is not None:
                    context['my_kpi'] = all_kpi
                    context['active_pms'] = active_pms
                    context['approved_kpi'] = all_kpi.filter(company_kpi_status='Approved')
                    context['pending_kpi'] = all_kpi.filter(company_kpi_status="Pending")
                    context['edit_kpi'] = all_kpi.filter(company_kpi_status="Edit")
                    context['rejected_kpi'] = all_kpi.filter(company_kpi_status="Rejected")
                    context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                                 context['edit_kpi'].count()
                    context['total_pending'] = context['pending_kpi'].count()
                    context['total_rejected'] = context['rejected_kpi'].count()
                    context['percent_submitted'] = context['total_submitted'] / context[
                        'active_pms'].pms_individual_kpi_number * 100
                    context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                    context['user_is_md'] = self.request.user.staff_person.staff_md
                    context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                    context['user_bu'] = self.request.user.staff_person.staff_bu
                    context['no_of_bu'] = bu.objects.all().count()

                    # Get team Leader
                    user_team = self.request.user.staff_person.staff_team
                    return context


class Company_Kpi_Result_Update(UpdateView):
    model = company_kpi
    form_class = Company_Kpi_Results_Form
    template_name = "Company_Kpi/one_individual_kpi_update.html"

    def form_valid(self, form):

        if super().form_valid(form):
            messages.success(self.request, "KPI Edited successfully")
        return HttpResponseRedirect(reverse("Company_Kpi_Result_Update", kwargs={'pk': self.kwargs['pk']}))

    def get_queryset(self):
        return company_kpi.objects.filter(company_kpi_id=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        return reverse("BU_Kpi_Result_Update", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(Company_Kpi_Result_Update, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()
        if active_pms is not None:
            all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

            if all_kpi is not None:
                context['active_pms'] = active_pms
                context['approved_kpi'] = all_kpi.filter(company_kpi_status='Approved')
                context['pending_kpi'] = all_kpi.filter(company_kpi_status="Pending")
                context['edit_kpi'] = all_kpi.filter(company_kpi_status="Edit")
                context['rejected_kpi'] = all_kpi.filter(company_kpi_status="Rejected")
                context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + context[
                    'edit_kpi'].count()
                context['total_pending'] = context['pending_kpi'].count()
                context['total_rejected'] = context['rejected_kpi'].count()
                context['percent_submitted'] = context['total_submitted'] / context[
                    'active_pms'].pms_individual_kpi_number * 100
                context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                context['user_is_md'] = self.request.user.staff_person.staff_md
                context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                context['user_bu'] = self.request.user.staff_person.staff_bu
                context['no_of_bu'] = bu.objects.all().count()

                # Get team Leader
                user_team = self.request.user.staff_person.staff_team
                return context


# =====================================================================================================================
#                                                 My Checkin
# =====================================================================================================================


@login_required
def my_check_in(request):
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md == 'No':
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_ci = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=request.user)

            if all_ci is not None:
                confirmed_ci = all_ci.filter(checkIn_status='Confirmed')
                pending_ci = all_ci.filter(checkIn_status="Pending")
                rejected_ci = all_ci.filter(checkIn_status="Rejected")
                submitted_ci = all_ci.exclude(checkIn_status="Rejected")

                total_submitted = confirmed_ci.count() + pending_ci.count()
                total_pending = pending_ci.count()
                total_rejected = rejected_ci.count()
                percent_submitted = total_submitted / active_pms.checkin_number * 100
                ci_months = []
                for ci in submitted_ci:
                    ci_months.append(ci.checkIn_month)

            else:
                ci_months = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            ci_months = all_ci = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None

        context = {
            'my_ci': all_ci,
            'ci_months': ci_months,
            'active_pms': active_pms,
            'confirmed_ci': confirmed_ci,
            'pending_ci': pending_ci,
            'rejected_ci': rejected_ci,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Check-In/checkin.html', context)

    else:
        pass


@login_required
def checkin_Submit_Kpi(request):
    # Check Level
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md == 'No':
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_ci = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=request.user)

            if all_ci is not None:
                confirmed_ci = all_ci.filter(checkIn_status='Confirmed')
                pending_ci = all_ci.filter(checkIn_status="Pending")
                rejected_ci = all_ci.filter(checkIn_status="Rejected")
                submitted_ci = all_ci.exclude(checkIn_status="Rejected")

                total_submitted = confirmed_ci.count() + pending_ci.count()
                total_pending = pending_ci.count()
                total_rejected = rejected_ci.count()
                percent_submitted = total_submitted / active_pms.checkin_number * 100
                ci_months = []
                for ci in submitted_ci:
                    ci_months.append(ci.checkIn_month)

            else:
                ci_months = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            ci_months = all_ci = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None

        # Get team Leader
        user_team = request.user.staff_person.staff_team
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                team_leader = team_leader.get()
            else:
                team_leader = None
        else:
            team_leader = None

        if request.method == 'POST':
            form = submit_Check_In_Form(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.checkIn_pms = active_pms
                post.checkIn_staff = request.user
                if team_leader is not None:
                    post.checkIn_team_leader = team_leader.staff_person
                post.checkIn_submit_date = datetime.datetime.now()
                post.checkIn_month = datetime.datetime.strftime(datetime.datetime.now(), '%B')
                post.company_kpi_pms_id = active_pms
                post.save()
                form = submit_Check_In_Form()
                messages.success(request, 'KPI submission success')

                if team_leader is not None:
                    send_mail(
                        subject='Check-In Submitted',
                        message='Dear ' + team_leader.staff_person.get_full_name() + ' '
                                + request.user.get_full_name() +
                                'Has just submitted a checkin for your approval',
                        recipient_list=[team_leader.staff_person.email, request.user.email],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )
                else:
                    send_mail(
                        subject='KPI Submitted',
                        message='Your KPI has been submitted successfully but i keep on failing contacting your '
                                'immediate supervisor.<br>Please raise the issue with HR for support',
                        recipient_list=[request.user.email, ],
                        fail_silently=False,
                        from_email='pms_notifier@c-k.co.ke',
                    )

                # return HttpResponseRedirect('')
                return HttpResponseRedirect(reverse("Check-In_Kpi_Submit"))
        else:
            form = submit_Check_In_Form()

        context = {
            'form': form,
            'month': datetime.datetime.strftime(datetime.datetime.now(), '%B'),
            'my_ci': all_ci,
            'ci_months': ci_months,
            'active_pms': active_pms,
            'confirmed_ci': confirmed_ci,
            'pending_ci': pending_ci,
            'rejected_ci': rejected_ci,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Check-In/submitci.html', context)
    else:
        pass


@login_required
def track_check_in(request):
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md == 'No':
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_ci = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=request.user)
            if all_ci is not None:
                confirmed_ci = all_ci.filter(checkIn_status='Confirmed')
                pending_ci = all_ci.filter(checkIn_status="Pending")
                rejected_ci = all_ci.filter(checkIn_status="Rejected")
                submitted_ci = all_ci.exclude(checkIn_status="Rejected")

                total_submitted = confirmed_ci.count() + pending_ci.count()
                total_pending = pending_ci.count()
                total_rejected = rejected_ci.count()
                percent_submitted = total_submitted / active_pms.checkin_number * 100
                ci_months = []
                for ci in submitted_ci:
                    ci_months.append(ci.checkIn_month)

            else:
                ci_months = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            ci_months = all_ci = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None

        context = {
            'my_ci': all_ci,
            'ci_months': ci_months,
            'active_pms': active_pms,
            'confirmed_ci': confirmed_ci,
            'pending_ci': pending_ci,
            'rejected_ci': rejected_ci,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Check-In/trackci.html', context)

    else:
        pass


@login_required
def check_In_edit(request):
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu

    no_of_bu = bu.objects.all().count()
    # Check Level
    user_is_bu_head = request.user.staff_person.staff_head_bu
    if user_is_md == 'No':
        # Active PMS
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_ci = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=request.user)

            if all_ci is not None:
                confirmed_ci = all_ci.filter(checkIn_status='Confirmed')
                pending_ci = all_ci.filter(checkIn_status="Pending")
                rejected_ci = all_ci.filter(checkIn_status="Rejected")
                submitted_ci = all_ci.exclude(checkIn_status="Rejected")

                total_submitted = confirmed_ci.count() + pending_ci.count()
                total_pending = pending_ci.count()
                total_rejected = rejected_ci.count()
                percent_submitted = total_submitted / active_pms.checkin_number * 100
                ci_months = []
                for ci in submitted_ci:
                    ci_months.append(ci.checkIn_month)

            else:
                ci_months = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None
        else:
            ci_months = all_ci = confirmed_ci = pending_ci = rejected_ci = total_submitted = total_pending = total_rejected = percent_submitted = None

        context = {
            'my_ci': all_ci,
            'ci_months': ci_months,
            'active_pms': active_pms,
            'confirmed_ci': confirmed_ci,
            'pending_ci': pending_ci,
            'rejected_ci': rejected_ci,
            'total_submitted': total_submitted,
            'percent_submitted': percent_submitted,
            'total_pending': total_pending,
            'total_rejected': total_rejected,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Check-In/editci.html', context)

    else:
        pass


class Check_In_Detail_View(generic.DetailView):
    model = checkIn
    template_name = 'Check-In/one_individual_ci.html'
    context_object_name = 'cis'

    def get_queryset(self):
        return checkIn.objects.filter(checkIn_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(Check_In_Detail_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        # Check Level
        user_is_bu_head = self.request.user.staff_person.staff_head_bu
        user_is_md = self.request.user.staff_person.staff_md
        user_is_tl = self.request.user.staff_person.staff_head_team
        user_bu = self.request.user.staff_person.staff_bu

        no_of_bu = bu.objects.all().count()
        if user_is_md == 'No':

            # Active PMS
            active_pms = pms.objects.filter(pms_status='Active')
            active_pms = active_pms.get()

            if active_pms is not None:
                all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

                if all_kpi is not None:
                    context['my_kpi'] = all_kpi
                    context['active_pms'] = active_pms
                    context['approved_kpi'] = all_kpi.filter(company_kpi_status='Approved')
                    context['pending_kpi'] = all_kpi.filter(company_kpi_status="Pending")
                    context['edit_kpi'] = all_kpi.filter(company_kpi_status="Edit")
                    context['rejected_kpi'] = all_kpi.filter(company_kpi_status="Rejected")
                    context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                                 context['edit_kpi'].count()
                    context['total_pending'] = context['pending_kpi'].count()
                    context['total_rejected'] = context['rejected_kpi'].count()
                    context['percent_submitted'] = context['total_submitted'] / context[
                        'active_pms'].pms_individual_kpi_number * 100
                    context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                    context['user_is_md'] = self.request.user.staff_person.staff_md
                    context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                    context['user_bu'] = self.request.user.staff_person.staff_bu
                    context['no_of_bu'] = bu.objects.all().count()

                    # Get team Leader
                    user_team = self.request.user.staff_person.staff_team
                    return context


class Chech_In_Edit_View(UpdateView):
    model = checkIn
    form_class = edit_Check_In_Form
    context_object_name = 'cis'
    template_name = "Check-In/one_individual_ci_edit.html"

    def form_valid(self, form):
        messages.success(self.request, "KPI Edited successfully")
        super().form_valid(form)
        return HttpResponseRedirect(reverse("Check-In_Edit_One", kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, *args, **kwargs):
        kpi = get_object_or_404(checkIn, pk=self.kwargs['pk'])
        return kpi

    def get_success_url(self, *args, **kwargs):
        return reverse("Check-In_Edit_One", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(Chech_In_Edit_View, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        # Check Level
        user_is_bu_head = self.request.user.staff_person.staff_head_bu
        user_is_md = self.request.user.staff_person.staff_md
        user_is_tl = self.request.user.staff_person.staff_head_team
        user_bu = self.request.user.staff_person.staff_bu

        no_of_bu = bu.objects.all().count()
        if user_is_md is not None:

            # Active PMS
            active_pms = pms.objects.filter(pms_status='Active')
            active_pms = active_pms.get()

            if active_pms is not None:
                all_kpi = company_kpi.objects.filter(company_kpi_pms_id=active_pms)

                if all_kpi is not None:
                    context['my_kpi'] = all_kpi
                    context['active_pms'] = active_pms
                    context['approved_kpi'] = all_kpi.filter(company_kpi_status='Approved')
                    context['pending_kpi'] = all_kpi.filter(company_kpi_status="Pending")
                    context['edit_kpi'] = all_kpi.filter(company_kpi_status="Edit")
                    context['rejected_kpi'] = all_kpi.filter(company_kpi_status="Rejected")
                    context['total_submitted'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                                 context['edit_kpi'].count()
                    context['total_pending'] = context['pending_kpi'].count()
                    context['total_rejected'] = context['rejected_kpi'].count()
                    context['percent_submitted'] = context['total_submitted'] / context[
                        'active_pms'].pms_individual_kpi_number * 100
                    context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                    context['user_is_md'] = self.request.user.staff_person.staff_md
                    context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                    context['user_bu'] = self.request.user.staff_person.staff_bu
                    context['no_of_bu'] = bu.objects.all().count()

                    # Get team Leader
                    user_team = self.request.user.staff_person.staff_team
                    return context


# ======================================================================================================================
#                                           STAFF CHECKIN
# ======================================================================================================================


@login_required
def staff_check_in(request):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_n_ci = None
    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        ci_approved_count = 0
        ci_pending_count = 0
        ci_zero_count = 0
        if team_members is not None:
            for member in team_members:
                staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Confirmed').count()
                staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                          checkIn_status='Pending').count()
                staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Rejected').count()

                total_ci = staff_approved_ci + staff_pending_ci

                staff_n_ci = [staff_n_ci,
                              [member.staff_person.get_full_name, member.staff_person.email, member.staff_Pf_Number,
                               staff_approved_ci, staff_pending_ci, staff_rejected_ci, total_ci]]

                if staff_approved_ci > 0:
                    ci_approved_count = + 1

                if staff_pending_ci > 0:
                    ci_pending_count = + 1

                if total_ci < 1:
                    ci_zero_count = + 1
        else:
            staff_n_ci = None
    else:
        team_members = None

    context = {
        'staff_n_ci': list(chain(staff_n_ci)),
        'team_members': team_members,
        'ci_approved_count': ci_approved_count,
        'ci_pending_count': ci_pending_count,
        'ci_zero_count': ci_zero_count,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Ci/staffci.html', context)


@login_required
def staff_check_in_staff(request, pk):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_u = User.objects.get(id=pk)
    staff_p = staff.objects.filter(staff_person=staff_u)
    staff_pending_ci = checkIn.objects.filter(checkIn_staff=pk, checkIn_pms_id=active_pms, checkIn_status='Pending')

    context = {
        'staff_u': staff_u,
        'staff_pending_ci': staff_pending_ci,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }

    return render(request, 'Staff_Ci/staffcistaff.html', context)


@login_required
def staff_individual_check_in(request, pk, ci_id):
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team

    staff_u = User.objects.get(id=pk)
    ci = checkIn.objects.get(checkIn_id=ci_id)
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if active_pms is not None:
        all_ci = checkIn.objects.filter(checkIn_id=ci_id, checkIn_pms=active_pms).get()

    context = {
        'all_ci': all_ci,
        'staff_u': staff_u,
        'ci': ci,
    }
    return render(request, 'Staff_Ci/one_individual_approve_ci.html', context)


@login_required
def approve_check_in(request):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_n_ci = None
    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        ci_approved_count = 0
        ci_pending_count = 0
        ci_zero_count = 0
        if team_members is not None:
            for member in team_members:
                staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Confirmed').count()
                staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                          checkIn_status='Pending').count()
                staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Rejected').count()

                total_ci = staff_approved_ci + staff_pending_ci

                staff_n_ci = [staff_n_ci, [member, staff_approved_ci, staff_pending_ci, staff_rejected_ci, total_ci]]

                if staff_approved_ci > 0:
                    ci_approved_count = + 1

                if staff_pending_ci > 0:
                    ci_pending_count = + 1

                if total_ci < 1:
                    ci_zero_count = + 1
        else:
            staff_n_ci = None
    else:
        team_members = None

    context = {
        'staff_n_ci': staff_n_ci,
        'team_members': team_members,
        'ci_approved_count': ci_approved_count,
        'ci_pending_count': ci_pending_count,
        'ci_zero_count': ci_zero_count,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Ci/approveci.html', context)


class approve_check_in_view(UpdateView):
    model = individual_Kpi
    form_class = IndividualKpiUpdateForm
    template_name = "Staff_Kpi/one_individual_approve_kpi.html"

    def form_valid(self, form):
        messages.success(self.request, "KPI Edited successfully")
        super().form_valid(form)
        return HttpResponseRedirect(reverse("Individual_Kpi-Edit_One", kwargs={'pk': self.kwargs['pk']}))

    def get_object(self, *args, **kwargs):
        active_pms = pms.objects.filter(pms_status='Active').get()
        kpi = individual_Kpi.objects.filter(individual_kpi_user=self.kwargs['pk'],
                                            individual_kpi_pms=active_pms).first()
        return kpi

    def get_success_url(self, *args, **kwargs):
        return reverse("Individual_Kpi-Edit_One", kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(ApproveKpiView, self).get_context_data(**kwargs)
        active_pms = pms.objects.filter(pms_status='Active')
        active_pms = active_pms.get()

        if active_pms is not None:
            all_kpi = individual_Kpi.objects.filter(individual_kpi_user=self.kwargs['pk'],
                                                    individual_kpi_pms=active_pms)
            context['staff'] = User.objects.filter(id=self.kwargs['pk']).get()
            if all_kpi is not None:
                context['active_pms'] = active_pms
                context['my_kpi'] = all_kpi
                context['approved1_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                          individual_kpi_status='Approved 1')
                context['approved2_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                          individual_kpi_status='Approved 2')
                context['pending_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                        individual_kpi_status="Pending")
                context['edit_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                     individual_kpi_status="Edit")
                context['rejected1_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                          individual_kpi_status="Rejected 1")
                context['rejected2_kpi'] = all_kpi.filter(individual_kpi_user=self.request.user,
                                                          individual_kpi_status="Rejected 2")
                context['total_submitted'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                             context['pending_kpi'].count() + context['edit_kpi'].count()
                context['total_pending'] = context['approved1_kpi'].count() + context['pending_kpi'].count()
                context['total_rejected'] = context['rejected1_kpi'].count() + context['rejected2_kpi'].count()
                context['percent_submitted'] = context['total_submitted'] / context[
                    'active_pms'].pms_individual_kpi_number * 100
                context['user_is_bu_head'] = self.request.user.staff_person.staff_head_bu
                context['user_is_md'] = self.request.user.staff_person.staff_md
                context['user_is_tl'] = self.request.user.staff_person.staff_head_team
                context['user_bu'] = self.request.user.staff_person.staff_bu
                context['no_of_bu'] = bu.objects.all().count()
        # Get team Leader
        user_team = self.request.user.staff_person.staff_team
        return context


@login_required
def approve_individual_check_in(request, pk, ci_id):
    checkIn.objects.filter(checkIn_id=ci_id).update(checkIn_status=checkIn.status[1][0],
                                                    checkIn_team_leader=request.user.id,
                                                    checkIn_confirm_date=datetime.datetime.now())

    return HttpResponseRedirect(reverse("Staff_Approve_CI_list", kwargs={'pk': pk}))


@login_required
def reject_individual_check_in(request, pk, ci_id):
    checkIn.objects.filter(checkIn_id=ci_id).update(checkIn_status=checkIn.status[2][0],
                                                    checkIn_team_leader=request.user.id,
                                                    checkIn_confirm_date=datetime.datetime.now())

    return HttpResponseRedirect(reverse("Staff_Approve_CI_list", kwargs={'pk': pk}))


@login_required
def staff_track_check_in(request):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_n_ci = None
    if user_is_tl is not None:
        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
        ci_approved_count = 0
        ci_pending_count = 0
        ci_zero_count = 0
        if team_members is not None:
            for member in team_members:
                staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Confirmed').count()
                staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                          checkIn_status='Pending').count()
                staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                           checkIn_status='Rejected').count()

                total_ci = staff_approved_ci + staff_pending_ci

                staff_n_ci = [staff_n_ci,
                              [member.staff_person.id, member.staff_person.get_full_name, member.staff_person.email,
                               member.staff_Pf_Number,
                               staff_approved_ci, staff_pending_ci, staff_rejected_ci, total_ci]]

                if staff_approved_ci > 0:
                    ci_approved_count = + 1

                if staff_pending_ci > 0:
                    ci_pending_count = + 1

                if total_ci < 1:
                    ci_zero_count = + 1
        else:
            staff_n_ci = None
    else:
        team_members = None

    context = {
        'staff_n_ci': list(chain(staff_n_ci)),
        'team_members': team_members,
        'ci_approved_count': ci_approved_count,
        'ci_pending_count': ci_pending_count,
        'ci_zero_count': ci_zero_count,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Ci/trackci.html', context)


@login_required
def staff_track_check_in_staff(request, pk):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_u = User.objects.get(id=pk)
    staff_p = staff.objects.filter(staff_person=staff_u)
    staff_ci = checkIn.objects.filter(checkIn_staff=pk, checkIn_pms_id=active_pms)

    context = {
        'staff_u': staff_u,
        'staff_ci': staff_ci,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }

    return render(request, 'Staff_Ci/trackci_staff.html', context)


@login_required
def staff_track_check_in_staff_one(request, pk, ci_id):
    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_u = User.objects.get(id=pk)
    ci = checkIn.objects.get(checkIn_id=ci_id)
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    if active_pms is not None:
        all_ci = checkIn.objects.filter(checkIn_id=ci_id, checkIn_pms=active_pms).get()

    context = {
        'all_ci': all_ci,
        'staff_u': staff_u,
        'ci': ci,
        'user_is_md': user_is_md,
        'user_is_bu_head': user_is_bu_head,
        'user_is_tl': user_is_tl,
        'no_of_bu': no_of_bu,
        'user_bu': user_bu,
    }
    return render(request, 'Staff_Ci/trackci_staff_one.html', context)


# ======================================================================================================================
#                                           ASSESSMENT
# ======================================================================================================================


@login_required
def assessment(request):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    if active_pms is not None:
        evaluations = evaluation.objects.filter(evaluation_pms=active_pms)
        running_evaluations = evaluation.objects.filter(evaluation_pms=active_pms,
                                                        evaluation_start_date__lte=datetime.date.today(),
                                                        evaluation_end_date__gte=datetime.date.today())
        future_evaluations = evaluation.objects.filter(evaluation_pms=active_pms,
                                                       evaluation_start_date__gt=datetime.date.today(), )
        completed_evaluations = evaluation.objects.filter(evaluation_pms=active_pms,
                                                          evaluation_end_date__lt=datetime.date.today())

        if evaluations is not None:
            evals = []
            for e in evaluations:
                # TL evaluates Staff
                s_tl = "N/A"
                tl_s = "N/A"
                if e.evaluation_start_date <= datetime.date.today() and e.evaluation_end_date >= datetime.date.today():
                    active = True
                else:
                    active = False
                if user_is_tl is not None:
                    if user_is_md == "Yes":
                        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
                        staff_ev_count = 0
                        if team_members.count() > 1:
                            for mem in team_members:
                                if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                          done_staff=mem.staff_person.id,
                                                                          done_team_leader=request.user) is not None:
                                    staff_ev_count = staff_ev_count + 1

                        tl_s = str(staff_ev_count) + "/" + str(team_members.count())

                    else:
                        team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
                        staff_ev_count = 0
                        if team_members.count() > 1:
                            for mem in team_members:
                                if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                          done_staff=mem.staff_person.id,
                                                                          done_team_leader=request.user) is not None:
                                    staff_ev_count = staff_ev_count + 1
                else:
                    ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                     done_staff=request.user)
                    if ev_done:
                        s_tl = "Done"
                    else:
                        s_tl = "Not done"

                evals.append(
                    [e.evaluation_id, e.evaluation_name, e.evaluation_start_date, e.evaluation_end_date, s_tl, tl_s,
                     active])

        context = {
            'evals': evals,
            'active_pms': active_pms,
            'running_evaluations': running_evaluations,
            'future_evaluations': future_evaluations,
            'completed_evaluations': completed_evaluations,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
    return render(request, 'Assessment/assessment.html', context)


@login_required
def assessment_view(request, as_id):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()
    user_team = request.user.staff_person.staff_team

    team_leader = None

    if user_team is not None:
        team_leader = staff.objects.filter(staff_head_team=user_team)
        if team_leader is not None:
            team_leader = team_leader.get()

    if active_pms is not None:
        e = evaluation.objects.filter(evaluation_id=as_id).get()

        if e is not None:
            evals = None

            # TL evaluates Staff
            s_tl = "N/A"
            tl_s = "N/A"
            if e.evaluation_start_date <= datetime.date.today() and e.evaluation_end_date >= datetime.date.today():
                active = True
            else:
                active = False
            if user_is_tl is not None:
                if user_is_md == "Yes":
                    team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
                    staff_ev_count = 0
                    if team_members.count() > 1:
                        for mem in team_members:
                            if done_tl_evaluates_staff.objects.filter(done_evaluation=e, done_staff=mem.staff_person,
                                                                      done_team_leader=request.user) is not None:
                                staff_ev_count = staff_ev_count + 1

                    tl_s = str(staff_ev_count) + "/" + str(team_members.count())

                else:
                    team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
                    staff_ev_count = 0
                    if team_members.count() > 1:
                        for mem in team_members:
                            if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                      done_staff=mem.staff_person.id,
                                                                      done_team_leader=request.user) is not None:
                                staff_ev_count = staff_ev_count + 1
            else:
                ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                 done_staff=request.user,
                                                                 done_team_leader=team_leader.staff_person)
                if ev_done.__len__() > 0:
                    s_tl = "Done"
                else:
                    s_tl = "Not done"

            evals = [e.evaluation_id, e.evaluation_name, e.evaluation_start_date, e.evaluation_end_date, s_tl, tl_s,
                     active]

        context = {
            'evals': evals,
            'team_leader': team_leader,
            'active_pms': active_pms,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
    return render(request, 'Assessment/assessment_list.html', context)


@login_required
def assessment_s_tl(request, as_id):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()
    user_team = request.user.staff_person.staff_team

    team_leader = staff.objects.filter(staff_head_team=user_team)

    if active_pms is not None:
        e = evaluation.objects.filter(evaluation_id=as_id).get()

        if e is not None:
            questions = question_staff_evaluate_tl(question_evaluation=e)

            context = {
                'team_leader': team_leader,
                'questions': questions,
                'active_pms': active_pms,
                'user_is_md': user_is_md,
                'user_is_bu_head': user_is_bu_head,
                'user_is_tl': user_is_tl,
                'no_of_bu': no_of_bu,
                'user_bu': user_bu,
            }
            return render(request, 'Assessment/assessment_s_tl.html', context)


@login_required
def assessment_s_tl_one(request, as_id, tl_id):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    team_leader = User.objects.get(id=tl_id)

    if active_pms is not None:
        e = evaluation.objects.filter(evaluation_id=as_id).get()

        if e is not None:
            ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e, done_staff=request.user,
                                                             done_team_leader=team_leader)
            questions = question_staff_evaluate_tl.objects.filter(question_evaluation_id=e)
            default_data = {'done_evaluation': e, 'done_staff': request.user.id, 'done_team_leader': team_leader, }
            if questions is not None:
                if questions:
                    count = 1
                    for question in questions:
                        done = 'done_q' + str(count)
                        default_data[done] = question
                        count = count + 1

                if request.method == 'POST':
                    form = asssessment_s_tl_Form(request.POST)

                    if form.is_valid():
                        post = form.save(commit=False)
                        post.save()
                        form = asssessment_s_tl_Form(default_data)
                        messages.success(request, 'Assessment done')

                        # return HttpResponseRedirect('')
                        return HttpResponseRedirect(reverse("Assessment_View", kwargs={'as_id': as_id}))
                else:
                    form = asssessment_s_tl_Form(default_data)

                form = asssessment_s_tl_Form(default_data)


        else:
            questions = None
            form = None

        context = {
            'e': e,
            'ev_done': ev_done,
            'form': form,
            'team_leader': team_leader,
            'questions': questions,
            'active_pms': active_pms,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Assessment/assessment_s_tl.html', context)


@login_required
def assessment_tl_s(request, as_id):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    if active_pms is not None:
        if user_is_tl:
            team_members = staff.objects.filter(staff_team=user_is_tl).exclude(staff_person=request.user)
            e = evaluation.objects.filter(evaluation_id=as_id).get()
            data = []
            if team_members.count() > 0:
                for mem in team_members:

                    ev_done = done_tl_evaluates_staff.objects.filter(done_evaluation=e, done_staff=mem.staff_person,
                                                                     done_team_leader=request.user)
                    if ev_done:
                        done = "Done"
                    else:
                        done = "Not Done"
                    mem_rec = [mem.staff_person.id, mem.staff_person.get_full_name, done]
                    data.append(mem_rec)

                context = {
                    'e': e,
                    'data': data,
                    'team_members': team_members,
                    'active_pms': active_pms,
                    'user_is_md': user_is_md,
                    'user_is_bu_head': user_is_bu_head,
                    'user_is_tl': user_is_tl,
                    'no_of_bu': no_of_bu,
                    'user_bu': user_bu,
                }
                return render(request, 'Assessment/assessment_tl_s_view.html', context)


@login_required
def assessment_tl_s_one(request, as_id, s_id):
    active_pms = pms.objects.filter(pms_status='Active')
    active_pms = active_pms.get()

    user_is_bu_head = request.user.staff_person.staff_head_bu
    user_is_md = request.user.staff_person.staff_md
    user_is_tl = request.user.staff_person.staff_head_team
    user_bu = request.user.staff_person.staff_bu
    no_of_bu = bu.objects.all().count()

    staff_mem = User.objects.get(id=s_id)

    if active_pms is not None:
        e = evaluation.objects.filter(evaluation_id=as_id).get()

        if e is not None:
            ev_done = done_tl_evaluates_staff.objects.filter(done_evaluation=e, done_staff=staff_mem,
                                                             done_team_leader=request.user)
            questions = question_tl_evaluate_staff.objects.filter(question_evaluation_id=e)
            default_data = {'done_evaluation': e, 'done_staff': staff_mem, 'done_team_leader': request.user, }
            if questions is not None:
                if questions:
                    count = 1
                    for question in questions:
                        done = 'done_q' + str(count)
                        default_data[done] = question
                        count = count + 1

                if request.method == 'POST':
                    form = asssessment_tl_s_Form(request.POST)

                    if form.is_valid():
                        post = form.save(commit=False)
                        post.save()
                        form = asssessment_tl_s_Form(default_data)
                        messages.success(request, 'Assessment done')

                        # return HttpResponseRedirect('')
                        return HttpResponseRedirect(reverse("Assessment_View", kwargs={'as_id': as_id}))
                else:
                    form = asssessment_tl_s_Form(default_data)
                form = asssessment_tl_s_Form(default_data)

        else:
            questions = None
            form = None

        context = {
            'e': e,
            'ev_done': ev_done,
            'form': form,
            'staff_mem': staff_mem,
            'questions': questions,
            'active_pms': active_pms,
            'user_is_md': user_is_md,
            'user_is_bu_head': user_is_bu_head,
            'user_is_tl': user_is_tl,
            'no_of_bu': no_of_bu,
            'user_bu': user_bu,
        }
        return render(request, 'Assessment/assessment_tl_s.html', context)
