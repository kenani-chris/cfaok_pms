import os
from email.mime.image import MIMEImage

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UserModel
import datetime
from .permissions import is_member_company, is_admin
from django.conf import settings


def get_active_pms():
    if pms.objects.filter(pms_status='Active').count() != 1:
        return None
    else:
        return pms.objects.get(pms_status='Active')


def reset_all_password(request):
    staffs = staff.objects.all()

    for staff_u in staffs:
        user = get_object_or_404(User, id=staff_u.staff_person.id)
        # 'password_reset_confirm' ''' + str(user.id) + ''' ''' + default_token_generator.make_token(user) + ''' %
        # message = format_html('Click On the following <a href="{}">HERE</a>to reset your PMS password the following', reverse('toyota_kenya:password_reset_confirm', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.id)), 'token': default_token_generator.make_token(user)}))


        encoded_uid = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        link = format_html(str('<a href="https://ck-pms.com/accounts/reset/' + encoded_uid + '/' + token + '">PMS Link</a>'))
        pms_link = format_html(str('<a href="https://ck-pms.com/">Online PMS</a>'))

        msg = format_html('We are glad to have you onboard ' + pms_link + '<br><br>Your username: <b>' + user.username + '</b><br>Click on this ' + link + ' to reset your password<br>')

        message = msg
        if user.is_active and user.email:
            send_email_pms_one_reciepient('Welcome to PMS FY 2021-2022', user, message)

    return HttpResponseRedirect(reverse('toyota_kenya:index'))


def checkin_score(pms, staff):
    cis = checkIn.objects.filter(checkIn_staff=staff, checkIn_pms=pms)
    cis_approved = cis.filter(checkIn_status='Confirmed')
    cis_pending = cis.filter(checkIn_status='pending')
    required_cis = pms.checkin_number

    all_ci = []
    for ci in cis:
        all_ci.append(ci.checkIn_month)

    all_ci = len(set(all_ci))

    score = matrix_checkin.objects.filter(matrix_pms=pms, matrix_checkin_no=all_ci)
    if not score:
        score = 0

    return [score, cis, cis_approved, cis_pending]


def ind_kpi_score(pms, staff):
    kpi = individual_Kpi.objects.filter(individual_kpi_user=staff, individual_kpi_pms=pms)
    kpi_approved = kpi.filter(individual_kpi_status='Approved 2')

    kpi_matrix = kpi_months.objects.filter(kpi_months_class=kpi_months.kpi_class[2][0])
    if kpi_matrix:
        kpi_matrix = kpi_matrix.first()
        use_months = []
        if kpi_matrix.kpi_month_april == 'Yes':
            use_months.append('April')
        if kpi_matrix.kpi_month_may == 'Yes':
            use_months.append('May')
        if kpi_matrix.kpi_month_june == 'Yes':
            use_months.append('June')
        if kpi_matrix.kpi_month_july == 'Yes':
            use_months.append('July')
        if kpi_matrix.kpi_month_august == 'Yes':
            use_months.append('August')
        if kpi_matrix.kpi_month_september == 'Yes':
            use_months.append('September')
        if kpi_matrix.kpi_month_october == 'Yes':
            use_months.append('October')
        if kpi_matrix.kpi_month_november == 'Yes':
            use_months.append('November')
        if kpi_matrix.kpi_month_december == 'Yes':
            use_months.append('December')
        if kpi_matrix.kpi_month_january == 'Yes':
            use_months.append('January')
        if kpi_matrix.kpi_month_february == 'Yes':
            use_months.append('February')
        if kpi_matrix.kpi_month_march == 'Yes':
            use_months.append('March')
    else:
        use_months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
                      'January', 'February', 'March']

    kpi_score = []
    sum_score = 0
    for kpi in kpi_approved:
        kpi_calc = []
        target = kpi.individual_kpi_target
        if kpi.individual_kpi_type == 'Addition':
            if 'April' in use_months and kpi.individual_kpi_april_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_april_score)
            if 'May' in use_months and kpi.individual_kpi_may_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_may_score)
            if 'June' in use_months and kpi.individual_kpi_june_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_june_score)
            if 'July' in use_months and kpi.individual_kpi_july_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_july_score)
            if 'August' in use_months and kpi.individual_kpi_august_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_august_score)
            if 'September' in use_months and kpi.individual_kpi_september_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_september_score)
            if 'October' in use_months and kpi.individual_kpi_october_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_october_score)
            if 'November' in use_months and kpi.individual_kpi_november_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_november_score)
            if 'December' in use_months and kpi.individual_kpi_december_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_december_score)
            if 'January' in use_months and kpi.individual_kpi_january_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_january_score)
            if 'February' in use_months and kpi.individual_kpi_february_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_february_score)
            if 'March' in use_months and kpi.individual_kpi_march_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_march_score)

            kpi_calc = [0 if v is None else v for v in kpi_calc]
            score = sum(kpi_calc)
            print('Score ' + str(score))
            if kpi.individual_kpi_function == "Maximize" or kpi.individual_kpi_function == "maximize":
                score = (score / target) * 100
            else:
                if score == 0:
                    if score <= target:
                        score = 100
                    else:
                        score = 0
                else:
                    score = (target / score) * 100

            kpi_score.append([kpi, round(score, 0)])

        elif kpi.individual_kpi_type == 'YTD':
            today = datetime.date.today()
            value = 0
            if today >= pms.pms_end_date:
                if 'March' in use_months and kpi.individual_kpi_march_score_approve == 'Approved':
                    value = kpi.individual_kpi_march_score
            else:
                month = today.strftime('%B')
                if month == 'April':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'April' in use_months and kpi.individual_kpi_april_score_approve == 'Approved':
                            value = kpi.individual_kpi_april_score
                if month == 'May':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'May' in use_months and kpi.individual_kpi_may_score_approve == 'Approved':
                            value = kpi.individual_kpi_may_score
                    else:
                        if 'April' in use_months and kpi.individual_kpi_april_score_approve == 'Approved':
                            value = kpi.individual_kpi_april_score
                if month == 'June':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'June' in use_months and kpi.individual_kpi_june_score_approve == 'Approved':
                            value = kpi.individual_kpi_june_score
                    else:
                        if 'May' in use_months and kpi.individual_kpi_may_score_approve == 'Approved':
                            value = kpi.individual_kpi_may_score

                if month == 'July':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'July' in use_months and kpi.individual_kpi_july_score_approve == 'Approved':
                            value = kpi.individual_kpi_july_score
                    else:
                        if 'June' in use_months and kpi.individual_kpi_june_score_approve == 'Approved':
                            value = kpi.individual_kpi_june_score

                if month == 'August':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'August' in use_months and kpi.individual_kpi_august_score_approve == 'Approved':
                            value = kpi.individual_kpi_august_score
                    else:
                        if 'July' in use_months and kpi.individual_kpi_july_score_approve == 'Approved':
                            value = kpi.individual_kpi_july_score
                if month == 'September':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'September' in use_months and kpi.individual_kpi_september_score_approve == 'Approved':
                            value = kpi.individual_kpi_september_score
                    else:
                        if 'August' in use_months and kpi.individual_kpi_august_score_approve == 'Approved':
                            value = kpi.individual_kpi_august_score

                if month == 'October':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'October' in use_months and kpi.individual_kpi_october_score_approve == 'Approved':
                            value = kpi.individual_kpi_october_score
                    else:
                        if 'September' in use_months and kpi.individual_kpi_september_score_approve == 'Approved':
                            value = kpi.individual_kpi_september_score
                if month == 'November':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'November' in use_months and kpi.individual_kpi_november_score_approve == 'Approved':
                            value = kpi.individual_kpi_november_score
                    else:
                        if 'October' in use_months and kpi.individual_kpi_october_score_approve == 'Approved':
                            value = kpi.individual_kpi_october_score
                if month == 'December':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'December' in use_months and kpi.individual_kpi_december_score_approve == 'Approved':
                            value = kpi.individual_kpi_december_score
                    else:
                        if 'November' in use_months and kpi.individual_kpi_november_score_approve == 'Approved':
                            value = kpi.individual_kpi_november_score
                if month == 'January':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'January' in use_months and kpi.individual_kpi_january_score_approve == 'Approved':
                            value = kpi.individual_kpi_january_score
                    else:
                        if 'December' in use_months and kpi.individual_kpi_december_score_approve == 'Approved':
                            value = kpi.individual_kpi_december_score
                if month == 'February':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'February' in use_months and kpi.individual_kpi_february_score_approve == 'Approved':
                            value = kpi.individual_kpi_february_score
                    else:
                        if 'January' in use_months and kpi.individual_kpi_january_score_approve == 'Approved':
                            value = kpi.individual_kpi_january_score
                if month == 'March':
                    if int(today.strftime('%-d')) >= pms.pms_individual_submit_results_date:
                        if 'March' in use_months and kpi.individual_kpi_march_score_approve == 'Approved':
                            value = kpi.individual_kpi_march_score
                    else:
                        if 'February' in use_months and kpi.individual_kpi_february_score_approve == 'Approved':
                            value = kpi.individual_kpi_february_score
            if value is None:
                value = 0

            if kpi.individual_kpi_function == "Maximize" or kpi.individual_kpi_function == "maximize":

                score = (value / target) * 100
            else:
                if value == 0:
                    if value <= target:
                        score = 100
                    else:
                        score = 0
                else:
                    score = (value / score) * 100

            kpi_score.append([kpi, round(score, 0)])

        elif kpi.individual_kpi_type == 'Average':
            if 'April' in use_months and kpi.individual_kpi_april_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_april_score)
            if 'May' in use_months and kpi.individual_kpi_may_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_may_score)
            if 'June' in use_months and kpi.individual_kpi_june_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_june_score)
            if 'July' in use_months and kpi.individual_kpi_july_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_july_score)
            if 'August' in use_months and kpi.individual_kpi_august_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_august_score)
            if 'September' in use_months and kpi.individual_kpi_september_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_september_score)
            if 'October' in use_months and kpi.individual_kpi_october_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_october_score)
            if 'November' in use_months and kpi.individual_kpi_november_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_november_score)
            if 'December' in use_months and kpi.individual_kpi_december_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_december_score)
            if 'January' in use_months and kpi.individual_kpi_january_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_january_score)
            if 'February' in use_months and kpi.individual_kpi_february_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_february_score)
            if 'March' in use_months and kpi.individual_kpi_march_score_approve == 'Approved':
                kpi_calc.append(kpi.individual_kpi_march_score)

            if len(kpi_calc) > 0:
                kpi_calc = [0 if v is None else v for v in kpi_calc]
                score = sum(kpi_calc) / len(kpi_calc)

                if kpi.individual_kpi_function == "Maximize" or kpi.individual_kpi_function == 'maximize':
                    score = (score / target) * 100
                else:
                    if score == 0:
                        if score <= target:
                            score = 100
                        else:
                            score = 0
                    else:
                        score = (target / score) * 100
            else:
                score = 0

            kpi_score.append([kpi, round(score, 0)])

        else:
            score = 0
            kpi_score.append([kpi, 0])

        score = round(score * (kpi.individual_kpi_weight / 100), 0)
        sum_score += score
        print('sum_score: ' + str(sum_score))

    return [sum_score, kpi_score, len(kpi_score)]


