import datetime
import os
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from cfaok_pms import settings
from cfaok_pms.settings import PASSWORD_CHANGE_DURATION
from .models import *


def get_staff_account(company, user):
    return Staff.objects.filter(
        staff_company=company,
        staff_person=user,
        staff_active=True
    ).first()


def get_company(company_id):
    return Company.objects.filter(
        company_id=company_id,
        company_status=True
    ).first()


def get_active_pms(company):
    return PMS.objects.filter(
        pms_active=True,
        pms_company=company
    ).first()


def checks(company_id, user):
    if get_company(company_id):
        if get_active_pms(get_company(company_id)):
            if get_staff_account(get_company(company_id), user):
                return None
            else:
                return "Error001"
        else:
            return "Error003"
    else:
        return "Error002"


def global_context(company_id, user, local_context):
    calendar_dict = {}
    context = {'company': get_company(company_id)}
    category_up_list = []
    # company contexts
    if get_company(company_id):
        # staff context
        context['staff'] = get_staff_account(get_company(company_id), user)
        context['company_id'] = company_id
        context['month'] = datetime.date.today().strftime('%B')
        # pms context
        context['pms'] = get_active_pms(get_company(company_id))

        if context['pms']:
            all_categories_up(get_staff_account(get_company(company_id), user).staff_category, category_up_list)
            context['category_up_list'] = category_up_list

            calendar_months(context['pms'], calendar_dict)

        if context['staff']:
            context['staff_is_level_head'] = check_staff_is_level_head(company_id, context['staff'])
    context['calendar_dict'] = calendar_dict

    local_context |= context


def calendar_months(pms, calendar_dict):
    start_date = pms.pms_year_start_date
    end_date = pms.pms_year_end_date

    year = start_date.year
    month = start_date.month
    while True:
        current = datetime.date(year, month, 1)
        calendar_dict[current.strftime('%B')] = current.year
        if current.month == end_date.month and current.year == end_date.year:
            break
        else:
            month = ((month + 1) % 12) or 12
            if month == 1:
                year += 1


def check_staff_is_level_head(company_id, staff):
    if Level.objects.filter(level_head=staff, level_category__category_company__company_id=company_id):
        return True
    else:
        return False


# get_user_level
def get_staff_level(staff):
    level = LevelMembership.objects.filter(membership_staff=staff, membership_is_active=True)
    if level:
        level = level.first().membership_level
    else:
        level = None
    return level


# get_user submission data
def get_user_submission_data(staff, pms):
    submission_data = SubmissionKPI.objects.filter(submission_level_category=staff.staff_category, submission_pms=pms)
    if submission_data:
        return submission_data.first()
    else:
        return None


def kpi_list(staff, pms):
    context = {'approved_kpi': KPI.objects.filter(kpi_staff=staff, kpi_pms=pms, kpi_status='Approved'),
               'pending_kpi': KPI.objects.filter(kpi_staff=staff, kpi_pms=pms, kpi_status='Pending'),
               'submitted_kpi': KPI.objects.filter(kpi_staff=staff, kpi_pms=pms, kpi_status='Submitted'),
               'rejected_kpi': KPI.objects.filter(kpi_staff=staff, kpi_pms=pms, kpi_status='Rejected')}

    return context


def kpi_number_check(staff, pms):
    kpi_count = 0
    if kpi_list(staff, pms):
        kpis = kpi_list(staff, pms)
        kpi_count = kpis['approved_kpi'].count() + kpis['pending_kpi'].count() + kpis['submitted_kpi'].count()

    return kpi_count


def kpi_weight_check(staff, pms):
    kpis = kpi_list(staff, pms)

    weight = 0

    for kpi in (kpis['approved_kpi']):
        weight += kpi.kpi_weight

    for kpi in (kpis['pending_kpi']):
        weight += kpi.kpi_weight

    for kpi in (kpis['submitted_kpi']):
        weight += kpi.kpi_weight

    return weight


def kpi_submission_checks(staff, pms):
    date_check = True
    number_check = True

    if get_user_submission_data(staff, pms):
        submission_start = get_user_submission_data(staff, pms).submission_start_date
        submission_end = get_user_submission_data(staff, pms).submission_end_date

        # check dates
        if (datetime.datetime.now(timezone.utc) >= submission_start) and \
                (datetime.datetime.now(timezone.utc) <= submission_end):
            date_check = True
        else:
            date_check = False

        # KPI no Checks
        # submission_min = get_user_submission_data(staff, pms).submission_minimum_number
        submission_max = get_user_submission_data(staff, pms).submission_maximum_number

        if kpi_number_check(staff, pms) < submission_max:
            number_check = True
        else:
            number_check = False

    # check weight
    if kpi_weight_check(staff, pms) < 100:
        weight_check = True
    else:
        weight_check = False

    return {'date_check': date_check,
            'number_check': number_check,
            'weight_check': weight_check}


