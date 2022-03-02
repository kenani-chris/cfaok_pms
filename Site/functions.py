import datetime

from django.shortcuts import redirect
from django.urls import reverse

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
    return  PMS.objects.filter(
        pms_active=True,
        pms_company=company
    ).first()


def checks(company_id, user):
    if get_company(company_id):
        print(get_active_pms(get_company(company_id)))
        print("we are somewhere here")
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

    context = {'company': get_company(company_id)}
    category_up_list = []
    # company contexts
    if get_company(company_id):
        # staff context
        context['staff'] = get_staff_account(get_company(company_id), user)
        context['company_id'] = company_id
        # pms context
        context['pms'] = get_active_pms(get_company(company_id))

        if context['pms']:
            all_categories_up(get_staff_account(get_company(company_id), user).staff_category, category_up_list)
            context['category_up_list'] = category_up_list
            print(category_up_list)

        if context['staff']:
            context['staff_is_level_head'] = check_staff_is_level_head(company_id, context['staff'])

    local_context |= context


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
    if get_staff_level(staff):
        submission_data = SubmissionKPI.objects.filter(submission_level_category=staff.staff_category,
                                                       submission_pms=pms)
        if submission_data:
            return submission_data.first()
        else:
            return None
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
        if (datetime.datetime.now() >= submission_start) and (datetime.datetime.now() <= submission_end):
            date_check = True
        else:
            date_check = False

        # KPI no Checks
        submission_min = get_user_submission_data(staff, pms).submission_minimum_number
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


def notification_send(n_type, receiver, title, msg):
    Notification.objects.create(notification_type=n_type, notification_recipient=receiver, notification_title=title,
                                notification_message=msg, notification_status='Pending')


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

        if submission.submission_april_results_calculation:
            month_results.append(apr)
            month_targets.append(tar_apr)

        if submission.submission_may_results_calculation:
            month_results.append(may)
            month_targets.append(tar_may)

        if submission.submission_june_results_calculation:
            month_results.append(jun)
            month_targets.append(tar_jun)

        if submission.submission_july_results_calculation:
            month_results.append(jul)
            month_targets.append(tar_jul)

        if submission.submission_august_results_calculation:
            month_results.append(aug)
            month_targets.append(tar_aug)

        if submission.submission_september_results_calculation:
            month_results.append(sep)
            month_targets.append(tar_sep)

        if submission.submission_october_results_calculation:
            month_results.append(oct)
            month_targets.append(tar_oct)

        if submission.submission_november_results_calculation:
            month_results.append(nov)
            month_targets.append(tar_nov)

        if submission.submission_december_results_calculation:
            month_results.append(dec)
            month_targets.append(tar_dec)

        if submission.submission_january_results_calculation:
            month_results.append(jan)
            month_targets.append(tar_jan)

        if submission.submission_february_results_calculation:
            month_results.append(feb)
            month_targets.append(tar_feb)

        if submission.submission_march_results_calculation:
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
                kpi_score  = 0
            else:
                kpi_score = round((sum_target/sum_score)*100, 2)
        else:
            if sum_target == 0:
                kpi_score = 0
            else:
                kpi_score = round((sum_target/sum_score)*100, 2)
    elif kpi_type == "BSC":

        kpi_sum = round(sum(month_results), 2)
        kpi_average = round(kpi_sum / len(month_results), 2)

        if kpi.kpi_function.lower() == 'maximize':
            if kpi.kpi_type.lower() == 'addition':
                kpi_score = (kpi_sum / kpi.kpi_target) * 100
            elif kpi.kpi_type.lower() == 'average':
                kpi_score = (kpi_average / kpi.kpi_target) * 100
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:

                    this_month = datetime.date.today().strftime("%B")

                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    if result_dict[this_month] is None:
                        if result_dict[last_month] is None:
                            kpi_score = (0 / kpi.kpi_target) * 100
                        else:
                            kpi_score = (result_dict[last_month] / kpi.kpi_target) * 100
                    else:
                        kpi_score = (result_dict[this_month] / kpi.kpi_target) * 100
                else:
                    if mar is None:
                        mar = 0
                    kpi_score = (mar / kpi.kpi_target) * 100
        elif kpi.kpi_function.lower() == 'minimize':
            if kpi.kpi_type.lower() == 'addition':
                kpi_score = (kpi.kpi_target / kpi_sum) * 100
            elif kpi.kpi_type.lower() == 'average':
                kpi_score = (kpi.kpi_target / kpi_average) * 100
            elif kpi.kpi_type.lower() == 'ytd':
                if datetime.date.today() <= kpi.kpi_pms.pms_year_end_date:
                    this_month = datetime.date.today().strftime("%B")
                    last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B")
                    if result_dict[this_month] is None:
                        if result_dict[last_month] is None:
                            kpi_score = 0
                        else:
                            kpi_score = (kpi.kpi_target / result_dict[last_month]) * 100
                    else:
                        kpi_score = (kpi.kpi_target / result_dict[this_month]) * 100
                else:
                    if mar is None:
                        mar = 0
                    kpi_score = (mar / kpi.kpi_target) * 100

    elif kpi_type == "Annual Target":

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