def bu_kpi_score(pms, bu):
    kpi = bu_kpi.objects.filter(bu_kpi_bu=bu, bu_kpi_pms=pms)
    kpi_approved = kpi.filter(bu_kpi_status='Approved')

    kpi_matrix = kpi_months.objects.filter(kpi_months_class=kpi_months.kpi_class[1][0])
    if kpi_matrix:
        kpi_matrix = kpi_matrix.first()
        use_months = []
        if kpi_matrix.kpi_month_april == 'Yes':
            use_months.append('April')
        if kpi_matrix.kpi_month_may == 'Yes':
            use_months.append('May')
        if kpi_matrix.kpi_month_june == 'Yes':
            use_months.append('June')
        if kpi_matrix.kpi_month_july == 'Yes':
            use_months.append('July')
        if kpi_matrix.kpi_month_august == 'Yes':
            use_months.append('August')
        if kpi_matrix.kpi_month_september == 'Yes':
            use_months.append('September')
        if kpi_matrix.kpi_month_october == 'Yes':
            use_months.append('October')
        if kpi_matrix.kpi_month_november == 'Yes':
            use_months.append('November')
        if kpi_matrix.kpi_month_december == 'Yes':
            use_months.append('December')
        if kpi_matrix.kpi_month_january == 'Yes':
            use_months.append('January')
        if kpi_matrix.kpi_month_february == 'Yes':
            use_months.append('February')
        if kpi_matrix.kpi_month_march == 'Yes':
            use_months.append('March')
    else:
        use_months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
                      'January', 'February', 'March']

    kpi_score = []
    sum_score = 0
    for kpi in kpi_approved:
        kpi_calc = []
        target = kpi.bu_kpi_target
        if kpi.bu_kpi_type == 'Addition':
            if 'April' in use_months and kpi.bu_kpi_april_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_april_score)
            if 'May' in use_months and kpi.bu_kpi_may_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_may_score)
            if 'June' in use_months and kpi.bu_kpi_june_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_june_score)
            if 'July' in use_months and kpi.bu_kpi_july_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_july_score)
            if 'August' in use_months and kpi.bu_kpi_august_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_august_score)
            if 'September' in use_months and kpi.bu_kpi_september_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_september_score)
            if 'October' in use_months and kpi.bu_kpi_october_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_october_score)
            if 'November' in use_months and kpi.bu_kpi_november_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_november_score)
            if 'December' in use_months and kpi.bu_kpi_december_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_december_score)
            if 'January' in use_months and kpi.bu_kpi_january_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_january_score)
            if 'February' in use_months and kpi.bu_kpi_february_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_february_score)
            if 'March' in use_months and kpi.bu_kpi_march_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_march_score)

            kpi_calc = [0 if v is None else v for v in kpi_calc]
            score = sum(kpi_calc)
            if kpi.bu_kpi_function == "Maximize" or kpi.bu_kpi_function == "maximize":
                score = (score / target) * 100
            else:
                if score == 0:
                    if score <= target:
                        score = 100
                    else:
                        score = 0
                else:
                    score = (target / score) * 100

            kpi_score.append([kpi, round(score, 0)])

        elif kpi.bu_kpi_type == 'YTD':
            today = datetime.date.today()
            value = 0
            if today >= pms.pms_end_date:
                if 'March' in use_months and kpi.bu_kpi_march_score_approve == 'Approved':
                    value = kpi.bu_kpi_march_score
            else:
                month = today.strftime('%B')
                if month == 'April':
                    if 'April' in use_months and kpi.bu_kpi_april_score_approve == 'Approved':
                        value = kpi.bu_kpi_april_score
                if month == 'May':
                    if 'May' in use_months and kpi.bu_kpi_may_score_approve == 'Approved':
                        value = kpi.bu_kpi_may_score
                if month == 'June':
                    if 'June' in use_months and kpi.bu_kpi_june_score_approve == 'Approved':
                        value = kpi.bu_kpi_june_score
                if month == 'July':
                    if 'July' in use_months and kpi.bu_kpi_july_score_approve == 'Approved':
                        value = kpi.bu_kpi_july_score
                if month == 'August':
                    if 'August' in use_months and kpi.bu_kpi_august_score_approve == 'Approved':
                        value = kpi.bu_kpi_august_score
                if month == 'September':
                    if 'September' in use_months and kpi.bu_kpi_september_score_approve == 'Approved':
                        value = kpi.bu_kpi_september_score
                if month == 'October':
                    if 'October' in use_months and kpi.bu_kpi_october_score_approve == 'Approved':
                        value = kpi.bu_kpi_october_score
                if month == 'November':
                    if 'November' in use_months and kpi.bu_kpi_november_score_approve == 'Approved':
                        value = kpi.bu_kpi_november_score
                if month == 'December':
                    if 'December' in use_months and kpi.bu_kpi_december_score_approve == 'Approved':
                        value = kpi.bu_kpi_december_score
                if month == 'January':
                    if 'January' in use_months and kpi.bu_kpi_january_score_approve == 'Approved':
                        value = kpi.bu_kpi_january_score
                if month == 'February':
                    if 'February' in use_months and kpi.bu_kpi_february_score_approve == 'Approved':
                        value = kpi.bu_kpi_february_score
                if month == 'March':
                    if 'March' in use_months and kpi.bu_kpi_march_score_approve == 'Approved':
                        value = kpi.bu_kpi_march_score

            if value is None:
                value = 0

            if kpi.bu_kpi_function == "Maximize" or kpi.bu_kpi_function == "maximize":
                score = (value / target) * 100
            else:
                if value == 0:
                    if value <= target:
                        score = 100
                    else:
                        score = 0
                else:
                    score = (value / round(score, 0)) * 100

            kpi_score.append([kpi, score])

        elif kpi.bu_kpi_type == 'Average':
            if 'April' in use_months and kpi.bu_kpi_april_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_april_score)
            if 'May' in use_months and kpi.bu_kpi_may_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_may_score)
            if 'June' in use_months and kpi.bu_kpi_june_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_june_score)
            if 'July' in use_months and kpi.bu_kpi_july_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_july_score)
            if 'August' in use_months and kpi.bu_kpi_august_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_august_score)
            if 'September' in use_months and kpi.bu_kpi_september_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_september_score)
            if 'October' in use_months and kpi.bu_kpi_october_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_october_score)
            if 'November' in use_months and kpi.bu_kpi_november_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_november_score)
            if 'December' in use_months and kpi.bu_kpi_december_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_december_score)
            if 'January' in use_months and kpi.bu_kpi_january_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_january_score)
            if 'February' in use_months and kpi.bu_kpi_february_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_february_score)
            if 'March' in use_months and kpi.bu_kpi_march_score_approve == 'Approved':
                kpi_calc.append(kpi.bu_kpi_march_score)

            if len(kpi_calc) > 0:
                kpi_calc = [0 if v is None else v for v in kpi_calc]
                score = sum(kpi_calc) / len(kpi_calc)

                if kpi.bu_kpi_function == "Maximize" or kpi.bu_kpi_function == "maximize":
                    score = (score / target) * 100
                else:
                    if score == 0:
                        if score <= target:
                            score = 100
                        else:
                            score = 0
                    else:
                        score = (target / score) * 100
            else:
                score = 0

            kpi_score.append([kpi, round(score, 0)])

        else:
            score = 0
            kpi_score.append([kpi, 0])

        score = round(score * (kpi.bu_kpi_weight / 100), 0)
        sum_score += score

    return [sum_score, kpi_score, len(kpi_score)]


def company_kpi_score(pms):
    kpi_score = []
    sum_score = 0
    if pms:
        kpi = company_kpi.objects.filter(company_kpi_pms=pms)
        kpi_approved = kpi.filter(company_kpi_status='Approved')

        kpi_matrix = kpi_months.objects.filter(kpi_months_class=kpi_months.kpi_class[0][0])
        if kpi_matrix:
            kpi_matrix = kpi_matrix.first()
            use_months = []
            if kpi_matrix.kpi_month_april == 'Yes':
                use_months.append('April')
            if kpi_matrix.kpi_month_may == 'Yes':
                use_months.append('May')
            if kpi_matrix.kpi_month_june == 'Yes':
                use_months.append('June')
            if kpi_matrix.kpi_month_july == 'Yes':
                use_months.append('July')
            if kpi_matrix.kpi_month_august == 'Yes':
                use_months.append('August')
            if kpi_matrix.kpi_month_september == 'Yes':
                use_months.append('September')
            if kpi_matrix.kpi_month_october == 'Yes':
                use_months.append('October')
            if kpi_matrix.kpi_month_november == 'Yes':
                use_months.append('November')
            if kpi_matrix.kpi_month_december == 'Yes':
                use_months.append('December')
            if kpi_matrix.kpi_month_january == 'Yes':
                use_months.append('January')
            if kpi_matrix.kpi_month_february == 'Yes':
                use_months.append('February')
            if kpi_matrix.kpi_month_march == 'Yes':
                use_months.append('March')
        else:
            use_months = ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
                          'January', 'February', 'March']

        kpi_score = []
        sum_score = 0
        for kpi in kpi_approved:
            kpi_calc = []
            target = kpi.company_kpi_target
            if kpi.company_kpi_type == 'Addition':
                if 'April' in use_months:
                    kpi_calc.append(kpi.company_kpi_april_score)
                if 'May' in use_months:
                    kpi_calc.append(kpi.company_kpi_may_score)
                if 'June' in use_months:
                    kpi_calc.append(kpi.company_kpi_june_score)
                if 'July' in use_months:
                    kpi_calc.append(kpi.company_kpi_july_score)
                if 'August' in use_months:
                    kpi_calc.append(kpi.company_kpi_august_score)
                if 'September' in use_months:
                    kpi_calc.append(kpi.company_kpi_september_score)
                if 'October' in use_months:
                    kpi_calc.append(kpi.company_kpi_october_score)
                if 'November' in use_months:
                    kpi_calc.append(kpi.company_kpi_november_score)
                if 'December' in use_months:
                    kpi_calc.append(kpi.company_kpi_december_score)
                if 'January' in use_months:
                    kpi_calc.append(kpi.company_kpi_january_score)
                if 'February' in use_months:
                    kpi_calc.append(kpi.company_kpi_february_score)
                if 'March' in use_months:
                    kpi_calc.append(kpi.company_kpi_march_score)

                kpi_calc = [0 if v is None else v for v in kpi_calc]
                score = sum(kpi_calc)

                if kpi.company_kpi_function == "Maximize" or kpi.company_kpi_function == "maximize":
                    score = (score / target) * 100
                else:
                    if score == 0:
                        if score <= target:
                            score = 100
                        else:
                            score = 0
                    else:
                        score = (target / score) * 100

                kpi_score.append([kpi, round(score, 0)])

            elif kpi.company_kpi_type == 'YTD':
                today = datetime.date.today()
                value = 0
                if today >= pms.pms_end_date:
                    if 'March' in use_months:
                        value = kpi.company_kpi_march_score
                else:
                    month = today.strftime('%B')
                    if month == 'April':
                        if 'April' in use_months:
                            value = kpi.company_kpi_april_score
                    if month == 'May':
                        if 'May' in use_months:
                            value = kpi.company_kpi_may_score
                    if month == 'June':
                        if 'June' in use_months:
                            value = kpi.company_kpi_june_score
                    if month == 'July':
                        if 'July' in use_months:
                            value = kpi.company_kpi_july_score
                    if month == 'August':
                        if 'August' in use_months:
                            value = kpi.company_kpi_august_score
                    if month == 'September':
                        if 'September' in use_months:
                            value = kpi.company_kpi_september_score
                    if month == 'October':
                        if 'October' in use_months:
                            value = kpi.company_kpi_october_score
                    if month == 'November':
                        if 'November' in use_months:
                            value = kpi.company_kpi_november_score
                    if month == 'December':
                        if 'December' in use_months:
                            value = kpi.company_kpi_december_score
                    if month == 'January':
                        if 'January' in use_months:
                            value = kpi.company_kpi_january_score
                    if month == 'February':
                        if 'February' in use_months:
                            value = kpi.company_kpi_february_score
                    if month == 'March':
                        if 'March' in use_months:
                            value = kpi.company_kpi_march_score
                if value is None:
                    value = 0
                if kpi.company_kpi_function == "Maximize" or kpi.company_kpi_function == "maximize":

                    score = (value / target) * 100
                else:
                    if value == 0:
                        if value <= target:
                            score = 100
                        else:
                            score = 0
                    else:
                        score = (value / score) * 100

                kpi_score.append([kpi, round(score, 0)])

            elif kpi.company_kpi_type == 'Average':
                if 'April' in use_months:
                    kpi_calc.append(kpi.company_kpi_april_score)
                if 'May' in use_months:
                    kpi_calc.append(kpi.company_kpi_may_score)
                if 'June' in use_months:
                    kpi_calc.append(kpi.company_kpi_june_score)
                if 'July' in use_months:
                    kpi_calc.append(kpi.company_kpi_july_score)
                if 'August' in use_months:
                    kpi_calc.append(kpi.company_kpi_august_score)
                if 'September' in use_months:
                    kpi_calc.append(kpi.company_kpi_september_score)
                if 'October' in use_months:
                    kpi_calc.append(kpi.company_kpi_october_score)
                if 'November' in use_months:
                    kpi_calc.append(kpi.company_kpi_november_score)
                if 'December' in use_months:
                    kpi_calc.append(kpi.company_kpi_december_score)
                if 'January' in use_months:
                    kpi_calc.append(kpi.company_kpi_january_score)
                if 'February' in use_months:
                    kpi_calc.append(kpi.company_kpi_february_score)
                if 'March' in use_months:
                    kpi_calc.append(kpi.company_kpi_march_score)

                if len(kpi_calc) > 0:
                    kpi_calc = [0 if v is None else v for v in kpi_calc]
                    score = sum(kpi_calc) / len(kpi_calc)

                    if kpi.company_kpi_function == "Maximize" or kpi.company_kpi_function == "maximize":
                        score = (score / target) * 100
                    else:
                        if score == 0:
                            if score <= target:
                                score = 100
                            else:
                                score = 0
                        else:
                            score = (target / score) * 100
                else:
                    score = 0

                kpi_score.append([kpi, round(score, 0)])

            else:
                score = 0
                kpi_score.append([kpi, 0])

            score = round(score * (kpi.company_kpi_weight / 100), 0)
            sum_score += score

    return [sum_score, kpi_score, len(kpi_score)]