def notification_log(n_type, ref_key, user_name, receiver, title, msg):
    notification = Notification()
    notification.notification_type = n_type
    notification.notification_reference_key = ref_key
    notification.notification_user_name = user_name
    notification.notification_email = receiver
    notification.notification_title = title
    notification.notification_message = msg
    notification.notification_date = datetime.datetime.now()
    notification.notification_status = "Pending"
    notification.save()


def all_categories_up(cat, cat_list):
    if cat is None:
        return
    else:
        cat_list.append(cat)
        all_categories_up(cat.category_parent, cat_list)


def all_levels_down(level, level_list):
    if level is None:
        return
    else:
        child_levels = Level.objects.filter(level_parent=level)
        for child in child_levels:
            level_list.append(child)
            all_levels_down(child, level_list)


def all_levels_up(level, level_list):
    if level is None:
        return
    else:
        parent_level = level.level_parent
        level_list.append(parent_level)
        all_levels_up(parent_level, level_list)


def calculate_kpi_score(kpi, kpi_type):
    kpi_score = 0
    kpi_sum = 0

    month_targets = []
    month_results = []

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

    tar_apr = kpi.kpi_april_target
    tar_may = kpi.kpi_may_target
    tar_jun = kpi.kpi_june_target
    tar_jul = kpi.kpi_july_target
    tar_aug = kpi.kpi_august_target
    tar_sep = kpi.kpi_september_target
    tar_oct = kpi.kpi_october_target
    tar_nov = kpi.kpi_november_target
    tar_dec = kpi.kpi_december_target
    tar_jan = kpi.kpi_january_target
    tar_feb = kpi.kpi_february_target
    tar_mar = kpi.kpi_march_target

    result_dict = {'April': apr, 'May': may, 'June': jun, 'July': jul, 'August': aug, 'September': sep,
                   'October': oct, 'November': nov, 'December': dec, 'January': jan, 'February': feb, 'March': mar}

    if get_user_submission_data(kpi.kpi_staff, kpi.kpi_pms):

        submission = get_user_submission_data(kpi.kpi_staff, kpi.kpi_pms)

        if submission.submission_april_results_calculation == True:
            month_results.append(apr)
            month_targets.append(tar_apr)

        if submission.submission_may_results_calculation == True:
            month_results.append(may)
            month_targets.append(tar_may)

        if submission.submission_june_results_calculation == True:
            month_results.append(jun)
            month_targets.append(tar_jun)

        if submission.submission_july_results_calculation == True:
            month_results.append(jul)
            month_targets.append(tar_jul)

        if submission.submission_august_results_calculation == True:
            month_results.append(aug)
            month_targets.append(tar_aug)

        if submission.submission_september_results_calculation == True:
            month_results.append(sep)
            month_targets.append(tar_sep)

        if submission.submission_october_results_calculation == True:
            month_results.append(oct)
            month_targets.append(tar_oct)

        if submission.submission_november_results_calculation == True:
            month_results.append(nov)
            month_targets.append(tar_nov)

        if submission.submission_december_results_calculation == True:
            month_results.append(dec)
            month_targets.append(tar_dec)

        if submission.submission_january_results_calculation == True:
            month_results.append(jan)
            month_targets.append(tar_jan)

        if submission.submission_february_results_calculation == True:
            month_results.append(feb)
            month_targets.append(tar_feb)

        if submission.submission_march_results_calculation == True:
            month_results.append(mar)
            month_targets.append(tar_mar)

    else:
        month_results = [apr, may, jun, jul, aug, sep, oct, nov, dec, jan, feb, mar]
        month_targets = [tar_apr, tar_may, tar_jun, tar_jul, tar_aug, tar_sep, tar_oct, tar_nov, tar_dec, tar_jan,
                         tar_feb, tar_mar]

    month_results = [0 if v is None else v for v in month_results]
    month_targets = [0 if v is None else v for v in month_targets]

    if kpi_type == "Monthly Target":
        sum_score = round(sum(month_results), 2)
        sum_target = round(sum(month_targets), 2)

        if kpi.kpi_function.lower() == 'minimize':
            if sum_score == 0:
                if sum_target <= sum_score:
                    kpi_score = 100
                else:
                    kpi_score = 0
            else:
                kpi_score = round((sum_target / sum_score) * 100, 2)
        else:
            if sum_target == 0:
                kpi_score = 0
            else:
                kpi_score = round((sum_score / sum_target) * 100, 2)
    elif kpi_type == "BSC":

        kpi_sum = round(sum(month_results), 2)
        kpi_average = round(kpi_sum / len(month_results), 2)

        if kpi.kpi_function.lower() == 'maximize':
            if kpi.kpi_type.lower() == 'addition':
                if kpi.kpi_target is None or kpi.kpi_target == 0:
                    if kpi_sum >= kpi.kpi_target:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi_sum / kpi.kpi_target) * 100
            elif kpi.kpi_type.lower() == 'average':
                if kpi_average != 0:
                    kpi_score = (kpi.kpi_target / kpi_average) * 100
                else:
                    if kpi_average >= kpi.kpi_target:
                        kpi_score = 100
                    else:
                        kpi_score = 0
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:

                    this_month = datetime.date.today().strftime("%B")

                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    before_last_month = (datetime.date.today() - datetime.timedelta(days=61)).strftime("%B")
                    if result_dict[this_month] is None:
                        if result_dict[last_month] is None:
                            if result_dict[before_last_month] is None:
                                if kpi.kpi_target is None or kpi.kpi_target == 0:
                                    kpi_score = 0
                                else:
                                    kpi_score = (0 / kpi.kpi_target) * 100
                            else:
                                if kpi.kpi_target == 0 or kpi.kpi_target is None:
                                    if result_dict[before_last_month] >= 0:
                                        kpi_score = 100
                                    else:
                                        kpi_score = 0
                                else:
                                    kpi_score = (result_dict[before_last_month] / kpi.kpi_target) * 100
                        else:
                            if kpi.kpi_target == 0 or kpi.kpi_target is None:
                                if result_dict[last_month] >= 0:
                                    kpi_score = 100
                                else:
                                    kpi_score = 0
                            else:
                                kpi_score = (result_dict[last_month] / kpi.kpi_target) * 100

                    else:
                        if kpi.kpi_target == 0 or kpi.kpi_target is None:
                            if result_dict[this_month] >= 0:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                        else:
                            kpi_score = (result_dict[this_month] / kpi.kpi_target) * 100
                else:
                    if mar is None:
                        mar = 0
                    if kpi.kpi_target is None or kpi.kpi_target == 0:
                        if mar > 0:
                            kpi_score = 100
                        else:
                            kpi_score = 0
                    else:
                        kpi_score = (mar / kpi.kpi_target) * 100
        elif kpi.kpi_function.lower() == 'minimize':
            if kpi.kpi_type.lower() == 'addition':
                if kpi_sum == 0:
                    if kpi.kpi_target >= 0:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi.kpi_target / kpi_sum) * 100
            elif kpi.kpi_type.lower() == 'average':
                if kpi_average == 0:
                    if kpi.kpi_target > 0:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi.kpi_target / kpi_average) * 100
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                    this_month = datetime.date.today().strftime("%B")
                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    if result_dict[this_month] is None:
                        if result_dict[last_month] is None:
                            kpi_score = 0
                        else:
                            if result_dict[last_month] == float(0):
                                if kpi.kpi_target >= 0:
                                    kpi_score = 100
                                else:
                                    kpi_score = 0
                            else:
                                kpi_score = (kpi.kpi_target / result_dict[last_month]) * 100
                    else:
                        if result_dict[this_month] == 0:
                            if kpi.kpi_target >= 0:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                        else:
                            kpi_score = (kpi.kpi_target / result_dict[this_month]) * 100
                else:
                    if mar is None:
                        mar = 0
                    if mar is None or mar == 0:
                        if kpi.kpi_target >= 0:
                            kpi_score = 100
                        else:
                            kpi_score = 0
                    else:
                        kpi_score = (kpi.kpi_target / mar) * 100

    elif kpi_type == "Annual Target":

        kpi_sum = round(sum(month_results), 2)
        kpi_average = round(kpi_sum / len(month_results), 2)

        if kpi.kpi_function.lower() == 'maximize':
            if kpi.kpi_type.lower() == 'addition':
                if kpi.kpi_target is None or kpi.kpi_target == 0:
                    if kpi_sum >= kpi.kpi_target:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi_sum / kpi.kpi_target) * 100
            elif kpi.kpi_type.lower() == 'average':
                if kpi.kpi_target is None or kpi.kpi_target == 0:
                    if kpi_average >= kpi.kpi_target:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi_average / kpi.kpi_target) * 100
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                    this_month = datetime.date.today().strftime("%B")

                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    before_last_month = (datetime.date.today() - datetime.timedelta(days=61)).strftime("%B")

                    if result_dict[this_month] is None:
                        if result_dict[last_month] is None:
                            if result_dict[before_last_month] is None:
                                if kpi.kpi_target is None or kpi.kpi_target == 0:
                                    kpi_score = 0
                                else:
                                    kpi_score = (0 / kpi.kpi_target) * 100
                            else:
                                if kpi.kpi_target is None or kpi.kpi_target == 0:
                                    if result_dict[before_last_month] >= 0:
                                        kpi_score = 100
                                    else:
                                        kpi_score = 0
                                else:
                                    kpi_score = (result_dict[before_last_month] / kpi.kpi_target) * 100
                        else:
                            if kpi.kpi_target is None or kpi.kpi_target == 0:
                                if result_dict[last_month] >= 0:
                                    kpi_score = 100
                                else:
                                    kpi_score = 0
                            else:
                                kpi_score = (result_dict[last_month] / kpi.kpi_target) * 100
                    else:
                        if kpi.kpi_target is None or kpi.kpi_target == 0:
                            if result_dict[this_month] >= 0:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                        else:
                            kpi_score = (result_dict[this_month] / kpi.kpi_target) * 100
                else:
                    if mar is None:
                        mar = 0
                    if kpi.kpi_target is None or kpi.kpi_target == 0:
                        if mar >= 0:
                            kpi_score = 100
                        else:
                            kpi_score = 0
                    else:
                        kpi_score = (mar / kpi.kpi_target) * 100
        elif kpi.kpi_function.lower() == 'minimize':
            if kpi.kpi_type.lower() == 'addition':
                if kpi_sum == 0:
                    if kpi.kpi_target >= kpi_sum:
                        kpi_score = 100
                    else:
                        kpi_score = 0
                else:
                    kpi_score = (kpi.kpi_target / kpi_sum) * 100
            elif kpi.kpi_type.lower() == 'average':
                if kpi_average != 0:
                    kpi_score = (kpi.kpi_target / kpi_average) * 100
                else:
                    if kpi_average >= kpi.kpi_target:
                        kpi_score = 100
                    else:
                        kpi_score = 0
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                    this_month = datetime.date.today().strftime("%B")
                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    if result_dict[this_month] is None or result_dict[this_month] == 0:
                        if result_dict[last_month] is None or result_dict[last_month] == 0:
                            if kpi.kpi_target >= 0:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                        else:
                            kpi_score = (kpi.kpi_target / result_dict[last_month]) * 100
                    else:
                        kpi_score = (kpi.kpi_target / result_dict[this_month]) * 100
                else:
                    if mar is None:
                        mar = 0
                    if mar == 0:
                        if kpi.kpi_target is None:
                            if mar <= 0:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                        else:
                            if mar <= kpi.kpi_target:
                                kpi_score = 100
                            else:
                                kpi_score = 0
                    else:
                        kpi_score = (kpi.kpi_target / mar) * 100

    if kpi.kpi_pms.pms_cap_results:
        if kpi_score > 100.00:
            kpi_score = 100.00

    return round(kpi_score, 2)


