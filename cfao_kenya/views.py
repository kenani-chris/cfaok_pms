import os
from email.mime.image import MIMEImage
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.views.generic import *
from itertools import chain
import datetime
from .permissions import is_member_company
from django.conf import settings


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
                <br>Dear ''' + name + ''',
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
        return '{}'.format(reverse('kpi-detail', kwargs={"pk": self.kwargs["pk"]}))


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

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7,
                      'november': 8,
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
        return HttpResponseRedirect(reverse('Individual_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('Individual_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


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
class StaffKpiTrackOneView(UpdateView):
    form_class = IndividualKpiResultsForm
    template_name = 'Staff_Kpi/trackkpi_staff_one.html'
    active_pms = pms
    context_object_name = 'staff'
    pk_url_kwarg = 'kpi_id'
    model = individual_Kpi

    def get_success_url(self):
        return '{}'.format(reverse('Staff_Track_Kpi_Staff_One', kwargs={"pk": self.kwargs["pk"],
                                                                        "kpi_id": self.kwargs["kpi_id"]}))

    def form_valid(self, form):
        super(StaffKpiTrackOneView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('Staff_Track_Kpi_Staff_One', kwargs={"pk": self.kwargs["pk"],
                                                                                 "kpi_id": self.kwargs["kpi_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_kpi'] = get_object_or_404(individual_Kpi, individual_kpi_id=self.kwargs.get('kpi_id'))
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['staff'] = User.objects.get(pk=self.kwargs['pk'])
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
            month = int(today.strftime('%-m'))
            if month == 1:
                month = 13
            elif month == 2:
                month = 14
            elif month == 3:
                month = 15

            context['current_month'] = month

            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            submit_date = int(active_pms.pms_individual_submit_results_date)

            result_kpi = get_object_or_404(individual_Kpi, pk=self.kwargs['kpi_id'])

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7,
                      'november': 8,
                      'december': 9, 'january': 10, 'february': 11, 'march': 12}

            if result_kpi.individual_kpi_april_score_approve == 'Approved':
                april = 'hidden'
            else:
                april = 'reveal'

            if result_kpi.individual_kpi_may_score_approve == 'Approved':
                may = 'hidden'
            else:
                may = 'reveal'

            if result_kpi.individual_kpi_june_score_approve == 'Approved':
                june = 'hidden'
            else:
                june = 'reveal'

            if result_kpi.individual_kpi_july_score_approve == 'Approved':
                july = 'hidden'
            else:
                july = 'reveal'

            if result_kpi.individual_kpi_august_score_approve == 'Approved':
                august = 'hidden'
            else:
                august = 'reveal'

            if result_kpi.individual_kpi_september_score_approve == 'Approved':
                september = 'hidden'
            else:
                september = 'reveal'

            if result_kpi.individual_kpi_october_score_approve == 'Approved':
                october = 'hidden'
            else:
                october = 'reveal'

            if result_kpi.individual_kpi_november_score_approve == 'Approved':
                november = 'hidden'
            else:
                november = 'reveal'

            if result_kpi.individual_kpi_december_score_approve == 'Approved':
                december = 'hidden'
            else:
                december = 'reveal'

            if result_kpi.individual_kpi_january_score_approve == 'Approved':
                january = 'hidden'
            else:
                january = 'reveal'

            if result_kpi.individual_kpi_february_score_approve == 'Approved':
                february = 'hidden'
            else:
                february = 'reveal'

            if result_kpi.individual_kpi_march_score_approve == 'Approved':
                march = 'hidden'
            else:
                march = 'reveal'

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


@login_required
def approve_individual_kpi_score(request, pk, kpi_id, month):
    staff_person = get_object_or_404(staff, id=request.user.id)
    kpi = get_object_or_404(individual_Kpi, individual_kpi_id=kpi_id)
    if month == 4:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_april_score_approve="Approved"
        )
    elif month == 5:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_may_score_approve="Approved"
        )
    elif month == 6:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_june_score_approve="Approved"
        )
    elif month == 7:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_july_score_approve="Approved"
        )
    elif month == 8:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_august_score_approve="Approved"
        )
    elif month == 9:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_september_score_approve="Approved"
        )
    elif month == 10:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_october_score_approve="Approved"
        )
    elif month == 11:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_november_score_approve="Approved"
        )
    elif month == 12:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_december_score_approve="Approved"
        )
    elif month == 1:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_january_score_approve="Approved"
        )
    elif month == 2:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_february_score_approve="Approved"
        )
    elif month == 3:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_march_score_approve="Approved"
        )
    messages.success(request, 'KPI score approved successful')
    message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved"
    send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Track_Kpi_Staff_One", kwargs={'pk': pk, 'kpi_id': kpi_id}))


@login_required
def approve_individual_kpi_score_dashboard(request, pk, kpi_id, month):
    staff_person = get_object_or_404(staff, id=request.user.id)
    kpi = get_object_or_404(individual_Kpi, individual_kpi_id=kpi_id)
    if month == 4:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_april_score_approve="Approved"
        )
    elif month == 5:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_may_score_approve="Approved"
        )
    elif month == 6:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_june_score_approve="Approved"
        )
    elif month == 7:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_july_score_approve="Approved"
        )
    elif month == 8:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_august_score_approve="Approved"
        )
    elif month == 9:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_september_score_approve="Approved"
        )
    elif month == 10:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_october_score_approve="Approved"
        )
    elif month == 11:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_november_score_approve="Approved"
        )
    elif month == 12:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_december_score_approve="Approved"
        )
    elif month == 1:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_january_score_approve="Approved"
        )
    elif month == 2:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_february_score_approve="Approved"
        )
    elif month == 3:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_march_score_approve="Approved"
        )
    messages.success(request, 'KPI score approved successful')
    message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been approved"
    send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Track_Kpi_Staff", kwargs={'pk': pk}))