def assessment_score(pms, staff_u):
    staff_person = get_object_or_404(staff, staff_person=staff_u.id)
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    default_score = {'Strongly Agree': 10, 'Agree': 5, 'Disagree': -5, 'Strongly Disagree': -10, None: 0}
    evals = evaluation.objects.filter(evaluation_pms=pms, evaluation_use='Yes')

    score = tl_s_score = s_tl_score = tl_s_total_score = s_tl_total_score = eval_score = 0
    for eval in evals:
        if user_is_md == 'Yes':
            tl_s_score = 'N/A'
            s_tl_score = s_tl_score_fun(staff_u, eval, default_score)

            s_tl_total_score += s_tl_score
            tl_s_total_score = 'N/A'

            eval_score += s_tl_score

        elif user_is_tl:
            s_tl_score = s_tl_score_fun(staff_u, eval, default_score)
            tl_s_score = tl_s_score_fun(staff_u, eval, default_score)

            s_tl_total_score += s_tl_score
            tl_s_total_score += tl_s_total_score

            eval_score += (s_tl_score + tl_s_score) / 2
        else:
            s_tl_score = 'N/A'
            tl_s_score = tl_s_score_fun(staff_u, eval, default_score)

            s_tl_total_score = 'N/A'
            tl_s_total_score += tl_s_score

            eval_score += tl_s_score

    if evals:
        eval_score = eval_score / evals.count()
        if s_tl_total_score != 'N/A':
            s_tl_total_score = s_tl_total_score / evals.count()
        if tl_s_total_score != 'N/A':
            tl_s_total_score = tl_s_total_score / evals.count()

    return [eval_score, s_tl_total_score, tl_s_total_score]


def tl_s_score_fun(staff_u, eval, default_score):
    tl_s_team_score = 0
    # TL_S_Score
    staff_u = get_object_or_404(staff, staff_person=staff_u.id)

    tl_responses = done_tl_evaluates_staff.objects.filter(done_staff=staff_u.staff_person)
    for response in tl_responses:
        q1_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q1)
        if q1_score:
            q1_score = q1_score.first().response_score
        else:
            q1_score = default_score[response.score_q1]

        q2_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q2)
        if q2_score:
            q2_score = q2_score.first().response_score
        else:
            q2_score = default_score[response.score_q2]

        q3_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q3)
        if q3_score:
            q3_score = q3_score.first().response_score
        else:
            q3_score = default_score[response.score_q3]

        q4_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q4)
        if q4_score:
            q4_score = q4_score.first().response_score
        else:
            q4_score = default_score[response.score_q4]

        q5_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q5)
        if q5_score:
            q5_score = q5_score.first().response_score
        else:
            q5_score = default_score[response.score_q5]

        q6_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q6)
        if q6_score:
            q6_score = q6_score.first().response_score
        else:
            q6_score = default_score[response.score_q6]

        q7_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q7)
        if q7_score:
            q7_score = q7_score.first().response_score
        else:
            q7_score = default_score[response.score_q7]

        tl_score = (q1_score + q2_score + q3_score + q4_score + q5_score + q6_score + q7_score) / 7 * 100
        tl_s_team_score += tl_score
    if tl_responses:
        tl_s_team_score = tl_s_team_score / tl_responses.count()

    return tl_s_team_score


def s_tl_score_fun(staff_u, eval, default_score):
    s_tl_team_score = 0
    # S_TL_Score
    staff_u = get_object_or_404(staff, staff_person=staff_u.id)
    staff_responses = done_staff_evaluates_tl.objects.filter(done_team_leader=staff_u.staff_person)
    for response in staff_responses:
        q1_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q1)
        if q1_score:
            q1_score = q1_score.first().response_score
        else:
            q1_score = default_score[response.score_q1]

        q2_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q2)
        if q2_score:
            q2_score = q2_score.first().response_score
        else:
            q2_score = default_score[response.score_q2]

        q3_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q3)
        if q3_score:
            q3_score = q3_score.first().response_score
        else:
            q3_score = default_score[response.score_q3]

        q4_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q4)
        if q4_score:
            q4_score = q4_score.first().response_score
        else:
            q4_score = default_score[response.score_q4]

        q5_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q5)
        if q5_score:
            q5_score = q5_score.first().response_score
        else:
            q5_score = default_score[response.score_q5]

        q6_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q6)
        if q6_score:
            q6_score = q6_score.first().response_score
        else:
            q6_score = default_score[response.score_q6]

        q7_score = evaluation_responses.objects.filter(response_evaluation=eval, response=response.score_q7)
        if q7_score:
            q7_score = q7_score.first().response_score
        else:
            q7_score = default_score[response.score_q7]

        staff_score = (q1_score + q2_score + q3_score + q4_score + q5_score + q6_score + q7_score) / 7 * 100
        s_tl_team_score += staff_score

    if staff_responses:
        s_tl_team_score = s_tl_team_score / staff_responses.count()

    return s_tl_team_score


def get_matrix(pms, staff_u):
    staff_person = get_object_or_404(staff, staff_person=staff_u.id)
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    user_is_bu_head = staff_person.staff_head_bu

    matrix = [0, 0, 0, 0]

    if user_is_md == 'Yes':
        md_matrix = score_matrix.objects.filter(matrix_class='MD', matrix_pms=pms)
        if md_matrix:
            md_matrix = md_matrix.first()
            md_company = md_matrix.matrix_company_kpi_weight
            md_bu = md_matrix.matrix_bu_kpi_weight
            md_individual = md_matrix.matrix_individual_kpi_weight
            md_assessment = md_matrix.matrix_assessment_weight

            matrix = [md_company, md_bu, md_individual, md_assessment]

    elif user_is_bu_head:
        bu_matrix = score_matrix.objects.filter(matrix_class='BU', matrix_pms=pms)
        if bu_matrix:
            bu_matrix = bu_matrix.first()
            bu_company = bu_matrix.matrix_company_kpi_weight
            bu_bu = bu_matrix.matrix_bu_kpi_weight
            bu_individual = bu_matrix.matrix_individual_kpi_weight
            bu_assessment = bu_matrix.matrix_assessment_weight

            matrix = [bu_company, bu_bu, bu_individual, bu_assessment]
    else:
        individual_matrix = score_matrix.objects.filter(matrix_class='Staff', matrix_pms=pms)
        if individual_matrix:
            individual_matrix = individual_matrix.first()
            individual_company = individual_matrix.matrix_company_kpi_weight
            individual_bu = individual_matrix.matrix_bu_kpi_weight
            individual_individual = individual_matrix.matrix_individual_kpi_weight
            individual_assessment = individual_matrix.matrix_assessment_weight

            matrix = [individual_company, individual_bu, individual_individual, individual_assessment]

    return matrix


def overall_score(pms, staff_u):
    matrix = get_matrix(pms, staff_u)



@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class HomeView(TemplateView):
    template_name = 'toyota_kenya/index.html'
    model = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not pms.objects.filter(pms_status='Active'):
            context['pms'] = None
        else:
            context['pms'] = pms.objects.get(pms_status='Active')
            staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
            context['user_is_bu_head'] = staff_person.staff_head_bu
            context['user_is_md'] = staff_person.staff_md
            context['user_is_tl'] = staff_person.staff_head_team
            context['user_team'] = staff_person.staff_team
            context['user_bu'] = staff_person.staff_bu
            context['checkin'] = checkin_score(context['pms'], self.request.user)
            context['matrix'] = get_matrix(context['pms'], self.request.user)

            """if context['user_is_md'] == 'Yes':
                context['kpi'] = company_kpi_score(context['pms'])
                context['company_kpi'] = company_kpi_score(context['pms'])
            elif context['user_is_bu_head']:
                context['kpi'] = bu_kpi_score(context['pms'], context['user_is_bu_head'])
                context['bu_kpi'] = bu_kpi_score(context['pms'], context['user_is_bu_head'])
                context['company_kpi'] = company_kpi_score(context['pms'])
            else:
                context['kpi'] = ind_kpi_score(context['pms'], self.request.user)
                context['company_kpi'] = company_kpi_score(context['pms'])
                if staff_person.staff_bu:
                    context['bu_kpi'] = bu_kpi_score(context['pms'], staff_person.staff_bu)
                else:
                    context['bu_kpi'] = [0, [], [], []]

            context['assessment'] = assessment_score(context['pms'], self.request.user)"""

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class NoActivePmsView(TemplateView):
    template_name = 'toyota_kenya/no_active_pms.html'

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
    template_name = 'toyota_kenya/Individual_Kpi/mykpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Individual_Kpi/submitkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Individual_Kpi_Submit'))

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

        return HttpResponseRedirect(reverse('toyota_kenya:Individual_Kpi_Submit'))


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


def send_email_pms_one_reciepient(subject, receiver, e_message):
    name = receiver.get_full_name()

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
        to=[receiver.email]
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