def calculate_overall_kpi_score(staff, pms):
    kpis = kpi_list(staff, pms)
    kpi_type = KPIType.objects.filter(type_pms=pms, type_category=staff.staff_category)
    if kpi_type:
        kpi_type = kpi_type.first().type_kpi
    else:
        kpi_type = "Annual Target"
    results = []
    for kpi in kpis['approved_kpi']:
        weight = kpi.kpi_weight
        score = calculate_kpi_score(kpi, kpi_type)
        weighted_score = (weight * score) / 100
        results.append(weighted_score)
    return round(sum(results), 2)


def get_user_checkin(staff, pms):
    checkin = []
    for ci in CheckIn.objects.filter(check_in_Staff=staff, check_in_pms=pms).exclude(check_in_status='Rejected'):
        checkin.append(ci.check_in_month)
    return list(set(checkin))


def calculate_overall_check_in_score(staff, pms):
    ci = len(get_user_checkin(staff, pms))

    submission = SubmissionCheckin.objects.filter(submission_pms=pms, submission_level_category=staff.staff_category)
    score = 0
    if submission:
        submission = submission.first()

        if ci == 0:
            score = 0
        elif ci == 1:
            score = submission.submission_one_results
        elif ci == 2:
            score = submission.submission_two_results
        elif ci == 3:
            score = submission.submission_three_results
        elif ci == 4:
            score = submission.submission_four_results
        elif ci == 5:
            score = submission.submission_five_results
        elif ci == 6:
            score = submission.submission_six_results
        elif ci == 7:
            score = submission.submission_seven_results
        elif ci == 8:
            score = submission.submission_eight_results
        elif ci == 9:
            score = submission.submission_nine_results
        elif ci == 10:
            score = submission.submission_ten_results
        elif ci == 11:
            score = submission.submission_eleven_results
        elif ci == 12:
            score = submission.submission_twelve_results
        else:
            score = 0
    else:

        if ci == 0:
            score = 0
        elif ci == 1:
            score = 0
        elif ci == 2:
            score = 0
        elif ci == 3:
            score = 10
        elif ci == 4:
            score = 20
        elif ci == 5:
            score = 30
        elif ci == 6:
            score = 40
        elif ci == 7:
            score = 50
        elif ci == 8:
            score = 60
        elif ci == 9:
            score = 70
        elif ci == 10:
            score = 80
        elif ci == 11:
            score = 90
        elif ci == 12:
            score = 100

    return score