def calculate_overall_kpi_score(staff, pms):
    kpis = kpi_list(staff, pms)
    kpi_type = KPIType.objects.filter(type_pms=pms,type_category=staff.staff_category)
    if kpi_type:
        kpi_type = kpi_type.first().type_kpi
    else:
        kpi_type = "Annual Target"
    results = []
    for kpi in kpis['approved_kpi']:
        weight = kpi.kpi_weight
        score = calculate_kpi_score(kpi, kpi_type)
        weighted_score = (weight * score)/100
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
    assessments = Assessment.objects.filter(assessment_pms=pms, assessment_end_date__lt=datetime.datetime.now(),
                                            assessment_scoring_use=True)
    for assessment in assessments:
        if Level.objects.filter(level_head=staff):
            if LevelMembership.objects.filter(membership_staff=staff):
                s_tl_score = calculate_assessment_score(assessment, staff, 'Top')
                tl_s_score = calculate_assessment_score(assessment, staff, 'Bottom')
                score = score + (s_tl_score + tl_s_score)/2
            else:
                score = score + calculate_assessment_score(assessment, staff, 'Top')
        else:
            score = score + calculate_assessment_score(assessment, staff, 'Bottom')
    if assessments:
        score = round(score/assessments.count())
    return score


def calculate_assessment_score(assessment, staff, direction):
    score = 0
    questions = Questions.objects.filter(question_assessment=assessment, question_direction=direction)
    for question in questions:
        question_score = 0
        responses = QuestionResponses.objects.filter(response_question=question, response_evaluated=staff)
        for response in responses:
            question_score += response.response_submitted
        if responses:
            question_score = round(question_score/responses.count())
        score += ((question_score - assessment.assessment_min_score)/(assessment.assessment_max_score-assessment.assessment_min_score) * 100)
    if questions:
        score = (score/questions.count() * 100)
    return score


def get_matrix(staff, pms):
    if Matrix.objects.filter(matrix_pms=pms, matrix_grade=staff.staff_grade):
        return Matrix.objects.filter(matrix_pms=pms, matrix_grade=staff.staff_grade).first()
    elif Matrix.objects.filter(matrix_pms=pms, matrix_category=staff.staff_category):
        return Matrix.objects.filter(matrix_pms=pms, matrix_category=staff.staff_category)
    else:
        return None


default_matrix = {'KPI': 50,
                  'Assessment': 20,
                  'Check-In': 100,
                  'BU': 20,
                  'Company': 10
                  }


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

    kpi_score = kpi_weight/100 * calculate_overall_kpi_score(staff, pms)
    assessment_score = assessment_weight/100 * calculate_overall_assessment_score(staff, pms)
    checkin_score = checkin_weight/100 * calculate_overall_check_in_score(staff, pms)
    bu_score = get_bu_score(staff, pms)
    company_score = get_company_score(staff, pms)

    score = (kpi_score + assessment_score + bu_score + assessment_score + company_score) * checkin_score

    return score


def get_bu_score(staff, pms):
    score = 0
    categories = []
    all_categories_up(staff.staff_category, categories)
    for category in categories:
        if category.category_kpi_view and category != categories[-1]:
            if not Level.objects.filter(level_head=staff, level_category=category):
                level = Level.objects.filter(level_category=category)
                if level:
                    score = calculate_overall_kpi_score(level.first().level_head, pms)

    return score


def get_company_score(staff, pms):
    score = 0
    categories = []
    all_categories_up(staff.staff_category, categories)

    if len(categories) > 0:
        if categories[0] != categories[-1]:
            if not Level.objects.filter(level_head=staff, level_category=categories[0]):
                level = Level.objects.filter(level_category=categories[0])
                if level:
                    level.first()
                    score = calculate_overall_kpi_score(level.first().level_head, pms)

    return score