@login_required
def delete_individual_kpi(request, kpi_id):

    kpi = individual_Kpi.objects.get(individual_kpi_id=kpi_id)
    kpi.delete()

    messages.success(request, 'KPI Deleted Successfully')

    return HttpResponseRedirect(reverse("toyota_kenya:Individual_Kpi_Detail1"))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackKpiView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Individual_Kpi/trackkpi.html'
    active_pms = pms

    def get_queryset(self):
        if get_active_pms() is None:
            return None
        else:
            return individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                 individual_kpi_pms=get_active_pms())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Individual_Kpi/one_individual_kpi_edit.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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

    def get_initial(self):
        initial = super(EditKpiView, self).get_initial()
        initial['individual_kpi_status'] = 'Pending'

        return initial


    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:kpi-detail', kwargs={"pk": self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class DetailKpiView(DetailView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Individual_Kpi/one_individual_kpi.html'
    active_pms = pms

    def get_queryset(self):
        if get_active_pms() is None:
            return None
        else:
            return individual_Kpi.objects.filter(individual_kpi_user=self.request.user,
                                                 individual_kpi_pms=get_active_pms())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Individual_Kpi/kpiresults.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Individual_Kpi/one_individual_kpi_update.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return HttpResponseRedirect(reverse('toyota_kenya:Individual_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Individual_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


# ======================================================================================================================
#                                           STAFF KPI
# ======================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiListView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Staff_Kpi/staffkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            bu_head = context['user_is_bu_head']
            team_approved = bu_approved = 0
            team_pending = bu_pending = 0
            team_zero = bu_zero = 0
            if bu_head is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

                    team_members_kpi.append([member.staff_person.get_full_name(), member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                bu_members = staff.objects.filter(staff_bu=bu_head).exclude(staff_person=self.request.user)
                bu_members_kpi = []

                for member in bu_members:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count() + approved1_kpi.count()

                    bu_members_kpi.append([member.staff_person.get_full_name(), member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        bu_approved = bu_approved + 1

                    if pending_count > 0:
                        bu_pending = bu_pending + 1

                    if submitted_count < 1:
                        bu_zero = bu_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
                context['bu_members'] = bu_members
                context['bu_members_kpi'] = bu_members_kpi
            elif tl is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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
            context['bu_approved'] = bu_approved
            context['bu_pending'] = bu_pending
            context['bu_zero'] = bu_zero
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiPendingListView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Staff_Kpi/approvekpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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
class BUStaffKpiPendingListView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Staff_Kpi/buapprovekpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            bu_head = context['user_is_bu_head']
            team_approved = bu_approved = 0
            team_pending = bu_pending = 0
            team_zero = bu_zero = 0
            if bu_head is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

                    team_members_kpi.append([member.staff_person.get_full_name(), member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                bu_members = staff.objects.filter(staff_bu=bu_head).exclude(staff_person=self.request.user)
                bu_members_kpi = []

                for member in bu_members:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

                    bu_members_kpi.append([member, member.staff_Pf_Number,
                                           approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                           submitted_count])

                    if approved2_kpi.count() > 0:
                        bu_approved = bu_approved + 1

                    if approved1_kpi.count() > 0:
                        bu_pending = bu_pending + 1

                    if submitted_count < 1:
                        bu_zero = bu_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
                context['bu_members'] = bu_members
                context['bu_members_kpi'] = bu_members_kpi
            elif tl is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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
            context['bu_approved'] = bu_approved
            context['bu_pending'] = bu_pending
            context['bu_zero'] = bu_zero

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffKpiApproveView(DetailView):
    model = User
    template_name = 'toyota_kenya/Staff_Kpi/one_individual_approve_kpi.html'
    active_pms = pms
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['rejected_count'] = context['rejected2_kpi'].count() + context['rejected1_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count()
            context['now'] = datetime.date.today()
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUStaffKpiApproveView(DetailView):
    model = User
    template_name = 'toyota_kenya/Staff_Kpi/bu_one_individual_approve_kpi.html'
    active_pms = pms
    context_object_name = 'staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['rejected_count'] = context['rejected2_kpi'].count() + context['rejected1_kpi'].count()
            context['pending_count'] = context['pending_kpi'].count()
            context['now'] = datetime.date.today()

            tl = context['user_is_tl']
            bu_head = context['user_is_bu_head']
            team_approved = bu_approved = 0
            team_pending = bu_pending = 0
            team_zero = bu_zero = 0
            if bu_head is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

                    team_members_kpi.append([member.staff_person.get_full_name(), member.staff_Pf_Number,
                                             approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                             submitted_count])

                    if approved2_kpi.count() > 0:
                        team_approved = team_approved + 1

                    if pending_count > 0:
                        team_pending = team_pending + 1

                    if submitted_count < 1:
                        team_zero = team_zero + 1

                bu_members = staff.objects.filter(staff_bu=bu_head).exclude(staff_person=self.request.user)
                bu_members_kpi = []

                for member in bu_members:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

                    bu_members_kpi.append([member, member.staff_Pf_Number,
                                           approved2_kpi.count, approved1_kpi.count, pending_count, rejected_count,
                                           submitted_count])

                    if approved2_kpi.count() > 0:
                        bu_approved = bu_approved + 1

                    if approved1_kpi.count() > 0:
                        bu_pending = bu_pending + 1

                    if submitted_count < 1:
                        bu_zero = bu_zero + 1

                context['team_members'] = team_members
                context['team_members_kpi'] = team_members_kpi
                context['bu_members'] = bu_members
                context['bu_members_kpi'] = bu_members_kpi
            elif tl is not None:
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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
            context['bu_approved'] = bu_approved
            context['bu_pending'] = bu_pending
            context['bu_zero'] = bu_zero
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

        return HttpResponseRedirect(reverse("toyota_kenya:Staff_BU_Approve_Kpi_Detail", kwargs={'pk': pk}))

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

        return HttpResponseRedirect(reverse("toyota_kenya:Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


@login_required
def reject_individual_kpi(request, pk, kpi_id):
    staff_person = get_object_or_404(staff, id=request.user.id)
    user_is_bu_head = staff_person.staff_head_bu
    user_is_md = staff_person.staff_md
    user_is_tl = staff_person.staff_head_team
    kpi = individual_Kpi.objects.get(individual_kpi_id=kpi_id)

    if user_is_bu_head is not None or user_is_md is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[3][0],
        )

        messages.success(request, 'KPI Rejected successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been Rejected<br> KPI status has changed to" \
                                                         " <b>Rejected 1</b> to allow you to edit the KPI approval"
        send_email_pms('KPI Rejected', User.objects.get(id=pk), request.user, message)

        return HttpResponseRedirect(reverse("toyota_kenya:Staff_BU_Approve_Kpi_Detail", kwargs={'pk': pk}))
    elif user_is_tl is not None:
        individual_Kpi.objects.filter(individual_kpi_id=kpi_id).update(
            individual_kpi_status=individual_Kpi.status[3][0], individual_kpi_team_leader_approval=request.user.id)

        messages.success(request, 'KPI Rejected successful')
        message = "KPI <b>" + kpi.individual_kpi_title + "</b> has been Rejected<br> KPI status has changed to" \
                                                         " <b>Rejected 1</b> to allow you to edit the KPI approval"
        send_email_pms('KPI Rejected', User.objects.get(id=pk), request.user, message)

        return HttpResponseRedirect(reverse("toyota_kenya:Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


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

    return HttpResponseRedirect(reverse("toyota_kenya:Staff_Approve_Kpi_Detail", kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackKpiListView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Staff_Kpi/trackkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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
    template_name = 'toyota_kenya/Staff_Kpi/trackkpi_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['pending_count'] = context['pending_kpi'].count()

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
                rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                pending_count = pending_kpi.count()

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
    template_name = 'toyota_kenya/Staff_Kpi/trackkpi_staff_one.html'
    active_pms = pms
    context_object_name = 'staff'
    pk_url_kwarg = 'kpi_id'
    model = individual_Kpi

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Staff_Track_Kpi_Staff_One', kwargs={"pk": self.kwargs["pk"],
                                                                        "kpi_id": self.kwargs["kpi_id"]}))

    def form_valid(self, form):
        super(StaffKpiTrackOneView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('toyota_kenya:Staff_Track_Kpi_Staff_One', kwargs={"pk": self.kwargs["pk"],
                                                                                 "kpi_id": self.kwargs["kpi_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_kpi'] = get_object_or_404(individual_Kpi, individual_kpi_id=self.kwargs.get('kpi_id'))
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['pending_count'] = context['pending_kpi'].count()
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
                rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                pending_count = pending_kpi.count()

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

    return HttpResponseRedirect(reverse("toyota_kenya:Staff_Track_Kpi_Staff_One", kwargs={'pk': pk, 'kpi_id': kpi_id}))


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

    return HttpResponseRedirect(reverse("toyota_kenya:Staff_Track_Kpi_Staff", kwargs={'pk': pk}))


# BU Staff
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffBUKpiListView(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Staff_Kpi/staffkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    rejected_count = rejected2_kpi.count() + rejected1_kpi.count()
                    pending_count = pending_kpi.count()

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


# =====================================================================================================================
#                                                 BU KPI
# =====================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpiDashboard(TemplateView):
    template_name = 'toyota_kenya/BU_Kpi/budashboard.html'
    model = bu_kpi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Bu_Kpi/bukpi.html'
    model = bu_kpi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            kpis = []
            for pillar in bsc.objects.all():
                kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms,
                                            bu_kpi_bsc=pillar.bsc_id)
                kpis.append([pillar, kpi])
            kpi = bu_kpi.objects.filter(bu_kpi_bu=staff_person.staff_head_bu, bu_kpi_pms=active_pms,)
            context['my_kpi'] = kpis
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
    template_name = 'toyota_kenya/Bu_Kpi/submitkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        initial['bu_kpi_bu'] = staff_person.staff_head_bu
        initial['bu_kpi_submit_date'] = datetime.date.today()
        initial['bu_kpi_last_edit'] = datetime.date.today()
        initial['bu_kpi_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:BU_Kpi_Submit'))

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

        return HttpResponseRedirect(reverse('toyota_kenya:BU_Kpi_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackBuKpiView(ListView):
    template_name = 'toyota_kenya/Bu_Kpi/trackkpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Bu_Kpi/one_individual_kpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Bu_Kpi/one_individual_kpi_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        initial['bu_kpi_bu'] = staff_person.staff_head_bu
        initial['bu_kpi_submit_date'] = datetime.date.today()
        initial['bu_kpi_last_edit'] = datetime.date.today()
        initial['bu_kpi_status'] = 'Pending'
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:BU_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))

    def form_valid(self, form):
        super(TrackBuKpiEditlView, self).form_valid(form)
        messages.success(self.request, 'BU KPI edited successful')
        return HttpResponseRedirect(reverse('toyota_kenya:BU_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BuKpiResultListView(ListView):
    template_name = 'toyota_kenya/Bu_Kpi/kpiresults.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Bu_Kpi/one_individual_kpi_update.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return HttpResponseRedirect(reverse('toyota_kenya:BU_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:BU_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


# =====================================================================================================================
#                                                 Company KPI
# =====================================================================================================================


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CoKpiDashboard(TemplateView):
    template_name = 'toyota_kenya/Company_Kpi/companydashboard.html'
    model = bu_kpi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Company_Kpi/companykpi.html'
    model = company_kpi

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            kpis = []
            for pillars in bsc.objects.all():
                kpi = company_kpi.objects.filter(company_kpi_pms=active_pms, company_kpi_bsc=pillars.bsc_id)
                kpis.append([pillars, kpi])
            kpi = company_kpi.objects.filter(company_kpi_pms=active_pms)
            context['my_kpi'] = kpis
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
    template_name = 'toyota_kenya/Company_Kpi/submitkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Company_Kpi_Submit'))

    def form_valid(self, form):
        super(SubmitCompanyKpiView, self).form_valid(form)
        messages.success(self.request, 'BU KPI submit successful')

        return HttpResponseRedirect(reverse('toyota_kenya:Company_Kpi_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditCompanyKpiView(ListView):
    template_name = 'toyota_kenya/Company_Kpi/trackkpi.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Company_Kpi/one_individual_kpi_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Company_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))

    def form_valid(self, form):
        super(EditCompanyKpiUpdateView, self).form_valid(form)
        messages.success(self.request, 'Company KPI edited successful')
        return HttpResponseRedirect(reverse('toyota_kenya:Company_Kpi_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class CompanyKpiResultListView(ListView):
    template_name = 'toyota_kenya/Company_Kpi/kpiresults.html'

    def get_queryset(self):
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Company_Kpi/one_individual_kpi_update.html'
    active_pms = pms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return HttpResponseRedirect(reverse('toyota_kenya:Company_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Company_Kpi_Result_Update', kwargs={"pk": self.kwargs["pk"]}))


# ======================================================================================================================
#                                           BUs KPI
# ======================================================================================================================

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsKpiListView(ListView):
    all_bu = bu.objects.all()
    model = individual_Kpi
    template_name = 'toyota_kenya/Bus_Kpi/staffkpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    bu_leader = staff.objects.filter(staff_head_bu=bu)

                    bus_kpi.append([bu.bu_name, approved_kpi.count, pending_count, rejected_count, submitted_count, bu_leader])

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
    template_name = 'toyota_kenya/Bus_Kpi/approvekpi.html'
    all_bu = bu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    bu_leader = staff.objects.filter(staff_head_bu=bu)

                    bus_kpi.append([bu, approved_kpi.count, pending_count, rejected_count, submitted_count, bu_leader])

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
    template_name = 'toyota_kenya/Bus_Kpi/one_individual_approve_kpi.html'
    active_pms = pms
    context_object_name = 'bu'
    all_bu = bu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    bu_heads = staff.objects.filter(staff_head_bu=pk)
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(bu_kpi_status=bu_kpi.status[1][0])
    mds = staff.objects.filter(staff_md='Yes')

    message = "KPI <b>" + kpi.bu_kpi_title + "</b> has been approved"
    for md in mds:
        for buh in bu_heads:
            send_email_pms('KPI Approved', User.objects.get(id=buh.id), User.objects.get(id=md.id), message)

    messages.success(request, 'KPI Approved successful')
    return HttpResponseRedirect(reverse("toyota_kenya:BUs_Approve_Kpi_Detail", kwargs={'pk': pk}))


@login_required
def reject_bu_kpi(request, pk, kpi_id):
    bu_is = get_object_or_404(bu, bu_id=pk)
    bu_heads = staff.objects.filter(staff_head_bu=pk)
    kpi = get_object_or_404(bu_kpi, bu_kpi_id=kpi_id)
    bu_kpi.objects.filter(bu_kpi_id=kpi_id).update(bu_kpi_status=bu_kpi.status[2][0])
    mds = staff.objects.filter(staff_md='Yes')

    message = "KPI <b>" + kpi.bu_kpi_title + "</b> has been Rejected and status has dropped to rejected for your editting"
    for md in mds:
        for buh in bu_heads:
            send_email_pms('KPI Rejected', User.objects.get(id=buh.id), User.objects.get(id=md.id), message)

    messages.success(request, 'KPI Rejected successful')
    return HttpResponseRedirect(reverse("toyota_kenya:BUs_Approve_Kpi_Detail", kwargs={'pk': pk}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class BUsTrackKpiListView(ListView):
    model = bu_kpi
    template_name = 'toyota_kenya/Bus_Kpi/trackkpi.html'
    all_bu = bu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
                    bu_leader = staff.objects.filter(staff_head_bu=bu)

                    bus_kpi.append([bu, approved_kpi.count, pending_count, rejected_count, submitted_count, bu_leader])

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
    template_name = 'toyota_kenya/Bus_Kpi/trackkpi_staff.html'

    all_bu = bu.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            kpis = []
            for pillars in bsc.objects.all():
                kpi = bu_kpi.objects.filter(bu_kpi_bu=self.kwargs['pk'], bu_kpi_pms=active_pms, bu_kpi_bsc=pillars.bsc_id)
                kpis.append([pillars, kpi])
            context['my_kpi'] = kpis
            kpi = bu_kpi.objects.filter(bu_kpi_bu=self.kwargs['pk'], bu_kpi_pms=active_pms,)
            context['approved_kpi'] = kpi.filter(bu_kpi_status='Approved')
            context['pending_kpi'] = kpi.filter(bu_kpi_status='Pending')
            context['edit_kpi'] = kpi.filter(bu_kpi_status='Edit')
            context['rejected_kpi'] = kpi.filter(bu_kpi_status='Rejected')

            context['required_count'] = pms.pms_bu_kpi_number
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
    template_name = 'toyota_kenya/Bus_Kpi/trackkpi_staff_one.html'
    active_pms = pms
    context_object_name = 'staff'
    pk_url_kwarg = 'kpi_id'
    model = bu_kpi

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:BUs_Track_Kpi_BUs_One', kwargs={"pk": self.kwargs["pk"],
                                                                    "kpi_id": self.kwargs["kpi_id"]}))

    def form_valid(self, form):
        super(BUsKpiTrackOneView, self).form_valid(form)
        messages.success(self.request, 'KPI Update successful')
        return HttpResponseRedirect(reverse('toyota_kenya:BUs_Track_Kpi_BUs_One', kwargs={"pk": self.kwargs["pk"],
                                                                             "kpi_id": self.kwargs["kpi_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['the_kpi'] = get_object_or_404(bu_kpi, bu_kpi_id=self.kwargs.get('kpi_id'))
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Check-In/checkin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Check-In/submitci.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Check-In_Submit'))

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

        return HttpResponseRedirect(reverse('toyota_kenya:Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class TrackCheckIn(ListView):
    template_name = 'toyota_kenya/Check-In/trackci.html'

    def get_queryset(self):
        active_pms = get_active_pms()
        return checkIn.objects.filter(checkIn_staff=self.request.user, checkIn_pms=active_pms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Check-In_Submit'))

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

        return HttpResponseRedirect(reverse('toyota_kenya:Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class DetailCheckIn(DetailView):
    model = checkIn
    template_name = 'toyota_kenya/Check-In/one_individual_ci.html'
    context_object_name = 'ci'

    def get_queryset(self):
        active_pms = get_active_pms()
        return checkIn.objects.filter(checkIn_staff=self.request.user, checkIn_pms=active_pms)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Check-In_Submit'))

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

        return HttpResponseRedirect(reverse('toyota_kenya:Check-In_Submit'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class EditCheckIn(UpdateView):
    form_class = SubmitCheckInForm
    template_name = 'toyota_kenya/Check-In/one_individual_ci_edit.html'
    model = checkIn
    context_object_name = 'ci'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Check-In_Submit'))

    def form_valid(self, form):
        super(EditCheckIn, self).form_valid(form)
        messages.success(self.request, 'Checkin edited successful')

        return HttpResponseRedirect(reverse('toyota_kenya:Check-In_Edit_One', kwargs={"pk": self.kwargs["pk"]}))


# ======================================================================================================================
#                                           STAFF CHECKIN
# ======================================================================================================================


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffCheckIn(TemplateView):
    template_name = 'toyota_kenya/Staff_Ci/staffci.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Staff_Ci/approveci.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Staff_Ci/staffcistaff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Staff_Ci/one_individual_approve_ci.html'
    pk_url_kwarg = 'ci_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
        return '{}'.format(reverse('toyota_kenya:Staff_Approve_CI'))

    def form_valid(self, form):
        ci = get_object_or_404(checkIn, checkIn_id=self.kwargs['ci_id'])
        super(StaffApproveStaffCheckInOne, self).form_valid(form)
        messages.success(self.request, 'CheckIn Approved Successfully')
        send_email_pms('CheckIn Confirmed', ci.checkIn_staff, self.request.user,
                       'You Kpi for the month ' + ci.checkIn_month + ' has been confirmed')
        return HttpResponseRedirect(reverse('toyota_kenya:Staff_Approve_CI'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class StaffTrackCheckIn(TemplateView):
    context_object_name = 'staff'
    model = User
    template_name = 'toyota_kenya/Staff_Ci/trackci.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Staff_Ci/trackci_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Staff_Ci/trackci_staff_one.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Assessment/assessment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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

                evals.append([e, s_tl, tl_s, active])

            context['evals'] = evals

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentView(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'toyota_kenya/Assessment/assessment_list.html'

    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
    template_name = 'toyota_kenya/Assessment/assessment_tl_s_view.html'

    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
class AssessmentTlSStaff(CreateView):
    form_class = AssessmentTlSForm
    model = done_tl_evaluates_staff
    template_name = 'toyota_kenya/Assessment/assessment_tl_s.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['staff'] = get_object_or_404(User, id=self.kwargs['s_id'])

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
            context['evaluation'] = e
            questions = question_tl_evaluate_staff.objects.filter(question_evaluation=e).order_by(
                'question_id')

            if questions.count() == 7:
                context['questions'] = questions

            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                          done_staff=context['staff'],
                                                          done_team_leader=self.request.user):
                    ev_done = 'Done'
                    ev_results = done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                        done_staff=context['staff'],
                                                                        done_team_leader=self.request.user)[0]
                    q1 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q1_id)
                    q2 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q2_id)
                    q3 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q3_id)
                    q4 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q4_id)
                    q5 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q5_id)
                    q6 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q6_id)
                    q7 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q7_id)

                    ev_results = [[q1.question, ev_results.score_q1, ev_results.score_q1_comment],
                                  [q2.question, ev_results.score_q2, ev_results.score_q2_comment],
                                  [q3.question, ev_results.score_q3, ev_results.score_q3_comment],
                                  [q4.question, ev_results.score_q4, ev_results.score_q4_comment],
                                  [q5.question, ev_results.score_q5, ev_results.score_q5_comment],
                                  [q6.question, ev_results.score_q6, ev_results.score_q6_comment],
                                  [q7.question, ev_results.score_q7, ev_results.score_q7_comment],
                                  ]
                    context['ev_results'] = ev_results

                else:
                    ev_done = "Not Done"

                context['ev_done'] = ev_done

        return context

    def get_initial(self):
        staff_u = get_object_or_404(User, id=self.kwargs['s_id'])
        eval = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        questions = question_tl_evaluate_staff.objects.filter(question_evaluation=eval).order_by('question_id')

        initial = super(AssessmentTlSStaff, self).get_initial()
        initial['done_evaluation'] = eval
        initial['done_staff'] = staff_u
        initial['done_team_leader'] = self.request.user
        if questions.count() == 7:
            initial['done_q1'] = questions[0]
            initial['done_q2'] = questions[1]
            initial['done_q3'] = questions[2]
            initial['done_q4'] = questions[3]
            initial['done_q5'] = questions[4]
            initial['done_q6'] = questions[5]
            initial['done_q7'] = questions[6]
        return initial

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Assessment_S', kwargs={"as_id": self.kwargs["as_id"]}))

    def form_valid(self, form):
        super(AssessmentTlSStaff, self).form_valid(form)
        messages.success(self.request, 'Evaluated staff success')

        return HttpResponseRedirect(reverse('toyota_kenya:Assessment_S', kwargs={"as_id": self.kwargs["as_id"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentSTlStaff(CreateView):
    form_class = AsssessmentSTlForm
    model = done_staff_evaluates_tl
    template_name = 'toyota_kenya/Assessment/assessment_s_tl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['staff'] = get_object_or_404(User, id=self.kwargs['tl_id'])

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
            context['evaluation'] = e
            questions = question_staff_evaluate_tl.objects.filter(question_evaluation=e).order_by(
                'question_id')
            if questions.count() == 7:
                context['questions'] = questions
            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                if done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                          done_staff=self.request.user,
                                                          done_team_leader=context['staff']):
                    ev_done = 'Done'
                    ev_results = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                        done_team_leader=context['staff'],
                                                                        done_staff=self.request.user)[0]
                    q1 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q1_id)
                    q2 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q2_id)
                    q3 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q3_id)
                    q4 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q4_id)
                    q5 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q5_id)
                    q6 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q6_id)
                    q7 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q7_id)

                    ev_results = [[q1.question, ev_results.score_q1, ev_results.score_q1_comment],
                                  [q2.question, ev_results.score_q2, ev_results.score_q2_comment],
                                  [q3.question, ev_results.score_q3, ev_results.score_q3_comment],
                                  [q4.question, ev_results.score_q4, ev_results.score_q4_comment],
                                  [q5.question, ev_results.score_q5, ev_results.score_q5_comment],
                                  [q6.question, ev_results.score_q6, ev_results.score_q6_comment],
                                  [q7.question, ev_results.score_q7, ev_results.score_q7_comment],
                                  ]
                    context['ev_results'] = ev_results

                else:
                    ev_done = "Not Done"

                context['ev_done'] = ev_done

        return context

    def get_initial(self):
        staff_u = get_object_or_404(User, id=self.kwargs['tl_id'])
        eval = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        questions = question_staff_evaluate_tl.objects.filter(question_evaluation=eval).order_by('question_id')

        initial = super(AssessmentSTlStaff, self).get_initial()
        initial['done_evaluation'] = eval
        initial['done_team_leader'] = staff_u
        initial['done_staff'] = self.request.user
        if questions.count() == 7:
            initial['done_q1'] = questions[0]
            initial['done_q2'] = questions[1]
            initial['done_q3'] = questions[2]
            initial['done_q4'] = questions[3]
            initial['done_q5'] = questions[4]
            initial['done_q6'] = questions[5]
            initial['done_q7'] = questions[6]
        return initial

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Assessment_TL_One', kwargs={"as_id": self.kwargs["as_id"], "tl_id": self.kwargs["tl_id"]}))

    def form_valid(self, form):
        super(AssessmentSTlStaff, self).form_valid(form)
        messages.success(self.request, 'Evaluated staff success')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Assessment_S', kwargs={"as_id": self.kwargs["as_id"], "tl_id": self.kwargs["tl_id"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentPrevious(TemplateView):
    template_name = 'toyota_kenya/Assessment/assessment_previous.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            for e in context['completed_evaluations']:

                # TL evaluates Staff
                # =====================================================================

                s_tl = "N/A"
                tl_s = "N/A"

                if e.evaluation_start_date <= today <= e.evaluation_end_date:
                    active = True
                else:
                    active = False
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

                evals.append([e, s_tl, tl_s, active])

            context['evals'] = evals

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentPreviousView(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'toyota_kenya/Assessment/assessment_previous_list.html'

    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
class AssessmentSTlStaffPrevious(TemplateView):
    template_name = 'toyota_kenya/Assessment/assessment_s_tl_previous.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['staff'] = get_object_or_404(User, id=self.kwargs['tl_id'])

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
            context['evaluation'] = e
            questions = question_staff_evaluate_tl.objects.filter(question_evaluation=e).order_by(
                'question_id')
            if questions.count() == 7:
                context['questions'] = questions
            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                if done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                          done_staff=self.request.user,
                                                          done_team_leader=context['staff']):
                    ev_done = 'Done'
                    ev_results = done_staff_evaluates_tl.objects.filter(done_evaluation=e.evaluation_id,
                                                                        done_team_leader=context['staff'],
                                                                        done_staff=self.request.user)[0]
                    q1 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q1_id)
                    q2 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q2_id)
                    q3 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q3_id)
                    q4 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q4_id)
                    q5 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q5_id)
                    q6 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q6_id)
                    q7 = get_object_or_404(question_staff_evaluate_tl, question_id=ev_results.done_q7_id)

                    ev_results = [[q1.question, ev_results.score_q1, ev_results.score_q1_comment],
                                  [q2.question, ev_results.score_q2, ev_results.score_q2_comment],
                                  [q3.question, ev_results.score_q3, ev_results.score_q3_comment],
                                  [q4.question, ev_results.score_q4, ev_results.score_q4_comment],
                                  [q5.question, ev_results.score_q5, ev_results.score_q5_comment],
                                  [q6.question, ev_results.score_q6, ev_results.score_q6_comment],
                                  [q7.question, ev_results.score_q7, ev_results.score_q7_comment],
                                  ]
                    context['ev_results'] = ev_results

                else:
                    ev_done = "Not Done"

                context['ev_done'] = ev_done

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AssessmentTlSStaffPrevious(DetailView):
    context_object_name = 'evaluation'
    model = evaluation
    template_name = 'toyota_kenya/Assessment/assessment_tl_s_view_previous.html'

    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
class AssessmentTlSPreviousStaff(TemplateView):
    template_name = 'toyota_kenya/Assessment/assessment_tl_s_previous.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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
            context['staff'] = get_object_or_404(User, id=self.kwargs['s_id'])

            today = datetime.date.today()
            context['today'] = today
            e = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
            context['evaluation'] = e
            questions = question_tl_evaluate_staff.objects.filter(question_evaluation=e).order_by(
                'question_id')

            if questions.count() == 7:
                context['questions'] = questions

            s_tl = "N/A"
            tl_s = "N/A"

            evals = []
            if context['user_is_tl'] is not None:
                if done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                          done_staff=context['staff'],
                                                          done_team_leader=self.request.user):
                    ev_done = 'Done'
                    ev_results = done_tl_evaluates_staff.objects.filter(done_evaluation=e.evaluation_id,
                                                                        done_staff=context['staff'],
                                                                        done_team_leader=self.request.user)[0]
                    q1 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q1_id)
                    q2 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q2_id)
                    q3 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q3_id)
                    q4 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q4_id)
                    q5 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q5_id)
                    q6 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q6_id)
                    q7 = get_object_or_404(question_tl_evaluate_staff, question_id=ev_results.done_q7_id)

                    ev_results = [[q1.question, ev_results.score_q1, ev_results.score_q1_comment],
                                  [q2.question, ev_results.score_q2, ev_results.score_q2_comment],
                                  [q3.question, ev_results.score_q3, ev_results.score_q3_comment],
                                  [q4.question, ev_results.score_q4, ev_results.score_q4_comment],
                                  [q5.question, ev_results.score_q5, ev_results.score_q5_comment],
                                  [q6.question, ev_results.score_q6, ev_results.score_q6_comment],
                                  [q7.question, ev_results.score_q7, ev_results.score_q7_comment],
                                  ]
                    context['ev_results'] = ev_results

                else:
                    ev_done = "Not Done"

                context['ev_done'] = ev_done

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminDashboard(TemplateView):
    template_name = 'toyota_kenya/Admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBU(TemplateView):
    template_name = 'toyota_kenya/Admin/admin_bu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()

        bu_n_l = []
        bus = bu.objects.all()
        for bu_u in bus:
            bu_l = staff.objects.filter(staff_head_bu=bu_u.bu_id)
            bu_n_l.append([bu_u, bu_l])

        context['bu_n_l'] = bu_n_l

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBUOne(UpdateView):
    template_name = 'toyota_kenya/Admin/admin_bu_one.html'
    form_class = BUForm
    model = bu
    pk_url_kwarg = 'bu_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['bu_members'] = staff.objects.filter(staff_bu=self.kwargs['bu_id'])
        context['bu_head'] = staff.objects.filter(staff_head_bu=self.kwargs['bu_id'])
        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_BUs'))

    def form_valid(self, form):
        super(AdminBUOne, self).form_valid(form)
        messages.success(self.request, 'BU updated Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_BUs'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminBUNew(CreateView):
    template_name = 'toyota_kenya/Admin/admin_bu_new.html'
    form_class = BUForm
    model = bu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_BUs'))

    def form_valid(self, form):
        super(AdminBUNew, self).form_valid(form)
        messages.success(self.request, 'BU updated Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_BUs'))



@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminTeam(TemplateView):
    template_name = 'toyota_kenya/Admin/admin_team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()

        team_n_l = []
        teams = team.objects.all()
        for t in teams:
            tl = staff.objects.filter(staff_head_team=t.team_id)
            team_n_l.append([t, tl])

        context['team_n_l'] = team_n_l

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminTeamOne(UpdateView):
    template_name = 'toyota_kenya/Admin/admin_team_one.html'
    form_class = TeamForm
    model = team
    pk_url_kwarg = 't_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['team_members'] = staff.objects.filter(staff_team=self.kwargs['t_id'])
        context['team_head'] = staff.objects.filter(staff_head_team=self.kwargs['t_id'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Teams'))

    def form_valid(self, form):
        super(AdminTeamOne, self).form_valid(form)
        messages.success(self.request, 'Team Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Teams'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminTeamNew(CreateView):
    template_name = 'toyota_kenya/Admin/admin_team_new.html'
    form_class = TeamForm
    model = team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Teams'))

    def form_valid(self, form):
        super(AdminTeamNew, self).form_valid(form)
        messages.success(self.request, 'Team Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Teams'))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUser(TemplateView):
    template_name = 'toyota_kenya/Admin/admin_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserNew(CreateView):
    model = User
    form_class = UserCreationForm

    template_name = 'toyota_kenya/Admin/admin_users_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        return context


@login_required
def new_user(request):
    if request.user.is_superuser:
        context = {}
        staff_person = get_object_or_404(staff, id=request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_New_Details', kwargs={'pk': user.id}))
        else:
            form = UserCreationForm()
        context['form'] = form
        return render(request, 'toyota_kenya/Admin/admin_users_new.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserNewDetails(UpdateView):
    model = UserModel
    form_class = UserForm
    template_name = 'toyota_kenya/Admin/admin_users_new_details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Users_New_Details_Staff', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(AdminUserNewDetails, self).form_valid(form)
        messages.success(self.request, 'User updated Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_New_Details_Staff', kwargs={'pk': self.kwargs['pk']}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserNewDetailsStaff(CreateView):
    model = staff
    form_class = StaffForm
    template_name = 'toyota_kenya/Admin/admin_users_new_details_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(User, id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Users', ))

    def form_valid(self, form):
        super(AdminUserNewDetailsStaff, self).form_valid(form)
        messages.success(self.request, 'Staff record created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users'))

    def get_initial(self):
        initial = super(AdminUserNewDetailsStaff, self).get_initial()
        initial['staff_person'] = get_object_or_404(User, id=self.kwargs['pk'])
        return initial


@login_required
def new_user_details(request, pk):
    if request.user.is_superuser:
        context = {}
        staff_person = get_object_or_404(staff, id=request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        staff_u = User.objects.get(pk=pk)

        if request.method == 'POST':
            form = UserForm(staff_u, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_reset_password', kwargs={'pk': user.id}))
        else:
            form = UserForm(User.objects.filter(id=pk).first())
        context['form'] = form
        return render(request, 'toyota_kenya/Admin/admin_users_new_details.html', context)


@login_required
def change_password(request, pk):
    if request.user.is_superuser:
        context = {}
        staff_person = get_object_or_404(staff, id=request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        staff_u = User.objects.get(id=pk)
        context['staff_u'] = staff_u

        if request.method == 'POST':
            form = SetPasswordForm(staff_u, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_reset_password', kwargs={'pk': pk}))
        else:
            form = SetPasswordForm(staff_u)
        context['form'] = form
        return render(request, 'toyota_kenya/Admin/admin_users_reset_password.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminResetPasswordUser(UpdateView):
    model = User
    form_class = PasswordSet
    template_name = 'toyota_kenya/Admin/admin_users_reset_password.html'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        return get_object_or_404(User, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['staff_active'] = staff.objects.filter(staff_person__is_active=True)
        context['staff_tl'] = staff.objects.exclude(staff_head_team__isnull=True)
        context['staff_bu_heads'] = staff.objects.exclude(staff_head_bu__isnull=True)
        context['staff_md'] = staff.objects.exclude(staff_md='No')
        context['pms'] = pms.objects.all()
        context['teams'] = team.objects.all()
        context['bus'] = bu.objects.all()

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserOne(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'toyota_kenya/Admin/admin_users_one.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['pk'])

        return context


@login_required
def deactivate_account_dashboard(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=pk)
        user.is_active = False
        user.save()

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users'))


@login_required
def activate_account_dashboard(request, pk):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=pk)
        user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users'))


@login_required
def reset_user_password(request, pk):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('toyota_kenya:password_reset_confirm',
                                            kwargs={'uidb64': urlsafe_base64_encode(force_bytes(pk)),
                                                    'token': default_token_generator.make_token(
                                                        get_object_or_404(User, id=pk))}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserOneEditUser(UpdateView):
    model = UserModel
    form_class = UserForm
    template_name = 'toyota_kenya/Admin/admin_users_one_edit_user.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Users_One', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(AdminUserOneEditUser, self).form_valid(form)
        messages.success(self.request, 'User updated Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_One', kwargs={'pk': self.kwargs['pk']}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AdminUserOneEditStaff(UpdateView):
    model = staff
    form_class = StaffForm
    template_name = 'toyota_kenya/Admin/admin_users_one_edit_staff.html'
    context_object_name = 'staff'

    def get_object(self, queryset=None):
        return get_object_or_404(staff, staff_person=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Users_One', kwargs={'pk': self.kwargs['pk']}))

    def form_valid(self, form):
        super(AdminUserOneEditStaff, self).form_valid(form)
        messages.success(self.request, 'User updated Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Users_One', kwargs={'pk': self.kwargs['pk']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMS(DetailView):
    model = pms
    template_name = 'toyota_kenya/Admin/pms.html'
    pk_url_kwarg = 'pms_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSEdit(UpdateView):
    model = pms
    form_class = PmsForm
    template_name = 'toyota_kenya/Admin/pms_edit.html'
    pk_url_kwarg = 'pms_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()

        return context

    def form_valid(self, form):
        super(AdminPMSEdit, self).form_valid(form)
        messages.success(self.request, 'PMS Edited Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS', kwargs={"pms_id": self.kwargs["pms_id"]}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSNew(CreateView):
    model = pms
    form_class = PmsForm
    template_name = 'toyota_kenya/Admin/pms_new.html'
    pk_url_kwarg = 'pms_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_Dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()

        return context

    def form_valid(self, form):
        super(AdminPMSNew, self).form_valid(form)
        messages.success(self.request, 'PMS Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_Dashboard'))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSStaff(ListView):
    model = staff
    template_name = 'toyota_kenya/Admin/pms_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSStaffOne(DetailView):
    template_name = 'toyota_kenya/Admin/pms_staff_one.html'

    def get_object(self, queryset=None):
        return get_object_or_404(staff, staff_person=self.kwargs['s_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSStaffOneEdit(UpdateView):
    template_name = 'toyota_kenya/Admin/pms_staff_edit.html'
    form_class = StaffForm
    form_class2 = UserForm

    def get_context_data(self, **kwargs):
        context = super(AdminPMSStaffOneEdit, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.form_class2()
        return context

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['s_id'])


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSIndividual(ListView):
    model = staff
    template_name = 'toyota_kenya/Admin/pms_ind_kpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        staff_n_kpi = []

        approved_count = rejected_count = pending_count = 0

        for staff_u in context['staff']:
            kpi = individual_Kpi.objects.filter(individual_kpi_pms=self.kwargs['pms_id'],
                                                individual_kpi_user=staff_u.staff_person.id)
            approved2_kpi = kpi.filter(individual_kpi_status='Approved 2')
            approved1_kpi = kpi.filter(individual_kpi_status='Approved 1')
            pending_kpi = kpi.filter(individual_kpi_status='Pending')
            rejected_kpi = kpi.filter(individual_kpi_status='Rejected 2')

            approved_count += approved2_kpi.count()
            pending_count += (approved1_kpi.count() + pending_kpi.count())
            rejected_count += rejected_kpi.count()

            staff_n_kpi.append([staff_u, kpi, approved2_kpi, approved1_kpi, pending_kpi, rejected_kpi])

        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        context['approve_count'] = approved_count
        context['pending_count'] = pending_count
        context['rejected_count'] = rejected_count
        context['staff_n_kpi'] = staff_n_kpi

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSIndividualStaff(ListView):
    model = individual_Kpi
    template_name = 'toyota_kenya/Admin/pms_ind_kpi_staff.html'
    context_object_name = 'individual_kpi'

    def get_queryset(self):
        return individual_Kpi.objects.filter(individual_kpi_user=self.kwargs['s_id'],
                                             individual_kpi_pms=self.kwargs['pms_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSIndividualStaffOne(UpdateView):
    model = individual_Kpi
    form_class = IndividualKpiForm
    template_name = 'toyota_kenya/Admin/pms_ind_kpi_staff_one.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Individual_Staff_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                           'kpi_id': self.kwargs['kpi_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSIndividualStaffOne, self).form_valid(form)
        messages.success(self.request, 'KPI Editted Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Individual_Staff_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                                    'kpi_id': self.kwargs['kpi_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSIndividualStaffNew(CreateView):
    model = individual_Kpi
    form_class = IndividualKpiForm
    template_name = 'toyota_kenya/Admin/pms_ind_kpi_staff_new.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Individual_Staff',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSIndividualStaffNew, self).form_valid(form)
        messages.success(self.request, 'KPI Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Individual_Staff',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_initial(self):
        initial = super(AdminPMSIndividualStaffNew, self).get_initial()
        initial['individual_kpi_pms'] = self.kwargs['pms_id']
        initial['individual_kpi_user'] = self.kwargs['s_id']
        initial['individual_kpi_submit_date'] = datetime.date.today()

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSBU(ListView):
    model = staff
    template_name = 'toyota_kenya/Admin/pms_bu_kpi.html'
    queryset = staff.objects.exclude(staff_head_bu=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.exclude(staff_head_bu=None)
        staff_n_kpi = []

        approved_count = rejected_count = pending_count = 0

        for staff_u in context['staff']:
            kpi = bu_kpi.objects.filter(bu_kpi_pms=self.kwargs['pms_id'], bu_kpi_bu=staff_u.staff_head_bu)
            approved_kpi = kpi.filter(bu_kpi_status='Approved')
            pending_kpi = kpi.filter(bu_kpi_status='Pending')
            rejected_kpi = kpi.filter(bu_kpi_status='Rejected')

            approved_count += approved_kpi.count()
            pending_count += pending_kpi.count()
            rejected_count += rejected_kpi.count()

            staff_n_kpi.append([staff_u, kpi, approved_kpi, pending_kpi, rejected_kpi])

        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        context['approve_count'] = approved_count
        context['pending_count'] = pending_count
        context['rejected_count'] = rejected_count
        context['staff_n_kpi'] = staff_n_kpi

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSBUStaff(ListView):
    model = bu_kpi
    template_name = 'toyota_kenya/Admin/pms_bu_kpi_staff.html'
    context_object_name = 'bu_kpi'

    def get_queryset(self):
        staff_u = get_object_or_404(staff, staff_person=self.kwargs['s_id'])
        return bu_kpi.objects.filter(bu_kpi_bu=staff_u.staff_head_bu, bu_kpi_pms=self.kwargs['pms_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSBUStaffOne(UpdateView):
    model = bu_kpi
    form_class = BUKpiForm
    template_name = 'toyota_kenya/Admin/pms_bu_kpi_staff_one.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_BU_Staff_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                           'kpi_id': self.kwargs['kpi_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSBUStaffOne, self).form_valid(form)
        messages.success(self.request, 'KPI Editted Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_BU_Staff_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                                    'kpi_id': self.kwargs['kpi_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSBUStaffNew(CreateView):
    model = bu_kpi
    form_class = BUKpiForm
    template_name = 'toyota_kenya/Admin/pms_bu_kpi_staff_new.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_BU_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSBUStaffNew, self).form_valid(form)
        messages.success(self.request, 'KPI Created Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_BU_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_initial(self):
        staff_u = get_object_or_404(staff, staff_person=self.kwargs['s_id'])
        initial = super(AdminPMSBUStaffNew, self).get_initial()
        initial['bu_kpi_pms'] = self.kwargs['pms_id']
        initial['bu_kpi_bu'] = staff_u.staff_head_bu
        initial['bu_kpi_submit_date'] = datetime.date.today()

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCompany(ListView):
    model = company_kpi
    template_name = 'toyota_kenya/Admin/pms_company_kpi.html'
    context_object_name = 'company_kpi'

    def get_queryset(self):
        return company_kpi.objects.filter(company_kpi_pms=self.kwargs['pms_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCompanyOne(UpdateView):
    model = company_kpi
    form_class = CompanyKpiForm
    template_name = 'toyota_kenya/Admin/pms_company_kpi_one.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Company_One', kwargs={"pms_id": self.kwargs["pms_id"], 'kpi_id': self.kwargs['kpi_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def form_valid(self, form):
        super(AdminPMSCompanyOne, self).form_valid(form)
        messages.success(self.request, 'KPI Editted Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Company_One', kwargs={"pms_id": self.kwargs["pms_id"], 'kpi_id': self.kwargs['kpi_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCompanyNew(CreateView):
    model = company_kpi
    form_class = CompanyKpiForm
    template_name = 'toyota_kenya/Admin/pms_company_kpi_new.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Company', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def form_valid(self, form):
        super(AdminPMSCompanyNew, self).form_valid(form)
        messages.success(self.request, 'KPI Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Company', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_initial(self):
        initial = super(AdminPMSCompanyNew, self).get_initial()
        initial['company_kpi_pms'] = self.kwargs['pms_id']
        initial['company_kpi_submit_date'] = datetime.date.today()

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckIn(ListView):
    model = staff
    template_name = 'toyota_kenya/Admin/pms_checkin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        staff_n_ci = []

        approved_count = rejected_count = pending_count = 0

        for staff_u in context['staff']:
            ci = checkIn.objects.filter(checkIn_pms=self.kwargs['pms_id'], checkIn_staff=staff_u.staff_person.id)
            approved_ci = ci.filter(checkIn_status='Confirmed')
            pending_ci = ci.filter(checkIn_status='Pending')
            rejected_ci = ci.filter(checkIn_status='Rejected')

            approved_count += approved_ci.count()
            pending_count += pending_ci.count()
            rejected_count += rejected_ci.count()

            staff_n_ci.append([staff_u, ci, approved_ci, pending_ci, rejected_ci])

        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        context['approve_count'] = approved_count
        context['pending_count'] = pending_count
        context['rejected_count'] = rejected_count
        context['staff_n_ci'] = staff_n_ci
        context['checkin_matrix'] = matrix_checkin.objects.filter(matrix_pms=context['pms'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInScoreNew(CreateView):
    model = matrix_checkin
    form_class = MatrixCheckIn
    template_name = 'toyota_kenya/Admin/pms_checkin_score_new.html'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_CheckIn', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['checkin_matrix'] = matrix_checkin.objects.filter(matrix_pms=context['pms'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInScoreNew, self).form_valid(form)
        messages.success(self.request, 'CheckIn Score Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_CheckIn', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_initial(self):
        initial = super(AdminPMSCheckInScoreNew, self).get_initial()
        initial['matrix_pms'] = self.kwargs['pms_id']

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInScoreOne(UpdateView):
    model = matrix_checkin
    form_class = MatrixCheckIn
    template_name = 'toyota_kenya/Admin/pms_checkin_score_one.html'
    pk_url_kwarg = 'm_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_CheckIn', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['checkin_matrix'] = matrix_checkin.objects.filter(matrix_pms=context['pms'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInScoreOne, self).form_valid(form)
        messages.success(self.request, 'CheckIn Score Created Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_CheckIn', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_initial(self):
        initial = super(AdminPMSCheckInScoreOne, self).get_initial()
        initial['matrix_pms'] = self.kwargs['pms_id']

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInStaff(ListView):
    model = checkIn
    template_name = 'toyota_kenya/Admin/pms_checkin_staff.html'
    context_object_name = 'checkIn'

    def get_queryset(self):
        return checkIn.objects.filter(checkIn_staff=self.kwargs['s_id'], checkIn_pms=self.kwargs['pms_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInStaffOne(UpdateView):
    model = checkIn
    form_class = CheckInForm
    template_name = 'toyota_kenya/Admin/pms_checkin_staff_one.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_CheckIn_Staff_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                           'kpi_id': self.kwargs['kpi_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInStaffOne, self).form_valid(form)
        messages.success(self.request, 'CheckIn Editted Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_CheckIn_Staff_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                                    'kpi_id': self.kwargs['kpi_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInStaffNew(CreateView):
    model = checkIn
    form_class = CheckInForm
    template_name = 'toyota_kenya/Admin/pms_checkin_staff_new.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_CheckIn_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInStaffNew, self).form_valid(form)
        messages.success(self.request, 'CheckIn Created Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_CheckIn_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_initial(self):
        initial = super(AdminPMSCheckInStaffNew, self).get_initial()
        initial['checkIn_pms'] = self.kwargs['pms_id']
        initial['checkIn_staff'] = self.kwargs['s_id']
        initial['checkIn_submit_date'] = datetime.date.today()

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessment(ListView):
    model = evaluation
    template_name = 'toyota_kenya/Admin/pms_assessment.html'
    context_object_name = 'evaluation'

    def get_queryset(self):
        return evaluation.objects.filter(evaluation_pms=self.kwargs['pms_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = staff.objects.all()
        staff_n_ci = []

        approved_count = rejected_count = pending_count = 0

        for staff_u in context['staff']:
            ci = checkIn.objects.filter(checkIn_pms=self.kwargs['pms_id'], checkIn_staff=staff_u.staff_person.id)
            approved_ci = ci.filter(checkIn_status='Confirmed')
            pending_ci = ci.filter(checkIn_status='Pending')
            rejected_ci = ci.filter(checkIn_status='Rejected')

            approved_count += approved_ci.count()
            pending_count += pending_ci.count()
            rejected_count += rejected_ci.count()

            staff_n_ci.append([staff_u, ci, approved_ci, pending_ci, rejected_ci])

        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        context['approve_count'] = approved_count
        context['pending_count'] = pending_count
        context['rejected_count'] = rejected_count
        context['staff_n_ci'] = staff_n_ci

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOne(UpdateView):
    model = evaluation
    form_class = AssessmentForm
    template_name = 'toyota_kenya/Admin/pms_assessment_one.html'
    context_object_name = 'evaluation'
    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation_responses'] = evaluation_responses.objects.filter(response_evaluation=self.kwargs['as_id'])
        context['s_tl_questions'] = question_staff_evaluate_tl.objects.filter(question_evaluation=self.kwargs['as_id'])
        context['tl_s_questions'] = question_tl_evaluate_staff.objects.filter(question_evaluation=self.kwargs['as_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSAssessmentOne, self).form_valid(form)
        messages.success(self.request, 'Assessment Edited Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentNew(CreateView):
    model = evaluation
    form_class = AssessmentForm
    template_name = 'toyota_kenya/Admin/pms_assessment_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        return context

    def form_valid(self, form):
        super(AdminPMSAssessmentNew, self).form_valid(form)
        messages.success(self.request, 'Assessment Edited Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment', kwargs={"pms_id": self.kwargs["pms_id"]}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseNew(CreateView):
    model = evaluation_responses
    form_class = MatrixAssessment
    template_name = 'toyota_kenya/Admin/pms_assessment_one_response_new.html'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSAssessmentOneResponseNew, self).form_valid(form)
        messages.success(self.request, 'Score Matrix')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"],
                                                    'as_id': self.kwargs['as_id']}))

    def get_initial(self):
        initial = super(AdminPMSAssessmentOneResponseNew, self).get_initial()
        initial['response_evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseOne(UpdateView):
    model = evaluation_responses
    form_class = MatrixAssessment
    template_name = 'toyota_kenya/Admin/pms_assessment_one_response_one.html'
    pk_url_kwarg = 'm_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSAssessmentOneResponseOne, self).form_valid(form)
        messages.success(self.request, 'Score Matrix')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"],
                                                    'as_id': self.kwargs['as_id']}))

    def get_initial(self):
        initial = super(AdminPMSAssessmentOneResponseOne, self).get_initial()
        initial['response_evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneQuestionOneTlS(UpdateView):
    model = question_tl_evaluate_staff
    form_class = QuestionTlSForm
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_one_tl_s.html'
    context_object_name = 'question'
    pk_url_kwarg = 'q_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        context['s_tl_questions'] = question_staff_evaluate_tl.objects.filter(question_evaluation=self.kwargs['as_id'])
        context['tl_s_questions'] = question_tl_evaluate_staff.objects.filter(question_evaluation=self.kwargs['as_id'])

        def form_valid(self, form):
            super(AdminPMSAssessmentOneQuestionOneTlS, self).form_valid(form)
            messages.success(self.request, 'Question Edited Successfully')

            return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                                kwargs={"pms_id": self.kwargs["pms_id"],
                                                        'as_id': self.kwargs['as_id']}))

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneQuestionNewTlS(CreateView):
    model = question_tl_evaluate_staff
    form_class = QuestionTlSForm
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_one_tl_s.html'
    context_object_name = 'question'
    pk_url_kwarg = 'q_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        context['s_tl_questions'] = question_staff_evaluate_tl.objects.filter(question_evaluation=self.kwargs['as_id'])
        context['tl_s_questions'] = question_tl_evaluate_staff.objects.filter(question_evaluation=self.kwargs['as_id'])

        def form_valid(self, form):
            super(AdminPMSAssessmentOneQuestionOneTlS, self).form_valid(form)
            messages.success(self.request, 'Question Edited Successfully')

            return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                                kwargs={"pms_id": self.kwargs["pms_id"],
                                                        'as_id': self.kwargs['as_id']}))

        return context

    def get_initial(self):
        initial = super(AdminPMSAssessmentOneQuestionNewTlS, self).get_initial()
        initial['question_evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneQuestionOneSTl(UpdateView):
    model = question_staff_evaluate_tl
    form_class = QuestionSTlForm
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_one_s_tl.html'
    context_object_name = 'question'
    pk_url_kwarg = 'q_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        context['s_tl_questions'] = question_staff_evaluate_tl.objects.filter(question_evaluation=self.kwargs['as_id'])
        context['tl_s_questions'] = question_tl_evaluate_staff.objects.filter(question_evaluation=self.kwargs['as_id'])

        def form_valid(self, form):
            super(AdminPMSAssessmentOneQuestionOneSTl, self).form_valid(form)
            messages.success(self.request, 'Question Edited Successfully')

            return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                                kwargs={"pms_id": self.kwargs["pms_id"],
                                                        'as_id': self.kwargs['as_id']}))

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneQuestionNewSTl(CreateView):
    model = question_staff_evaluate_tl
    form_class = QuestionSTlForm
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_new_s_tl.html'
    context_object_name = 'question'
    pk_url_kwarg = 'q_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        context['s_tl_questions'] = question_staff_evaluate_tl.objects.filter(question_evaluation=self.kwargs['as_id'])
        context['tl_s_questions'] = question_tl_evaluate_staff.objects.filter(question_evaluation=self.kwargs['as_id'])

        def form_valid(self, form):
            super(AdminPMSAssessmentOneQuestionNewSTl, self).form_valid(form)
            messages.success(self.request, 'Question Added Successfully')

            return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One',
                                                kwargs={"pms_id": self.kwargs["pms_id"],
                                                        'as_id': self.kwargs['as_id']}))

        return context

    def get_initial(self):
        initial = super(AdminPMSAssessmentOneQuestionNewSTl, self).get_initial()
        initial['question_evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])
        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseSTl(DetailView):
    model = evaluation
    template_name = 'toyota_kenya/Admin/pms_assessment_one_stl.html'
    context_object_name = 'evaluation'
    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        staffs = staff.objects.all()
        staffs_u = []
        for staff_u in staffs:
            user = get_object_or_404(User, id=staff_u.staff_person.id)
            done = done_staff_evaluates_tl.objects.filter(done_evaluation_id=self.kwargs['as_id'],
                                                          done_staff_id=staff_u.staff_person.id)
            tl = None
            if done:
                done = done.first()
                if done.done_team_leader_id:
                    tl = get_object_or_404(User, id=done.done_team_leader_id)

            staffs_u.append([user, tl, done])

        context['staff_n_res'] = staffs_u
        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseSTlOne(UpdateView):
    model = done_staff_evaluates_tl
    form_class = DoneStaffEvaluateTl
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_one_s_tl_one.html'
    context_object_name = 'done'
    pk_url_kwarg = 'd_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One_STl_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id'],
                                           'd_id': self.kwargs['d_id'], }))

    def form_valid(self, form):
        super(AdminPMSAssessmentOneResponseSTlOne, self).form_valid(form)
        messages.success(self.request, 'Assessment Edited Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One_STl_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id'],
                                                    'd_id': self.kwargs['d_id'], }))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseTlS(DetailView):
    model = evaluation
    template_name = 'toyota_kenya/Admin/pms_assessment_one_tls.html'
    context_object_name = 'evaluation'
    pk_url_kwarg = 'as_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        staffs = staff.objects.all()
        staffs_u = []
        for staff_u in staffs:
            user = get_object_or_404(User, id=staff_u.staff_person.id)
            done = done_tl_evaluates_staff.objects.filter(done_evaluation_id=self.kwargs['as_id'],
                                                          done_staff_id=staff_u.staff_person.id)
            tl = None
            if done:
                done = done.first()
                if done.done_team_leader_id:
                    tl = get_object_or_404(User, id=done.done_team_leader_id)

            staffs_u.append([user, tl, done])

        context['staff_n_res'] = staffs_u
        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSAssessmentOneResponseTlSOne(UpdateView):
    model = done_tl_evaluates_staff
    form_class = DoneTlEvaluateStaff
    template_name = 'toyota_kenya/Admin/pms_assessment_one_question_one_tl_s_one.html'
    context_object_name = 'done'
    pk_url_kwarg = 'd_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['evaluation'] = get_object_or_404(evaluation, evaluation_id=self.kwargs['as_id'])

        return context

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_Assessment_One_TlS_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id'],
                                           'd_id': self.kwargs['d_id'], }))

    def form_valid(self, form):
        super(AdminPMSAssessmentOneResponseTlSOne, self).form_valid(form)
        messages.success(self.request, 'Assessment Edited Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_Assessment_One_TlS_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 'as_id': self.kwargs['as_id'],
                                                    'd_id': self.kwargs['d_id'], }))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInStaffOne(UpdateView):
    model = checkIn
    form_class = CheckInForm
    template_name = 'toyota_kenya/Admin/pms_checkin_staff_one.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(reverse('toyota_kenya:Admin_PMS_CheckIn_Staff_One',
                                   kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                           'kpi_id': self.kwargs['kpi_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInStaffOne, self).form_valid(form)
        messages.success(self.request, 'CheckIn Editted Successfully')

        return HttpResponseRedirect(reverse('toyota_kenya:Admin_PMS_CheckIn_Staff_One',
                                            kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id'],
                                                    'kpi_id': self.kwargs['kpi_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSCheckInStaffNew(CreateView):
    model = checkIn
    form_class = CheckInForm
    template_name = 'toyota_kenya/Admin/pms_checkin_staff_new.html'
    pk_url_kwarg = 'kpi_id'

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_CheckIn_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.kwargs['s_id'])

        return context

    def form_valid(self, form):
        super(AdminPMSCheckInStaffNew, self).form_valid(form)
        messages.success(self.request, 'CheckIn Created Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_CheckIn_Staff', kwargs={"pms_id": self.kwargs["pms_id"], 's_id': self.kwargs['s_id']}))

    def get_initial(self):
        initial = super(AdminPMSCheckInStaffNew, self).get_initial()
        initial['checkIn_pms'] = self.kwargs['pms_id']
        initial['checkIn_staff'] = self.kwargs['s_id']
        initial['checkIn_submit_date'] = datetime.date.today()

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class Matrix(TemplateView):
    template_name = 'toyota_kenya/Admin/pms_matrix.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixScore(UpdateView):
    model = score_matrix
    form_class = MatrixScore
    context_object_name = 'one_matrix'
    template_name = 'toyota_kenya/Admin/pms_matrix_score.html'
    pk_url_kwarg = 'm_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Matrix_Score', kwargs={"pms_id": self.kwargs["pms_id"], 'm_id': self.kwargs['m_id']}))

    def form_valid(self, form):
        super(AdminPMSMatrixScore, self).form_valid(form)
        messages.success(self.request, 'Matrix updated Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Matrix_Score', kwargs={"pms_id": self.kwargs["pms_id"], 'm_id': self.kwargs['m_id']}))


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixScoreNew(CreateView):
    model = score_matrix
    form_class = MatrixScore
    template_name = 'toyota_kenya/Admin/pms_matrix_score_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Matrix', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def form_valid(self, form):
        super(AdminPMSMatrixScoreNew, self).form_valid(form)
        messages.success(self.request, 'Matrix Created Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Matrix', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_initial(self):
        initial = super(AdminPMSMatrixScoreNew, self).get_initial()
        initial['matrix_pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixKPI(TemplateView):
    template_name = 'toyota_kenya/Admin/pms_matrix_kpi.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['kpi_matrix'] = kpi_months.objects.filter(kpi_months_pms=context['pms'])

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixKPINew(CreateView):
    model = kpi_months
    form_class = MatrixKpi
    template_name = 'toyota_kenya/Admin/pms_matrix_kpi_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def form_valid(self, form):
        super(AdminPMSMatrixKPINew, self).form_valid(form)
        messages.success(self.request, 'Matrix Created Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def get_initial(self):
        initial = super(AdminPMSMatrixKPINew, self).get_initial()
        initial['kpi_months_pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])

        return initial


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixKPIOne(UpdateView):
    model = kpi_months
    form_class = MatrixKpi
    template_name = 'toyota_kenya/Admin/pms_matrix_kpi_one.html'
    pk_url_kwarg = 'm_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def form_valid(self, form):
        super(AdminPMSMatrixKPIOne, self).form_valid(form)
        messages.success(self.request, 'Matrix Edited Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))


# =======================================================================================================

@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixAssessment(TemplateView):
    template_name = 'toyota_kenya/Admin/pms_matrix_assessment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['assessment'] = evaluation.objects.filter()

        return context


@method_decorator(user_passes_test(is_admin), name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class AdminPMSMatrixKPIOne(UpdateView):
    model = kpi_months
    form_class = MatrixKpi
    template_name = 'toyota_kenya/Admin/pms_matrix_kpi_one.html'
    pk_url_kwarg = 'm_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms'] = get_object_or_404(pms, pms_id=self.kwargs['pms_id'])
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu

        context['score_matrix'] = score_matrix.objects.filter(matrix_pms=context['pms'])

        return context

    def get_success_url(self):
        return '{}'.format(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))

    def form_valid(self, form):
        super(AdminPMSMatrixKPIOne, self).form_valid(form)
        messages.success(self.request, 'Matrix Edited Successfully')

        return HttpResponseRedirect(
            reverse('toyota_kenya:Admin_PMS_Matrix_KPI', kwargs={"pms_id": self.kwargs["pms_id"]}))


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class Report(TemplateView):
    template_name = 'toyota_kenya/Reports/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
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

            all_records =[]

            staff_u = get_object_or_404(staff, staff_person=self.request.user.id)



            # kpi_score
            if staff_u.staff_md == 'Yes':
                ind_kpi_scores = 0
                bu_kpi_scores = 0
            elif staff_u.staff_head_bu:
                ind_kpi_scores = 0
                bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_head_bu)
            else:
                ind_kpi_scores = ind_kpi_score(context['pms'], staff_u.staff_person)
                if staff_u.staff_bu:
                    bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_bu)
                else:
                    bu_kpi_scores = 0
            company_kpi_scores = kpi_score = company_kpi_score(context['pms'])

            # Assessment Score
            ass_score = assessment_score(context['pms'], staff_u)

            # Checkin Score
            ci_score = checkin_score(context['pms'], staff_u.staff_person)

            ov_score = overall_score(context['pms'], staff_u)

            all_records.append(
                [staff_u, company_kpi_scores, bu_kpi_scores, ind_kpi_scores, ass_score, ci_score, ov_score])


            if context['user_is_md'] == 'Yes' or self.request.user.is_superuser:
                all_staff = staff.objects.all()

                for staff_u in all_staff:

                    # kpi_score
                    if staff_u.staff_md == 'Yes':
                        ind_kpi_scores = 0
                        bu_kpi_scores = 0
                    elif staff_u.staff_head_bu:
                        ind_kpi_scores = 0
                        bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_head_bu)
                    else:
                        ind_kpi_scores = ind_kpi_score(context['pms'], staff_u.staff_person)
                        if staff_u.staff_bu:
                            bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_bu)
                        else:
                            bu_kpi_scores = 0
                    company_kpi_scores = kpi_score = company_kpi_score(context['pms'])

                    # Assessment Score
                    ass_score = assessment_score(context['pms'], staff_u)

                    # Checkin Score
                    ci_score = checkin_score(context['pms'], staff_u.staff_person)

                    ov_score = overall_score(context['pms'], staff_u)

                    all_records.append([staff_u, company_kpi_scores, bu_kpi_scores, ind_kpi_scores, ass_score, ci_score, ov_score])

            elif context['user_is_bu_head']:
                all_staff = staff.objects.filter(staff_bu=context['user_is_bu_head'])

                for staff_u in all_staff:

                    # kpi_score
                    if staff_u.staff_md == 'Yes':
                        ind_kpi_scores = 0
                        bu_kpi_scores = 0
                    elif staff_u.staff_head_bu:
                        ind_kpi_scores = 0
                        bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_head_bu)
                    else:
                        ind_kpi_scores = ind_kpi_score(context['pms'], staff_u.staff_person)
                        if staff_u.staff_bu:
                            bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_bu)
                        else:
                            bu_kpi_scores = 0
                    company_kpi_scores = kpi_score = company_kpi_score(context['pms'])

                    # Assessment Score
                    ass_score = assessment_score(context['pms'], staff_u)

                    # Checkin Score
                    ci_score = checkin_score(context['pms'], staff_u.staff_person)

                    ov_score = overall_score(context['pms'], staff_u)

                    all_records.append(
                        [staff_u, company_kpi_scores, bu_kpi_scores, ind_kpi_scores, ass_score, ci_score, ov_score])


            elif context['user_is_tl']:
                all_staff = staff.objects.filter(staff_bu=context['user_is_tl'])

                for staff_u in all_staff:

                    # kpi_score
                    if staff_u.staff_md == 'Yes':
                        ind_kpi_scores = 0
                        bu_kpi_scores = 0
                    elif staff_u.staff_head_bu:
                        ind_kpi_scores = 0
                        bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_head_bu)
                    else:
                        ind_kpi_scores = ind_kpi_score(context['pms'], staff_u.staff_person)
                        if staff_u.staff_bu:
                            bu_kpi_scores = bu_kpi_score(context['pms'], staff_u.staff_bu)
                        else:
                            bu_kpi_scores = 0
                    company_kpi_scores = kpi_score = company_kpi_score(context['pms'])

                    # Assessment Score
                    ass_score = assessment_score(context['pms'], staff_u)

                    # Checkin Score
                    ci_score = checkin_score(context['pms'], staff_u.staff_person)

                    ov_score = overall_score(context['pms'], staff_u)

                    all_records.append(
                        [staff_u, company_kpi_scores, bu_kpi_scores, ind_kpi_scores, ass_score, ci_score, ov_score])


            context['all_records'] = all_records

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member_company), name='dispatch')
class Profile(TemplateView):
    template_name = 'toyota_kenya/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_person = get_object_or_404(staff, staff_person=self.request.user.id)
        context['user_is_bu_head'] = staff_person.staff_head_bu
        context['user_is_md'] = staff_person.staff_md
        context['user_is_tl'] = staff_person.staff_head_team
        context['user_team'] = staff_person.staff_team
        context['user_bu'] = staff_person.staff_bu
        context['staff'] = get_object_or_404(staff, staff_person=self.request.user.id)

        return context