def calculate_overall_assessment_score(staff, pms):
    score = 0
    assessments = Assessment.objects.filter(assessment_pms=pms,
                                            assessment_end_date__lt=datetime.datetime.now(tz=timezone.utc),
                                            assessment_scoring_use=True)
    for assessment in assessments:
        if Level.objects.filter(level_head=staff):
            if LevelMembership.objects.filter(membership_staff=staff):
                s_tl_score = calculate_assessment_score(assessment, staff, 'Top')
                tl_s_score = calculate_assessment_score(assessment, staff, 'Bottom')
                score = score + (s_tl_score + tl_s_score) / 2
            else:
                score = score + calculate_assessment_score(assessment, staff, 'Top')
        else:
            score = score + calculate_assessment_score(assessment, staff, 'Bottom')
    if assessments:
        score = round(score / assessments.count())
    return score


def calculate_one_assessment_score(staff, pms, assessment):
    score = 0

    if Level.objects.filter(level_head=staff):
        if LevelMembership.objects.filter(membership_staff=staff):
            s_tl_score = calculate_assessment_score(assessment, staff, 'Top')
            tl_s_score = calculate_assessment_score(assessment, staff, 'Bottom')
            score = score + (s_tl_score + tl_s_score) / 2
        else:
            score = score + calculate_assessment_score(assessment, staff, 'Top')
    else:
        score = score + calculate_assessment_score(assessment, staff, 'Bottom')

    return round(score, 2)