# =====================================================================================================================
#                                                 BU KPI
# =====================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpiDashboard(TemplateView):
    template_name = 'Bu_Kpi/budashboard.html'
    model = bu_kpi

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
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpi(TemplateView):
    template_name = 'Bu_Kpi/bukpi.html'
    model = bu_kpi

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class SubmitBuKpiView(CreateView):
    form_class = SubmitBuKpiForm
    template_name = 'Bu_Kpi/submitkpi.html'

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_initial(self):
        initial = super(SubmitBuKpiView, self).get_initial()
        initial['bu_kpi_pms'] = pms.objects.get(pms_status='Active')
        initial['bu_kpi_user'] = self.request.user
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        initial['bu_kpi_bu'] = staff_person.staff_head_bu
        initial['bu_kpi_submit_date'] = datetime.date.today()
        initial['bu_kpi_last_edit'] = datetime.date.today()
        initial['bu_kpi_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('BU_Kpi_Submit'))

    def form_valid(self, form):
        super(SubmitBuKpiView, self).form_valid(form)
        user_team = get_object_or_404(staff, pk=self.request.user.id)
        mds = staff.objects.filter(staff_md='Yes')
        e_message = ""
        if mds is not None:
            for md in mds:
                if md:
                    e_message = 'you have one BU KPI from ' + self.request.user.get_full_name() + ' that requires ' \
                                                                                                  'your approval'
                else:
                    md = None
                    e_message = 'Your KPI has been submitted successfully but i keep on failing contacting your ' \
                                'immediate supervisor.<br>Please raise the issue with HR for support'
                send_email_pms('KPI Approval', md, self.request.user, e_message)
        else:
            md = None
            e_message = 'Your KPI has been submitted successfully but i keep on failing contacting your immediate ' \
                        'supervisor.<br>Please raise the issue with HR for support'

            send_email_pms('KPI Approval', md, self.request.user, e_message)

        messages.success(self.request, 'BU KPI submit successful')

        return HttpResponseRedirect(reverse('BU_Kpi_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackBuKpiView(ListView):
    template_name = 'Bu_Kpi/trackkpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        user_is_bu_head = staff_person.staff_head_bu
        user_is_md = staff_person.staff_md
        user_is_tl = staff_person.staff_head_team
        user_team = staff_person.staff_team
        user_bu = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            kpi = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)

        return kpi

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackBuKpiDetailView(DetailView):
    model = bu_kpi
    template_name = 'Bu_Kpi/one_individual_kpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        user_is_bu_head = staff_person.staff_head_bu
        user_is_md = staff_person.staff_md
        user_is_tl = staff_person.staff_head_team
        user_team = staff_person.staff_team
        user_bu = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            kpi = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)

        return kpi

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackBuKpiEditlView(UpdateView):
    model = bu_kpi
    form_class = SubmitBuKpiForm
    template_name = 'Bu_Kpi/one_individual_kpi_edit.html'

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_initial(self):
        initial = super(TrackBuKpiEditlView, self).get_initial()
        initial['bu_kpi_pms'] = pms.objects.get(pms_status='Active')
        initial['bu_kpi_user'] = self.request.user
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        initial['bu_kpi_bu'] = staff_person.staff_head_bu
        initial['bu_kpi_submit_date'] = datetime.date.today()
        initial['bu_kpi_last_edit'] = datetime.date.today()
        initial['bu_kpi_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('BU_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))

    def form_valid(self, form):
        super(TrackBuKpiEditlView, self).form_valid(form)
        messages.success(self.request, 'BU KPI edited successful')
        return HttpResponseRedirect(reverse('BU_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpiResultListView(ListView):
    template_name = 'Bu_Kpi/kpiresults.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        user_is_bu_head = staff_person.staff_head_bu
        user_is_md = staff_person.staff_md
        user_is_tl = staff_person.staff_head_team
        user_team = staff_person.staff_team
        user_bu = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            kpi = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)

        return kpi

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

            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(bu_kpi_status='Approved')
            context['pending'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpiResultUpdateView(UpdateView):
    model = bu_kpi
    form_class = BuKpiResultsForm
    template_name = 'Bu_Kpi/one_individual_kpi_update.html'
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
            submit_date = int(active_pms.pms_bu_submit_result_date)

            result_kpi = get_object_or_404(bu_kpi, pk=self.kwargs['pk'])

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7,
                      'november': 8,
                      'december': 9, 'january': 10, 'february': 11, 'march': 12}

            if result_kpi.bu_kpi_april_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_may_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_june_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_july_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_august_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_september_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_october_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_november_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_december_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_january_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_february_score_approve == 'Approved':
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

            if result_kpi.bu_kpi_march_score_approve == 'Approved':
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

            kpi = bu_kpi.objects.filter(bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(bu_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(bu_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(bu_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(bu_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_bu_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def form_valid(self, form):
        super(BuKpiResultUpdateView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('BU_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('BU_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


# =====================================================================================================================
#                                                 Company KPI
# =====================================================================================================================


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CoKpiDashboard(TemplateView):
    template_name = 'Company_Kpi/companydashboard.html'
    model = bu_kpi

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
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CompanyKpi(TemplateView):
    template_name = 'Company_Kpi/companykpi.html'
    model = company_kpi

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(company_kpi_status='Approved')
            context['pending'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected'] = kpi.filter(company_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class SubmitCompanyKpiView(CreateView):
    model = company_kpi
    form_class = SubmitCompanyKpiForm
    template_name = 'Company_Kpi/submitkpi.html'

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(company_kpi_status='Approved')
            context['pending'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected'] = kpi.filter(company_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_initial(self):
        initial = super(SubmitCompanyKpiView, self).get_initial()
        initial['company_kpi_pms'] = pms.objects.get(pms_status='Active')
        initial['company_kpi_user'] = self.request.user
        initial['company_kpi_submit_date'] = datetime.date.today()
        initial['company_kpi_last_edit'] = datetime.date.today()
        initial['company_kpi_status'] = 'Approved'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Company_Kpi_Submit'))

    def form_valid(self, form):
        super(SubmitCompanyKpiView, self).form_valid(form)
        messages.success(self.request, 'BU KPI submit successful')

        return HttpResponseRedirect(reverse('Company_Kpi_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditCompanyKpiView(ListView):
    template_name = 'Company_Kpi/trackkpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        user_is_bu_head = staff_person.staff_head_bu
        user_is_md = staff_person.staff_md
        user_is_tl = staff_person.staff_head_team
        user_team = staff_person.staff_team
        user_bu = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            kpi = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)

        return kpi

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(company_kpi_status='Approved')
            context['pending'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected'] = kpi.filter(company_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditCompanyKpiUpdateView(UpdateView):
    model = company_kpi
    form_class = SubmitCompanyKpiForm
    template_name = 'Company_Kpi/one_individual_kpi_edit.html'

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(company_kpi_status='Approved')
            context['pending'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected'] = kpi.filter(company_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def get_initial(self):
        initial = super(EditCompanyKpiUpdateView, self).get_initial()
        initial['company_kpi_pms'] = pms.objects.get(pms_status='Active')
        initial['company_kpi_user'] = self.request.user
        initial['company_kpi_submit_date'] = datetime.date.today()
        initial['company_kpi_last_edit'] = datetime.date.today()
        initial['company_kpi_status'] = 'Approved'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Company_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))

    def form_valid(self, form):
        super(EditCompanyKpiUpdateView, self).form_valid(form)
        messages.success(self.request, 'Company KPI edited successful')
        return HttpResponseRedirect(reverse('Company_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CompanyKpiResultListView(ListView):
    template_name = 'Company_Kpi/kpiresults.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        user_is_bu_head = staff_person.staff_head_bu
        user_is_md = staff_person.staff_md
        user_is_tl = staff_person.staff_head_team
        user_team = staff_person.staff_team
        user_bu = staff_person.staff_bu

        if pms.objects.filter(pms_status='Active').count() != 1:
            kpi = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)

        return kpi

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved'] = kpi.filter(company_kpi_status='Approved')
            context['pending'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected'] = kpi.filter(company_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved'].count() + context['pending'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected'].count()
            context['pending_count'] = context['pending'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CompanyKpiResultUpdateView(UpdateView):
    model = company_kpi
    form_class = CompanyKpiResultsForm
    template_name = 'Company_Kpi/one_individual_kpi_update.html'
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
            submit_date = int(active_pms.pms_bu_submit_result_date)

            result_kpi = get_object_or_404(company_kpi, pk=self.kwargs['pk'])

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7,
                      'november': 8,
                      'december': 9, 'january': 10, 'february': 11, 'march': 12}

            if months[month] <= months['april']:
                april = 'reveal'
            elif (months[month] - months['april']) == 1:
                if day <= submit_date:
                    april = 'reveal'
                else:
                    april = 'hidden'
            else:
                april = 'hidden'

            if months[month] <= months['may']:
                may = 'reveal'
            elif (months[month] - months['may']) == 1:
                if day <= submit_date:
                    may = 'reveal'
                else:
                    may = 'hidden'
            else:
                may = 'hidden'

            if months[month] <= months['june']:
                june = 'reveal'
            elif (months[month] - months['june']) == 1:
                if day <= submit_date:
                    june = 'reveal'
                else:
                    june = 'hidden'
            else:
                june = 'hidden'

            if months[month] <= months['july']:
                july = 'reveal'
            elif (months[month] - months['july']) == 1:
                if day <= submit_date:
                    july = 'reveal'
                else:
                    july = 'hidden'
            else:
                july = 'hidden'

            if months[month] <= months['august']:
                august = 'reveal'
            elif (months[month] - months['august']) == 1:
                if day <= submit_date:
                    august = 'reveal'
                else:
                    august = 'hidden'
            else:
                august = 'hidden'

            if months[month] <= months['september']:
                september = 'reveal'
            elif (months[month] - months['september']) == 1:
                if day <= submit_date:
                    september = 'reveal'
                else:
                    september = 'hidden'
            else:
                september = 'hidden'

            if months[month] <= months['october']:
                october = 'reveal'
            elif (months[month] - months['october']) == 1:
                if day <= submit_date:
                    october = 'reveal'
                else:
                    october = 'hidden'
            else:
                october = 'hidden'

            if months[month] <= months['november']:
                november = 'reveal'
            elif (months[month] - months['november']) == 1:
                if day <= submit_date:
                    november = 'reveal'
                else:
                    november = 'hidden'
            else:
                november = 'hidden'

            if months[month] <= months['december']:
                december = 'reveal'
            elif (months[month] - months['december']) == 1:
                if day <= submit_date:
                    december = 'reveal'
                else:
                    december = 'hidden'
            else:
                december = 'hidden'

            if months[month] <= months['january']:
                january = 'reveal'
            elif (months[month] - months['january']) == 1:
                if day <= submit_date:
                    january = 'reveal'
                else:
                    january = 'hidden'
            else:
                january = 'hidden'

            if months[month] <= months['february']:
                february = 'reveal'
            elif (months[month] - months['february']) == 1:
                if day <= submit_date:
                    february = 'reveal'
                else:
                    february = 'hidden'
            else:
                february = 'hidden'

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

            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(company_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(company_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(company_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(company_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(company_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(company_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_company_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context

    def form_valid(self, form):
        super(CompanyKpiResultUpdateView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('Company_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('Company_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


# ======================================================================================================================
#                                           BUs KPI
# ======================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsKpiListView(ListView):
    all_bu = bu.objects.all()
    model = individual_Kpi
    template_name = 'Bus_Kpi/staffkpi.html'

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
            md = context['user_is_md']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if md == 'Yes':
                bus = self.all_bu
                bus_kpi = []

                for bu in bus:
                    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=active_pms)
                    approved_kpi = kpi.filter(bu_kpi_status='Approved')
                    pending_kpi = kpi.filter(bu_kpi_status='Pending')
                    edit_kpi = kpi.filter(bu_kpi_status='Edit')
                    rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

                    required_count = pms.pms_bu_kpi_number
                    submitted_count = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                    rejected_count = rejected_kpi.count()
                    pending_count = pending_kpi.count() + edit_kpi.count()

                    bus_kpi.append([bu.bu_name, approved_kpi.count, pending_count, rejected_count, submitted_count])

                    if approved_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['bus'] = bus
                context['bus_kpi'] = bus_kpi
            else:
                context['bus'] = None
                context['bus_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsKpiPendingListView(ListView):
    model = bu_kpi
    template_name = 'Bus_Kpi/approvekpi.html'
    all_bu = bu.objects.all()

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
            md = context['user_is_md']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if md == 'Yes':
                bus = self.all_bu
                bus_kpi = []

                for bu in bus:
                    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=active_pms)
                    approved_kpi = kpi.filter(bu_kpi_status='Approved')
                    pending_kpi = kpi.filter(bu_kpi_status='Pending')
                    edit_kpi = kpi.filter(bu_kpi_status='Edit')
                    rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

                    required_count = pms.pms_bu_kpi_number
                    submitted_count = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                    rejected_count = rejected_kpi.count()
                    pending_count = pending_kpi.count() + edit_kpi.count()

                    bus_kpi.append([bu, approved_kpi.count, pending_count, rejected_count, submitted_count])

                    if approved_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['bus'] = bus
                context['bus_kpi'] = bus_kpi
            else:
                context['bus'] = None
                context['bus_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsKpiApproveView(DetailView):
    model = bu
    template_name = 'Bus_Kpi/one_individual_approve_kpi.html'
    active_pms = pms
    context_object_name = 'bu'
    all_bu = bu.objects.all()

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
            md = context['user_is_md']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if md == 'Yes':
                bus = self.all_bu
                bus_kpi = []

                for bu in bus:
                    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=active_pms)
                    approved_kpi = kpi.filter(bu_kpi_status='Approved')
                    pending_kpi = kpi.filter(bu_kpi_status='Pending')
                    edit_kpi = kpi.filter(bu_kpi_status='Edit')
                    rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

                    required_count = pms.pms_bu_kpi_number
                    submitted_count = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                    rejected_count = rejected_kpi.count()
                    pending_count = pending_kpi.count() + edit_kpi.count()

                    bus_kpi.append([bu.bu_name, approved_kpi.count, pending_count, rejected_count, submitted_count])

                    if approved_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['bus'] = bus
                context['bus_kpi'] = bus_kpi
            else:
                context['bus'] = None
                context['bus_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero

            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = bu_kpi.objects.filter(bu_kpi_bu=self.kwargs['pk'], bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved_kpi'] = kpi.filter(bu_kpi_status='Approved')
            context['pending_kpi'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected_kpi'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@login_required
def approve_bu_kpi(request, pk, kpi_id):
    bu_is = get_object_or_404(bu, bu_id=pk)
    bu_heads = staff.objects.filter(staff_head_bu=bu_is)
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(bu_kpi_status=bu_kpi.status[1][0])
    mds = staff.objects.filter(staff_md='Yes')

    message = "KPI <b>" + kpi.bu_kpi_title + "</b> has been approved"
    for md in mds:
        for buh in bu_heads:
            send_email_pms('KPI Approved', User.objects.get(id=buh.id), User.objects.get(id=md.id), message)

    messages.success(request, 'KPI Approved successful')
    return HttpResponseRedirect(reverse("BUs_Approve_Kpi_Detail", kwargs={'pk': pk}))


@login_required
def reject_bu_kpi(request, pk, kpi_id):
    bu_is = get_object_or_404(bu, bu_id=pk)
    bu_heads = staff.objects.filter(staff_head_bu=bu_is)
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(bu_kpi_status=bu_kpi.status[2][0])
    mds = staff.objects.filter(staff_md='Yes')

    message = "KPI <b>" + kpi.bu_kpi_title + "</b> has been Rejected"
    for md in mds:
        for buh in bu_heads:
            send_email_pms('KPI Approved', User.objects.get(id=buh.id), User.objects.get(id=md.id), message)

    messages.success(request, 'KPI Approved successful')
    return HttpResponseRedirect(reverse("BUs_Approve_Kpi_Detail", kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsTrackKpiListView(ListView):
    model = bu_kpi
    template_name = 'Bus_Kpi/trackkpi.html'
    all_bu = bu.objects.all()

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
            md = context['user_is_md']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if md == 'Yes':
                bus = self.all_bu
                bus_kpi = []

                for bu in bus:
                    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=active_pms)
                    approved_kpi = kpi.filter(bu_kpi_status='Approved')
                    pending_kpi = kpi.filter(bu_kpi_status='Pending')
                    edit_kpi = kpi.filter(bu_kpi_status='Edit')
                    rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

                    required_count = pms.pms_bu_kpi_number
                    submitted_count = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                    rejected_count = rejected_kpi.count()
                    pending_count = pending_kpi.count() + edit_kpi.count()

                    bus_kpi.append([bu, approved_kpi.count, pending_count, rejected_count, submitted_count])

                    if approved_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['bus'] = bus
                context['bus_kpi'] = bus_kpi
            else:
                context['bus'] = None
                context['bus_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsTrackKpiOneListView(DetailView):
    model = bu
    template_name = 'Bus_Kpi/trackkpi_staff.html'

    all_bu = bu.objects.all()

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
            md = context['user_is_md']
            team_approved = 0
            team_pending = 0
            team_zero = 0
            if md == 'Yes':
                bus = self.all_bu
                bus_kpi = []

                for bu in bus:
                    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=active_pms)
                    approved_kpi = kpi.filter(bu_kpi_status='Approved')
                    pending_kpi = kpi.filter(bu_kpi_status='Pending')
                    edit_kpi = kpi.filter(bu_kpi_status='Edit')
                    rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

                    required_count = pms.pms_bu_kpi_number
                    submitted_count = approved_kpi.count() + pending_kpi.count() + edit_kpi.count()
                    rejected_count = rejected_kpi.count()
                    pending_count = pending_kpi.count() + edit_kpi.count()

                    bus_kpi.append([bu.bu_name, approved_kpi.count, pending_count, rejected_count, submitted_count])

                    if approved_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                context['bus'] = bus
                context['bus_kpi'] = bus_kpi
            else:
                context['bus'] = None
                context['bus_kpi'] = None

            context['team_approved'] = team_approved
            context['team_pending'] = team_pending
            context['team_zero'] = team_zero

            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = bu_kpi.objects.filter(bu_kpi_bu=self.kwargs['pk'], bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved_kpi'] = kpi.filter(bu_kpi_status='Approved')
            context['pending_kpi'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected_kpi'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_individual_kpi_number
            context['submitted_count'] = context['approved_kpi'].count() + context['pending_kpi'].count() + \
                                         context['edit_kpi'].count()
            context['rejected_count'] = context['rejected_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['edit_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsKpiTrackOneView(UpdateView):
    form_class = BuKpiResultsForm
    template_name = 'Bus_Kpi/trackkpi_staff_one.html'
    active_pms = pms
    context_object_name = 'staff'
    pk_url_kwarg = 'kpi_id'
    model = bu_kpi

    def get_success_url(self):
        return '{}'.format(reverse('BUs_Track_Kpi_BUs_One', kwargs={"pk": self.kwargs["pk"],
                                                                    "kpi_id": self.kwargs["kpi_id"]}))

    def form_valid(self, form):
        super(BUsKpiTrackOneView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('BUs_Track_Kpi_BUs_One', kwargs={"pk": self.kwargs["pk"],
                                                                             "kpi_id": self.kwargs["kpi_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_kpi'] = get_object_or_404(bu_kpi, bu_kpi_id=self.kwargs.get('kpi_id'))
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['bu'] = get_object_or_404(bu, bu_id=self.kwargs['pk'])
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
            month = int(today.strftime('%-m'))
            if month == 1:
                month = 13
            elif month == 2:
                month = 14
            elif month == 3:
                month = 15

            context['current_month'] = month

            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms
            submit_date = int(active_pms.pms_individual_submit_results_date)

            result_kpi = get_object_or_404(bu_kpi, pk=self.kwargs['kpi_id'])

            months = {'april': 1, 'may': 2, 'june': 3, 'july': 4, 'august': 5, 'september': 6, 'october': 7,
                      'november': 8,
                      'december': 9, 'january': 10, 'february': 11, 'march': 12}

            if result_kpi.bu_kpi_april_score_approve == 'Approved':
                april = 'hidden'
            else:
                april = 'reveal'

            if result_kpi.bu_kpi_may_score_approve == 'Approved':
                may = 'hidden'
            else:
                may = 'reveal'

            if result_kpi.bu_kpi_june_score_approve == 'Approved':
                june = 'hidden'
            else:
                june = 'reveal'

            if result_kpi.bu_kpi_july_score_approve == 'Approved':
                july = 'hidden'
            else:
                july = 'reveal'

            if result_kpi.bu_kpi_august_score_approve == 'Approved':
                august = 'hidden'
            else:
                august = 'reveal'

            if result_kpi.bu_kpi_september_score_approve == 'Approved':
                september = 'hidden'
            else:
                september = 'reveal'

            if result_kpi.bu_kpi_october_score_approve == 'Approved':
                october = 'hidden'
            else:
                october = 'reveal'

            if result_kpi.bu_kpi_november_score_approve == 'Approved':
                november = 'hidden'
            else:
                november = 'reveal'

            if result_kpi.bu_kpi_december_score_approve == 'Approved':
                december = 'hidden'
            else:
                december = 'reveal'

            if result_kpi.bu_kpi_january_score_approve == 'Approved':
                january = 'hidden'
            else:
                january = 'reveal'

            if result_kpi.bu_kpi_february_score_approve == 'Approved':
                february = 'hidden'
            else:
                february = 'reveal'

            if result_kpi.bu_kpi_march_score_approve == 'Approved':
                march = 'hidden'
            else:
                march = 'reveal'

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

            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            kpi = bu_kpi.objects.filter(bu_kpi_user=self.kwargs['pk'],
                                        bu_kpi_pms=active_pms)
            context['my_kpi'] = kpi
            context['approved1_kpi'] = kpi.filter(bu_kpi_status='Approved 1')
            context['approved2_kpi'] = kpi.filter(bu_kpi_status='Approved 2')
            context['pending_kpi'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected1_kpi'] = kpi.filter(bu_kpi_status='Rejected 1')
            context['rejected2_kpi'] = kpi.filter(bu_kpi_status='Rejected 2')

            context['required_count'] = pms.pms_bu_kpi_number
            context['submitted_count'] = context['approved1_kpi'].count() + context['approved2_kpi'].count() + \
                                         context['pending_kpi'].count() + context['edit_kpi'].count() + \
                                         context['rejected1_kpi'].count()
            context['rejected_count'] = context['rejected2_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count() + context['rejected1_kpi'].count() + \
                                       context['edit_kpi'].count()
            context['now'] = datetime.date.today()

        tl = context['user_is_tl']
        team_approved = 0
        team_pending = 0
        team_zero = 0
        if tl is not None:
            team_members = staff.objects.filter(staff_team=tl).exclude(staff_person=self.request.user)
            team_members_kpi = []

            for member in team_members:
                kpi = bu_kpi.objects.filter(bu_kpi_user=member.staff_person,
                                            bu_kpi_pms=active_pms)
                approved1_kpi = kpi.filter(bu_kpi_status='Approved 1')
                approved2_kpi = kpi.filter(bu_kpi_status='Approved 2')
                pending_kpi = kpi.filter(bu_kpi_status='Pending')
                edit_kpi = kpi.filter(bu_kpi_status='Edit')
                rejected1_kpi = kpi.filter(bu_kpi_status='Rejected 1')
                rejected2_kpi = kpi.filter(bu_kpi_status='Rejected 2')

                required_count = pms.pms_bu_kpi_number
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


@login_required
def approve_bu_kpi_score(request, pk, kpi_id, month):
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    if month == 4:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_april_score_approve="Approved"
        )
    elif month == 5:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_may_score_approve="Approved"
        )
    elif month == 6:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_june_score_approve="Approved"
        )
    elif month == 7:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_july_score_approve="Approved"
        )
    elif month == 8:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_august_score_approve="Approved"
        )
    elif month == 9:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_september_score_approve="Approved"
        )
    elif month == 10:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_october_score_approve="Approved"
        )
    elif month == 11:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_november_score_approve="Approved"
        )
    elif month == 12:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_december_score_approve="Approved"
        )
    elif month == 1:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_january_score_approve="Approved"
        )
    elif month == 2:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_february_score_approve="Approved"
        )
    elif month == 3:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_march_score_approve="Approved"
        )

    return HttpResponseRedirect(reverse("BUs_Track_Kpi_BUs_One", kwargs={'pk': pk, 'kpi_id': kpi_id}))


@login_required
def approve_bu_kpi_score_dashboard(request, pk, kpi_id, month):
    staff_person = get_object_or_404(staff, id=request.user.id)
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    if month == 4:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_april_score_approve="Approved"
        )
    elif month == 5:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_may_score_approve="Approved"
        )
    elif month == 6:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_june_score_approve="Approved"
        )
    elif month == 7:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_july_score_approve="Approved"
        )
    elif month == 8:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_august_score_approve="Approved"
        )
    elif month == 9:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_september_score_approve="Approved"
        )
    elif month == 10:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_october_score_approve="Approved"
        )
    elif month == 11:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_november_score_approve="Approved"
        )
    elif month == 12:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_december_score_approve="Approved"
        )
    elif month == 1:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_january_score_approve="Approved"
        )
    elif month == 2:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_february_score_approve="Approved"
        )
    elif month == 3:
        bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(
            bu_kpi_march_score_approve="Approved"
        )
    messages.success(request, 'KPI score approved successful')
    message = "KPI <b>" + kpi.bu_kpi_title + "</b> has been approved"
    send_email_pms('KPI Approved', User.objects.get(id=pk), request.user, message)

    return HttpResponseRedirect(reverse("Staff_Track_Kpi_Staff", kwargs={'pk': pk}))


# =====================================================================================================================
#                                                 My Checkin
# =====================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class MyCheckIn(TemplateView):
    template_name = 'Check-In/checkin.html'

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
            context['all_ci'] = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=self.request.user)

            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

            context['total_submitted'] = context['confirmed_ci'].count() + context['pending_ci'].count()
            context['total_pending'] = context['pending_ci'].count()
            context['total_rejected'] = context['rejected_ci'].count()
            context['percent_submitted'] = context['total_submitted'] / active_pms.checkin_number * 100
            ci_months = []
            for ci in context['submitted_ci']:
                ci_months.append(ci.checkIn_month)
            context['ci_months'] = ci_months
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class SubmitCheckIn(CreateView):
    form_class = SubmitCheckInForm
    template_name = 'Check-In/submitci.html'

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
            context['all_ci'] = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=self.request.user)

            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

            context['total_submitted'] = context['confirmed_ci'].count() + context['pending_ci'].count()
            context['total_pending'] = context['pending_ci'].count()
            context['total_rejected'] = context['rejected_ci'].count()
            context['percent_submitted'] = context['total_submitted'] / active_pms.checkin_number * 100
            context['month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
            ci_months = []
            for ci in context['submitted_ci']:
                ci_months.append(ci.checkIn_month)
            context['ci_months'] = ci_months
        return context

    def get_initial(self):
        initial = super(SubmitCheckIn, self).get_initial()
        initial['checkIn_pms'] = pms.objects.get(pms_status='Active')
        initial['checkIn_submit_date'] = datetime.date.today()
        initial['checkIn_month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
        initial['checkIn_staff'] = self.request.user
        initial['checkIn_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Check-In_Submit'))

    def form_valid(self, form):
        super(SubmitCheckIn, self).form_valid(form)
        user_team = get_object_or_404(staff, pk=self.request.user.id)
        user_team = user_team.staff_team
        e_message = ""
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                e_message = 'you have one CheckIn from ' + self.request.user.get_full_name() + ' that requires your approval'
                for tl in team_leader:
                    send_email_pms('KPI Approval', User.objects.get(pk=tl.id), self.request.user, e_message)

            else:
                team_leader = None
                e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                            'supervisor.<br>Please raise the issue with HR for support'
                send_email_pms('KPI Approval', team_leader, self.request.user, e_message)
        else:
            team_leader = None
            e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                        'supervisor.<br>Please raise the issue with HR for support'
            send_email_pms('KPI Approval', team_leader, self.request.user, e_message)

        messages.success(self.request, 'Checkin submit successful')

        return HttpResponseRedirect(reverse('Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackCheckIn(ListView):
    template_name = 'Check-In/trackci.html'

    def get_queryset(self):
        active_pms = get_active_pms()
        return checkIn.objects.filter(checkIn_staff=self.request.user, checkIn_pms=active_pms)

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
            context['all_ci'] = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=self.request.user)

            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

            context['total_submitted'] = context['confirmed_ci'].count() + context['pending_ci'].count()
            context['total_pending'] = context['pending_ci'].count()
            context['total_rejected'] = context['rejected_ci'].count()
            context['percent_submitted'] = context['total_submitted'] / active_pms.checkin_number * 100
            context['month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
            ci_months = []
            for ci in context['submitted_ci']:
                ci_months.append(ci.checkIn_month)
            context['ci_months'] = ci_months
        return context

    def get_initial(self):
        initial = super(SubmitCheckIn, self).get_initial()
        initial['checkIn_pms'] = pms.objects.get(pms_status='Active')
        initial['checkIn_submit_date'] = datetime.date.today()
        initial['checkIn_month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
        initial['checkIn_staff'] = self.request.user
        initial['checkIn_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Check-In_Submit'))

    def form_valid(self, form):
        super(SubmitCheckIn, self).form_valid(form)
        user_team = get_object_or_404(staff, pk=self.request.user.id)
        user_team = user_team.staff_team
        e_message = ""
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                e_message = 'you have one CheckIn from ' + self.request.user.get_full_name() + ' that requires your approval'
                for tl in team_leader:
                    send_email_pms('KPI Approval', User.objects.get(pk=tl.id), self.request.user, e_message)

            else:
                team_leader = None
                e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                            'supervisor.<br>Please raise the issue with HR for support'
                send_email_pms('KPI Approval', team_leader, self.request.user, e_message)
        else:
            team_leader = None
            e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                        'supervisor.<br>Please raise the issue with HR for support'
            send_email_pms('KPI Approval', team_leader, self.request.user, e_message)

        messages.success(self.request, 'Checkin submit successful')

        return HttpResponseRedirect(reverse('Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class DetailCheckIn(DetailView):
    model = checkIn
    template_name = 'Check-In/one_individual_ci.html'
    context_object_name = 'ci'

    def get_queryset(self):
        active_pms = get_active_pms()
        return checkIn.objects.filter(checkIn_staff=self.request.user, checkIn_pms=active_pms)

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
            context['all_ci'] = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=self.request.user)

            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

            context['total_submitted'] = context['confirmed_ci'].count() + context['pending_ci'].count()
            context['total_pending'] = context['pending_ci'].count()
            context['total_rejected'] = context['rejected_ci'].count()
            context['percent_submitted'] = context['total_submitted'] / active_pms.checkin_number * 100
            context['month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
            ci_months = []
            for ci in context['submitted_ci']:
                ci_months.append(ci.checkIn_month)
            context['ci_months'] = ci_months
        return context

    def get_initial(self):
        initial = super(SubmitCheckIn, self).get_initial()
        initial['checkIn_pms'] = pms.objects.get(pms_status='Active')
        initial['checkIn_submit_date'] = datetime.date.today()
        initial['checkIn_month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
        initial['checkIn_staff'] = self.request.user
        initial['checkIn_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Check-In_Submit'))

    def form_valid(self, form):
        super(SubmitCheckIn, self).form_valid(form)
        user_team = get_object_or_404(staff, pk=self.request.user.id)
        user_team = user_team.staff_team
        e_message = ""
        if user_team is not None:
            team_leader = staff.objects.filter(staff_head_team=user_team)
            if team_leader:
                e_message = 'you have one CheckIn from ' + self.request.user.get_full_name() + ' that requires your approval'
                for tl in team_leader:
                    send_email_pms('KPI Approval', User.objects.get(pk=tl.id), self.request.user, e_message)

            else:
                team_leader = None
                e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                            'supervisor.<br>Please raise the issue with HR for support'
                send_email_pms('KPI Approval', team_leader, self.request.user, e_message)
        else:
            team_leader = None
            e_message = 'Your CheckIn has been submitted successfully but i keep on failing contacting your immediate ' \
                        'supervisor.<br>Please raise the issue with HR for support'
            send_email_pms('KPI Approval', team_leader, self.request.user, e_message)

        messages.success(self.request, 'Checkin submit successful')

        return HttpResponseRedirect(reverse('Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditCheckIn(UpdateView):
    form_class = SubmitCheckInForm
    template_name = 'Check-In/one_individual_ci_edit.html'
    model = checkIn
    context_object_name = 'ci'

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
            context['all_ci'] = checkIn.objects.filter(checkIn_pms=active_pms, checkIn_staff=self.request.user)

            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

            context['total_submitted'] = context['confirmed_ci'].count() + context['pending_ci'].count()
            context['total_pending'] = context['pending_ci'].count()
            context['total_rejected'] = context['rejected_ci'].count()
            context['percent_submitted'] = context['total_submitted'] / active_pms.checkin_number * 100
            context['month'] = datetime.datetime.strftime(datetime.datetime.now(), '%B')
            ci_months = []
            for ci in context['submitted_ci']:
                ci_months.append(ci.checkIn_month)
            context['ci_months'] = ci_months
        return context

    def get_initial(self):
        ci = get_object_or_404(checkIn, checkIn_id=self.kwargs['pk'])
        initial = super(EditCheckIn, self).get_initial()
        initial['checkIn_pms'] = ci.checkIn_pms
        initial['checkIn_submit_date'] = datetime.date.today()
        initial['checkIn_month'] = ci.checkIn_month
        initial['checkIn_staff'] = self.request.user
        initial['checkIn_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Check-In_Submit'))

    def form_valid(self, form):
        super(EditCheckIn, self).form_valid(form)
        messages.success(self.request, 'Checkin edited successful')

        return HttpResponseRedirect(reverse('Check-In_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


# ======================================================================================================================
#                                           STAFF CHECKIN
# ======================================================================================================================


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffCheckIn(TemplateView):
    template_name = 'Staff_Ci/staffci.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person.get_full_name, member.staff_person.email,
                                       member.staff_Pf_Number, staff_approved_ci, staff_pending_ci, staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffApproveCheckIn(TemplateView):
    template_name = 'Staff_Ci/approveci.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffApproveStaffCheckIn(DetailView):
    context_object_name = 'staff'
    model = User
    template_name = 'Staff_Ci/staffcistaff.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

            context['all_ci'] = checkIn.objects.filter(checkIn_staff=self.kwargs['pk'], checkIn_pms=active_pms)
            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffApproveStaffCheckInOne(UpdateView):
    form_class = ApproveCheckInForm
    context_object_name = 'ci'
    model = checkIn
    template_name = 'Staff_Ci/one_individual_approve_ci.html'
    pk_url_kwarg = 'ci_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, id=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(User, id=self.kwargs['pk'])

        if pms.objects.filter(pms_status='Active').count() != 1:
            context['pms'] = None
        else:
            active_pms = pms.objects.get(pms_status='Active')
            context['pms'] = active_pms

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

            context['all_ci'] = checkIn.objects.filter(checkIn_staff=self.kwargs['pk'], checkIn_pms=active_pms)
            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

        return context

    def get_initial(self):
        initial = super(StaffApproveStaffCheckInOne, self).get_initial()
        initial['checkIn_team_leader'] = self.request.user
        initial['checkIn_confirm_date'] = datetime.date.today()
        initial['checkIn_status'] = 'Confirmed'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('Staff_Approve_CI'))

    def form_valid(self, form):
        ci = get_object_or_404(checkIn, checkIn_id=self.kwargs['ci_id'])
        super(StaffApproveStaffCheckInOne, self).form_valid(form)
        messages.success(self.request, 'CheckIn Approved Successfully')
        send_email_pms('CheckIn Confirmed', ci.checkIn_staff, self.request.user,
                       'You Kpi for the month ' + ci.checkIn_month + ' has been confirmed')
        return HttpResponseRedirect(reverse('Staff_Approve_CI'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackCheckIn(TemplateView):
    context_object_name = 'staff'
    model = User
    template_name = 'Staff_Ci/trackci.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackStaffCheckIn(DetailView):
    context_object_name = 'staff'
    model = User
    template_name = 'Staff_Ci/trackci_staff.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

            context['all_ci'] = checkIn.objects.filter(checkIn_staff=self.kwargs['pk'], checkIn_pms=active_pms)
            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackStaffDetailCheckIn(DetailView):
    context_object_name = 'ci'
    model = checkIn
    pk_url_kwarg = 'ci_id'
    template_name = 'Staff_Ci/trackci_staff_one.html'

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

            staff_n_ci = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)
                ci_approved_count = 0
                ci_pending_count = 0
                ci_zero_count = 0
                for member in team_members:
                    staff_approved_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Confirmed').count()
                    staff_pending_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                              checkIn_status='Pending').count()
                    staff_rejected_ci = checkIn.objects.filter(checkIn_staff=member.id, checkIn_pms_id=active_pms,
                                                               checkIn_status='Rejected').count()

                    total_ci = staff_approved_ci + staff_pending_ci

                    staff_n_ci.append([member.staff_person, member.staff_Pf_Number, staff_approved_ci, staff_pending_ci,
                                       staff_rejected_ci,
                                       total_ci])

                    if staff_approved_ci > 0:
                        ci_approved_count = + 1

                    if staff_pending_ci > 0:
                        ci_pending_count = + 1

                    if total_ci < 1:
                        ci_zero_count = + 1

                context['staff_n_ci'] = staff_n_ci
                context['team_members'] = team_members
                context['ci_approved_count'] = ci_approved_count
                context['ci_pending_count'] = ci_pending_count
                context['ci_zero_count'] = ci_zero_count

            context['staff'] = get_object_or_404(User, id=self.kwargs['pk'])
            context['all_ci'] = checkIn.objects.filter(checkIn_staff=self.kwargs['pk'], checkIn_pms=active_pms)
            context['confirmed_ci'] = context['all_ci'].filter(checkIn_status='Confirmed')
            context['pending_ci'] = context['all_ci'].filter(checkIn_status="Pending")
            context['rejected_ci'] = context['all_ci'].filter(checkIn_status="Rejected")
            context['submitted_ci'] = context['all_ci'].exclude(checkIn_status="Rejected")

        return context


# ======================================================================================================================
#                                           ASSESSMENT
# ======================================================================================================================


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class Assessment(TemplateView):
    template_name = 'Assessment/assessment.html'

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

            today = datetime.date.today()
            evaluations = evaluation.objects.filter(evaluation_pms=active_pms)
            context['running_evaluations'] = evaluation.objects.filter(evaluation_pms=active_pms,
                                                                       evaluation_start_date__lte=today,
                                                                       evaluation_end_date__gte=today)
            context['future_evaluations'] = evaluation.objects.filter(evaluation_pms=active_pms,
                                                                      evaluation_start_date__gt=today, )
            context['completed_evaluations'] = evaluation.objects.filter(evaluation_pms=active_pms,
                                                                         evaluation_end_date__lt=today)

            evals = []
            for e in evaluations:

                # TL evaluates Staff
                # =====================================================================

                s_tl = "N/A"
                tl_s = "N/A"

                if e.evaluation_start_date <= today <= e.evaluation_end_date:
                    active = True
                else:
                    active = False
                if context['user_is_tl'] is not None:
                    team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                        staff_person=self.request.user)

                    if context['user_is_md'] == "Yes":

                        staff_ev_count = 0
                        for mem in team_members:
                            if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                      done_staff=mem.staff_person.id,
                                                                      done_team_leader=self.request.user) is not None:
                                staff_ev_count = staff_ev_count + 1

                        tl_s = str(staff_ev_count) + "/" + str(team_members.count())

                    else:
                        staff_ev_count = 0
                        if team_members.count() > 1:
                            for mem in team_members:
                                if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                          done_staff=mem.staff_person.id,
                                                                          done_team_leader=self.request.user) is not None:
                                    staff_ev_count = staff_ev_count + 1
                else:
                    ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                     done_staff=self.request.user)
                    if ev_done:
                        s_tl = "Done"
                    else:
                        s_tl = "Not done"

                evals.append([e, s_tl, tl_s, active])

            context['evals'] = evals

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentView(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'Assessment/assessment_list.html'

    pk_url_kwarg = 'as_id'

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

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

            my_team = get_object_or_404(staff, id=self.request.user.id)
            tl = staff.objects.filter(staff_head_team=my_team.staff_team).first()
            context['team_leader'] = tl

            s_tl = "N/A"
            tl_s = "N/A"

            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)

                if context['user_is_md'] == "Yes":

                    staff_ev_count = 0
                    for mem in team_members:
                        if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                  done_staff=mem.staff_person.id,
                                                                  done_team_leader=self.request.user) is not None:
                            staff_ev_count = staff_ev_count + 1

                    tl_s = str(staff_ev_count) + "/" + str(team_members.count())

                else:
                    staff_ev_count = 0
                    for mem in team_members:
                        if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                  done_staff=mem.staff_person.id,
                                                                  done_team_leader=self.request.user):
                            staff_ev_count = staff_ev_count + 1

                    tl_s = str(staff_ev_count) + "/" + str(team_members.count())

                    ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                     done_staff=self.request.user)
                    if ev_done:
                        s_tl = "Done"
                    else:
                        s_tl = "Not done"

            else:
                ev_done = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                 done_staff=self.request.user)
                if ev_done:
                    s_tl = "Done"
                else:
                    s_tl = "Not done"

            context['evals'] = [e, tl_s, s_tl]

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentTlS(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'Assessment/assessment_tl_s_view.html'

    pk_url_kwarg = 'as_id'

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

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)

                for mem in team_members:
                    if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                              done_staff=mem.staff_person.id,
                                                              done_team_leader=self.request.user):
                        ev = 'Done'
                    else:
                        ev = "Not Done"
                    evals.append([mem, ev])

            context['evals'] = evals

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentTlS(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'Assessment/assessment_tl_s_view.html'

    pk_url_kwarg = 'as_id'

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

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                team_members = staff.objects.filter(staff_team=context['user_is_tl']).exclude(
                    staff_person=self.request.user)

                for mem in team_members:
                    if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                              done_staff=mem.staff_person.id,
                                                              done_team_leader=self.request.user):
                        ev = 'Done'
                    else:
                        ev = "Not Done"
                    evals.append([mem, ev])

            context['evals'] = evals

        return context

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
