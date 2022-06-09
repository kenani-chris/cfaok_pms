import datetime
import os
from email.mime.image import MIMEImage
from typing import Dict, Union, Any

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from cfaok_pms import settings
from cfaok_pms.settings import PASSWORD_CHANGE_DURATION
from .models import Staff, Company, PMS, Level, LevelMembership, SubmissionKPI, Notification, KPI, KPIType, \
    SubmissionCheckin, QuestionResponses, Questions, Matrix, Assessment, CheckIn, PasswordChange, User


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

def get_required_months(kpi):

    results = {'april': kpi.kpi_april_score, 'may': kpi.kpi_may_score, 'june': kpi.kpi_june_score,
                   'july': kpi.kpi_july_score, 'august': kpi.kpi_august_score, 'september': kpi.kpi_september_score,
                   'october': kpi.kpi_october_score, 'november': kpi.kpi_november_score,
                   'december': kpi.kpi_december_score, 'january': kpi.kpi_january_score,
                   'february': kpi.kpi_february_score, 'march': kpi.kpi_march_score}

    targets = {'april': kpi.kpi_april_target, 'may': kpi.kpi_may_target,
                   'june': kpi.kpi_june_target,
                   'july': kpi.kpi_july_target, 'august': kpi.kpi_august_target,
                   'september': kpi.kpi_september_target,
                   'october': kpi.kpi_october_target, 'november': kpi.kpi_november_target,
                   'december': kpi.kpi_december_target, 'january': kpi.kpi_january_target,
                   'february': kpi.kpi_february_target, 'march': kpi.kpi_march_target}

    submission = get_user_submission_data(kpi.kpi_staff, kpi.kpi_pms)

    if submission:

        if not submission.submission_april_results_calculation:
            results.pop('april')
            targets.pop('april')
        if not submission.submission_may_results_calculation:
            results.pop('may')
            targets.pop('may')
        if not submission.submission_june_results_calculation:
            results.pop('june')
            targets.pop('june')
        if not submission.submission_july_results_calculation:
            results.pop('july')
            targets.pop('july')
        if not submission.submission_august_results_calculation:
            results.pop('august')
            targets.pop('august')
        if not submission.submission_september_results_calculation:
            results.pop('september')
            targets.pop('september')
        if not submission.submission_october_results_calculation:
            results.pop('october')
            targets.pop('october')
        if not submission.submission_november_results_calculation:
            results.pop('november')
            targets.pop('november')
        if not submission.submission_december_results_calculation:
            results.pop('december')
            targets.pop('december')
        if not submission.submission_january_results_calculation:
            results.pop('january')
            targets.pop('january')
        if not submission.submission_february_results_calculation:
            results.pop('february')
            targets.pop('february')
        if not submission.submission_march_results_calculation:
            results.pop('march')
            targets.pop('march')
            
    return targets, results
            

def calculate_kpi_score(kpi, kpi_type):
    score = 0

    try:
        targets, results = get_required_months(kpi)

        targets = {k: v or 0 for (k, v) in targets.items()}
        results = {k: v or 0 for (k, v) in results.items()}

        if kpi_type == "Monthly Target":
            score = calculate_kpi_monthly_target_score(kpi, targets, results)
        elif kpi_type == "BSC":
            score = calculate_kpi_annual_target_score(kpi, kpi.kpi_bsc_s_target, results)
        elif kpi_type == "Annual Target":
            score = calculate_kpi_annual_target_score(kpi, kpi.kpi_target, results)

        if kpi.kpi_pms.pms_cap_results and score > 100.00:
            score = 100.00
        elif kpi.kpi_pms.pms_cap_results and score < 0.00:
            score = 0.00

    except Exception as e:
        print(kpi.kpi_staff, " - ", kpi.kpi_title, e)

    return round(score, 2)


def calculate_kpi_monthly_target_score(kpi, targets, results):
    return calculate_by_function(kpi.kpi_function, sum(targets.values()), sum(results.values()))


def calculate_kpi_annual_target_score(kpi, targets, results):

    if kpi.kpi_type.lower() == 'addition':
        return calculate_by_function(kpi.kpi_function, targets, round(sum(results.values()), 2))
    elif kpi.kpi_type.lower() == 'average':
        return calculate_by_function(kpi.kpi_function, targets, round(sum(results.values())/len(results), 2))
    else:
        return calculate_by_function(kpi.kpi_function, targets, results[get_month_to_use_results(kpi, results)])


def get_month_to_use_results(kpi, result):
    if kpi.kpi_pms.pms_year_end_date < datetime.date.today():
        return 'march'
    else:
        this_month = datetime.date.today().strftime("%B").lower()
        last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%B").lower()

        if this_month in result:
            return this_month
        else:
            if last_month in result:
                return last_month
            else:
                return this_month


def calculate_by_function(function, target, result):
    score = 0
    if function and isinstance(float(target), float) and isinstance(float(result), float):
        if function.lower() == "minimize":
            if result == 0 and target >= result:
                score = 100
            else:
                score = round(target/result*100, 2)
        else:
            if target == 0 and target <= result:
                score = 100
            else:
                score = round(result/target*100, 2)
    return score


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
                                            assessment_scoring_use="Yes")
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
        score = round(score / assessments.count(), 2)
    return score


def calculate_one_assessment_score(staff, assessment):
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

    score = round((kpi_score + bu_score + company_score + assessment_score) * checkin_score / 100, 2)

    return score


def get_bu_score(staff, pms):
    score = 0

    if get_bu(staff) is not None:
        score = calculate_overall_kpi_score(get_bu(staff).level_head, pms)
    return score


def get_bu(staff):

    bu = None
    categories = []
    levels_up = []

    if staff.staff_bu_override is not None:
        return staff.staff_bu_override
    else:
        if not Level.objects.filter(level_head=staff, level_category__category_kpi_view=True):
            all_categories_up(staff.staff_category, categories)
            for category in categories:
                if category.category_kpi_view is True and category != categories[-1]:
                    if Level.objects.filter(level_category=category).exclude(level_head=staff):
                        all_levels_up(get_staff_level(staff), levels_up)
                        levels_up.append(get_staff_level(staff))
                        '''for level in Level.objects.filter(level_category=category).exclude(level_head=staff):
                            if level in levels_up:
                                bu = level
                                break
                        '''
                        for level in levels_up:
                            if level and level.level_category == category and level.level_head != staff:
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