def calculate_assessment_score(assessment, staff, direction):
    score = 0
    questions = Questions.objects.filter(question_assessment=assessment, question_direction=direction)
    for question in questions:
        question_score = 0
        responses = QuestionResponses.objects.filter(response_question=question, response_evaluated=staff)
        for response in responses:
            question_score += response.response_submitted
        if responses:
            question_score = round(question_score / responses.count())
        score += ((question_score - assessment.assessment_min_score) / (
                    assessment.assessment_max_score - assessment.assessment_min_score) * 100)
    if questions:
        score = (score / questions.count())
    return round(score, 2)


def get_matrix(staff, pms):
    if Matrix.objects.filter(matrix_pms=pms, matrix_grade=staff.staff_grade):
        return Matrix.objects.filter(matrix_pms=pms, matrix_grade=staff.staff_grade).first()
    elif Matrix.objects.filter(matrix_pms=pms, matrix_category=staff.staff_category):
        return Matrix.objects.filter(matrix_pms=pms, matrix_category=staff.staff_category).first()
    else:
        return None


default_matrix = {'KPI': 50,
                  'Assessment': 20,
                  'Check-In': 100,
                  'BU': 20,
                  'Company': 10
                  }


def display_matrix(staff, pms):
    matrix = get_matrix(staff, pms)
    matrix_applied = {}
    if matrix:
        matrix_applied['Assessment'] = matrix.matrix_assessment_weight
        matrix_applied['KPI'] = matrix.matrix_kpi_weight
        matrix_applied['Check-In'] = matrix.matrix_kpi_weight
        matrix_applied['BU'] = matrix.matrix_bu_weight
        matrix_applied['Company'] = matrix.matrix_company_weight

    else:
        matrix_applied = default_matrix

    return matrix_applied


def display_months_used(staff, pms):
    submission_kpi = get_user_submission_data(staff, pms)
    month_use = {
        'April': True,
        'May': True,
        'June': True,
        'July': True,
        'August': True,
        'September': True,
        'October': True,
        'November': True,
        'December': True,
        'January': True,
        'February': True,
        'March': True,
    }
    if submission_kpi is not None:
        month_use['April'] = submission_kpi.submission_april_results_calculation
        month_use['May'] = submission_kpi.submission_may_results_calculation
        month_use['June'] = submission_kpi.submission_june_results_calculation
        month_use['July'] = submission_kpi.submission_july_results_calculation
        month_use['August'] = submission_kpi.submission_august_results_calculation
        month_use['September'] = submission_kpi.submission_september_results_calculation
        month_use['October'] = submission_kpi.submission_october_results_calculation
        month_use['November'] = submission_kpi.submission_november_results_calculation
        month_use['December'] = submission_kpi.submission_december_results_calculation
        month_use['January'] = submission_kpi.submission_january_results_calculation
        month_use['February'] = submission_kpi.submission_february_results_calculation
        month_use['March'] = submission_kpi.submission_march_results_calculation

        print(submission_kpi)
    return month_use


def display_checkin_scoring_used(staff, pms):
    checkin_scores = {
        "1": "0%",
        "2": "0%",
        "3": "10%",
        "4": "20%",
        "5": "30%",
        "6": "40%",
        "7": "50%",
        "8": "60%",
        "9": "70%",
        "10": "80%",
        "11": "90%",
        "12": "100%",
    }

    if SubmissionCheckin.objects.filter(submission_pms=pms, submission_level_category=staff.staff_category):
        submission = SubmissionCheckin.objects.filter(submission_pms=pms,
                                                      submission_level_category=staff.staff_category).first()
        checkin_scores["1"] = str(submission.submission_one_results) + "%"
        checkin_scores["2"] = str(submission.submission_two_results) + "%"
        checkin_scores["3"] = str(submission.submission_three_results) + "%"
        checkin_scores["4"] = str(submission.submission_four_results) + "%"
        checkin_scores["5"] = str(submission.submission_five_results) + "%"
        checkin_scores["6"] = str(submission.submission_six_results) + "%"
        checkin_scores["7"] = str(submission.submission_seven_results) + "%"
        checkin_scores["8"] = str(submission.submission_eight_results) + "%"
        checkin_scores["9"] = str(submission.submission_nine_results) + "%"
        checkin_scores["10"] = str(submission.submission_ten_results) + "%"
        checkin_scores["11"] = str(submission.submission_eleven_results) + "%"
        checkin_scores["12"] = str(submission.submission_twelve_results) + "%"

    return checkin_scores


def calculate_overall_score(staff, pms):
    matrix = get_matrix(staff, pms)
    matrix_applied = {}
    if matrix:
        matrix_applied['Assessment'] = matrix.matrix_assessment_weight
        matrix_applied['KPI'] = matrix.matrix_kpi_weight
        matrix_applied['Check-In'] = matrix.matrix_kpi_weight
        matrix_applied['BU'] = matrix.matrix_bu_weight
        matrix_applied['Company'] = matrix.matrix_company_weight

    else:
        matrix_applied = default_matrix

    kpi_weight = matrix_applied['KPI']
    checkin_weight = matrix_applied['Check-In']
    assessment_weight = matrix_applied['Assessment']
    bu_weight = matrix_applied['BU']
    company_weight = matrix_applied['Company']

    if kpi_weight is None:
        kpi_weight = 0

    if checkin_weight is None:
        checkin_weight = 0

    if assessment_weight is None:
        assessment_weight = 0

    if bu_weight is None:
        bu_weight = 0

    if company_weight is None:
        company_weight = 0

    kpi_score = kpi_weight / 100 * calculate_overall_kpi_score(staff, pms)
    assessment_score = assessment_weight / 100 * calculate_overall_assessment_score(staff, pms)
    checkin_score = calculate_overall_check_in_score(staff, pms)
    bu_score = bu_weight / 100 * get_bu_score(staff, pms)
    company_score = company_weight / 100 * get_company_score(staff, pms)

    score = round((kpi_score + assessment_score + bu_score + assessment_score + company_score) * checkin_score / 100, 2)

    return score


def get_bu_score(staff, pms):
    score = 0
    categories = []
    levels_up = []
    all_categories_up(staff.staff_category, categories)
    for category in categories:
        if category.category_kpi_view is True and category != categories[-1]:
            if Level.objects.filter(level_category=category).exclude(level_head=staff):
                all_levels_up(get_staff_level(staff), levels_up)
                levels_up.append(get_staff_level(staff))
                for level in Level.objects.filter(level_category=category).exclude(level_head=staff):
                    if level in levels_up:
                        score = calculate_overall_kpi_score(level.level_head, pms)
                        break
    return score


def get_bu(staff):

    bu = None
    categories = []
    levels_up = []

    if not Level.objects.filter(level_head=staff, level_category__category_kpi_view=True):
        all_categories_up(staff.staff_category, categories)
        for category in categories:
            if category.category_kpi_view is True and category != categories[-1]:
                if Level.objects.filter(level_category=category).exclude(level_head=staff):
                    all_levels_up(get_staff_level(staff), levels_up)
                    levels_up.append(get_staff_level(staff))
                    for level in Level.objects.filter(level_category=category).exclude(level_head=staff):
                        if level in levels_up:
                            bu = level
                            break
    return bu


def get_company_score(staff, pms):
    score = 0
    categories = []
    all_categories_up(staff.staff_category, categories)

    if len(categories) > 0:
        if categories[0] != categories[-1]:
            if not Level.objects.filter(level_head=staff, level_category=categories[-1]):
                level = Level.objects.filter(level_category=categories[-1])
                if level:
                    level.first()
                    score = calculate_overall_kpi_score(level.first().level_head, pms)

    return score


def get_company_used(staff):

    the_company = None
    categories = []
    all_categories_up(staff.staff_category, categories)

    if len(categories) > 0:
        if categories[0] != categories[-1]:
            if not Level.objects.filter(level_head=staff, level_category=categories[-1]):
                level = Level.objects.filter(level_category=categories[-1])
                if level:
                    the_company = level.first()

    return the_company


def send_email(title, receiver, message):
    user = User.objects.filter(email=receiver)
    if user is not None:
        name = user.first().first_name
    else:
        name = "Receiver"

    pms_guide = '<a href="https://1drv.ms/b/s!AvHDzgs7pzmrundGQQj6-nrkpP-H?e=eDM6SR">PMS Guide</a>'
    pms_link = '<a href="https:ck-pms.com">PMS Link</a>'

    body_html = '''
        <html>
            <body>
                <br>Dear ''' + name + ''',
                <br>
                <br>
                ''' + message + '''
                <br>
                <br>
                  ''' + pms_guide + '''  |  ''' + pms_link + '''
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
    msg = EmailMultiAlternatives(title, body_html, from_email=from_email, to=[receiver])

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


def log_issue(message):
    now = datetime.datetime.now()
    message = str(now) + "  :   " + message
    folder_path = "/home/cfaok_pms_user/cfaok_pms_project/logs/"
    file = "Log_" + str(now.day) + "_" + str(now.month) + "_" + str(now.year) + ".txt"
    log_file = os.path.join(folder_path, file)
    if os.path.isdir(folder_path):
        if os.path.isfile(log_file):
            with open(log_file, 'a') as file:
                file.write(message + "\n")
        else:
            with open(log_file, 'w') as file:
                file.write(message + "\n")
    else:
        os.mkdir(folder_path)


def password_change_decorator(func):
    def function(request, *args, **kwargs):
        if request.user.is_authenticated:
            changes = PasswordChange.objects.filter(change_user=request.user)
            if changes:
                last_change = changes.last()
                now = datetime.datetime.now(last_change.change_last_date.tzinfo)
                if abs((last_change.change_last_date - now).days) >= PASSWORD_CHANGE_DURATION:
                    return HttpResponseRedirect(reverse('password_expire'))
            else:
                return HttpResponseRedirect(reverse('password_expire'))
        return func(request, *args, **kwargs)
    return function
