from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


# Extend User Model ==================================================================================================
class staff(models.Model):
    staff_person = models.OneToOneField(User, on_delete=models.CASCADE, related_name="toyota_kenya_staff_person")
    staff_Pf_Number = models.CharField(max_length=10)

    # Groups the staff belongs to
    staff_department = models.ForeignKey('department', on_delete=models.RESTRICT, null=True, blank=True,
                                         related_name="toyota_kenya_belongs_to_dept")
    staff_branch = models.ForeignKey('branch', on_delete=models.RESTRICT, null=True, blank=True,
                                     related_name="toyota_kenya_belongs_to_branch")
    staff_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, null=True, blank=True,
                                 related_name="toyota_kenya_belongs_to_bu")
    staff_team = models.ForeignKey('team', on_delete=models.RESTRICT, null=True, blank=True,
                                   related_name="toyota_kenya_belongs_to_team")

    # Staff leading groups
    staff_head_department = models.ForeignKey('department', on_delete=models.RESTRICT, blank=True, null=True,
                                              related_name="toyota_kenya_is_head_dept")
    staff_head_branch = models.ForeignKey('branch', on_delete=models.RESTRICT, null=True, blank=True,
                                          related_name="toyota_kenya_is_head_branch")
    staff_head_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, null=True, blank=True,
                                      related_name="toyota_kenya_is_head_bu")
    staff_head_team = models.ForeignKey('team', on_delete=models.RESTRICT, null=True, blank=True,
                                        related_name="toyota_kenya_is_head_team")

    md = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    staff_md = models.CharField(max_length=10, choices=md, blank=True, default='No', help_text='If user is MD')
    staff_bsc = models.CharField(max_length=10, choices=md, blank=True, default='No', help_text='If user is uses bsc')

    grade = {
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('T3', 'T3'),
        ('T4', 'T4'),
        ('T5', 'T5'),
        ('T6', 'T6'),
    }
    staff_grade = models.CharField(max_length=5, choices=grade, blank=True, help_text='user grade')

    def __str__(self):
        return self.staff_person.username


# PMS & Config ========================================================================================================
class pms(models.Model):
    pms_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Id for PMS")
    pms_name = models.CharField(max_length=200)
    pms_start_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_end_date = models.DateField(auto_now=False, auto_now_add=False)

    status = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    pms_status = models.CharField(max_length=10, choices=status, blank=True, default='Active', help_text='PMS Status')

    # Individual Config
    pms_individual_kpi_number = models.IntegerField(help_text='Number Of KPIs to be submitted by an individual')
    pms_individual_submit_start_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_individual_submit_end_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_individual_submit_results_date = models.FloatField(default=15)

    # Bu KPI Config
    pms_bu_kpi_number = models.IntegerField(help_text='Number Of KPIs to be submitted by a BU')
    pms_bu_submit_start_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_bu_submit_end_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_bu_submit_result_date = models.FloatField(default=15)

    # Company Config
    pms_company_kpi_number = models.IntegerField(help_text='Number Of KPIs to be submitted by the company')
    pms_company_submit_start_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_company_submit_end_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_company_submit_result_date = models.FloatField(default=15)

    checkin_number = models.IntegerField(help_text='Number Of Checkins to be submitted by the user', default=12)
    assessment_number = models.IntegerField(help_text='Number Of assessment to be done in the year', default=3)

    def __str__(self):
        """String for representing the Model object."""
        return self.pms_name


# Scoring matrix =====================================================================================================
class score_matrix(models.Model):

    matrix_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    matrix_pms = models.ForeignKey('pms', on_delete=models.RESTRICT, null=True)
    m_class = (
        ('MD', 'MD'),
        ('BU', 'BU'),
        ('staff', 'staff'),
    )
    matrix_class = models.CharField(max_length=10, choices=m_class, blank=True, help_text='PMS class')
    matrix_grade = models.ForeignKey('staff_grade', on_delete=models.RESTRICT, null=True)
    matrix_company_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_bu_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_individual_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_assessment_weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.matrix_class) + ' ' + str(self.matrix_grade)


class staff_grade(models.Model):
    grade_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identfier for staff grade")
    grade = models.CharField(max_length=10, blank=True, null=True, help_text='Staff Grade')

    def __str__(self):
        return self.grade


class matrix_checkin(models.Model):
    matrix_checkin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identfier ci matrix")
    matrix_pms = models.ForeignKey('pms', on_delete=models.RESTRICT, null=True)
    matrix_checkin_no = models.IntegerField(blank=True, null=True, help_text='No of Checkins')
    matrix_checkin_score = models.FloatField(blank=True, null=True, help_text='Staff Grade')

    def __str__(self):
        return str(self.matrix_pms.pms_name) + " _   " + str(self.matrix_checkin_no)


class kpi_months(models.Model):
    kpi_months_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    kpi_class = (
        ('Company', 'Company'),
        ('BU', 'BU'),
        ('Individual', 'Individual'),
    )
    kpi_months_class = models.CharField(max_length=10, choices=kpi_class, blank=True)
    kpi_months_pms = models.ForeignKey('pms', on_delete=models.RESTRICT, null=True)

    choice = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    kpi_month_april = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_may = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_june = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_july = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_august = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_september = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_october = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_november = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_december = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_january = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_february = models.CharField(max_length=5, choices=choice, blank=True)
    kpi_month_march = models.CharField(max_length=5, choices=choice, blank=True)


# Check In =============================================================================================================
class checkIn(models.Model):
    checkIn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    checkIn_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    checkIn_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_individual_user")
    checkIn_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_team_leader",
                                            null=True, blank=True)
    checkIn_submit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    checkIn_confirm_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    # Check In details
    checkIn_performance_area = models.TextField()
    checkIn_progress_discussed = models.TextField()
    checkIn_team_member_actions = models.TextField()
    checkIn_team_leader_support = models.TextField()
    checkIn_team_leader_comment = models.TextField(null=True, blank=True)

    months = (
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
    )

    status = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )
    checkIn_month = models.CharField(max_length=15, default=None, choices=months, null=True)
    checkIn_status = models.CharField(max_length=10, choices=status, blank=True, default='Pending',
                                      help_text='PMS Status')


# Assessments / Evaluation ============================================================================================
class evaluation(models.Model):
    evaluation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    evaluation_name = models.CharField(max_length=50)
    evaluation_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    evaluation_start_date = models.DateField(auto_now=False, auto_now_add=False)
    evaluation_end_date = models.DateField(auto_now=False, auto_now_add=False)
    eval_use = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    evaluation_use = models.CharField(max_length=15, default=None, null=True, choices=eval_use)

    def __str__(self):
        """String for representing the Model object."""
        return self.evaluation_name


class question_staff_evaluate_tl(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for Question")
    question_evaluation = models.ForeignKey('evaluation', on_delete=models.RESTRICT)
    question = models.TextField()

    def __str__(self):
        """String for representing the Model object."""
        return self.question


class question_tl_evaluate_staff(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for Question")
    question_evaluation = models.ForeignKey('evaluation', on_delete=models.RESTRICT)
    question = models.TextField()

    def __str__(self):
        """String for representing the Model object."""
        return self.question


class evaluation_responses(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    response_evaluation = models.ForeignKey(evaluation, on_delete=models.RESTRICT)
    results = (
        ('Strongly Agree', 'Strongly Agree'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Strongly Disagree', 'Strongly Disagree'),
    )
    response = models.CharField(max_length=20, blank=True, choices=results, default=None)
    response_score = models.FloatField()


class done_staff_evaluates_tl(models.Model):
    done_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier done evaluation")
    done_evaluation = models.ForeignKey('evaluation', on_delete=models.RESTRICT)
    done_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_staff_evaluating")
    done_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_tl_evaluated")

    results = (
        ('Strongly Agree', 'Strongly Agree'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Strongly Disagree', 'Strongly Disagree'),
    )

    done_q1 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q1",
                                blank=True,
                                default=None, null=True)
    done_q2 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q2",
                                blank=True,
                                default=None, null=True)
    done_q3 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q3",
                                blank=True,
                                default=None, null=True)
    done_q4 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q4",
                                blank=True,
                                default=None, null=True)
    done_q5 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q5",
                                blank=True,
                                default=None, null=True)
    done_q6 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q6",
                                blank=True,
                                default=None, null=True)
    done_q7 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="toyota_kenya_q7",
                                blank=True,
                                default=None, null=True)

    score_q1 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q2 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q3 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q4 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q5 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q6 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q7 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)

    score_q1_comment = models.TextField(default=None, blank=True, null=True)
    score_q2_comment = models.TextField(default=None, blank=True, null=True)
    score_q3_comment = models.TextField(default=None, blank=True, null=True)
    score_q4_comment = models.TextField(default=None, blank=True, null=True)
    score_q5_comment = models.TextField(default=None, blank=True, null=True)
    score_q6_comment = models.TextField(default=None, blank=True, null=True)
    score_q7_comment = models.TextField(default=None, blank=True, null=True)


class done_tl_evaluates_staff(models.Model):
    done_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier done evaluation")
    done_evaluation = models.ForeignKey('evaluation', on_delete=models.RESTRICT)
    done_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_tl_evaluating")
    done_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_staff_evaluated")

    results = (
        ('Strongly Agree', 'Strongly Agree'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Strongly Disagree', 'Strongly Disagree'),
    )

    done_q1 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q1",
                                blank=True,
                                default=None, null=True)
    done_q2 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q2",
                                blank=True,
                                default=None, null=True)
    done_q3 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q3",
                                blank=True,
                                default=None, null=True)
    done_q4 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q4",
                                blank=True,
                                default=None, null=True)
    done_q5 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q5",
                                blank=True,
                                default=None, null=True)
    done_q6 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q6",
                                blank=True,
                                default=None, null=True)
    done_q7 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="toyota_kenya_q7",
                                blank=True,
                                default=None, null=True)

    score_q1 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q2 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q3 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q4 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q5 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q6 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)
    score_q7 = models.CharField(max_length=20, choices=results, blank=True, default=None, null=True)

    score_q1_comment = models.TextField(default=None, blank=True, null=True)
    score_q2_comment = models.TextField(default=None, blank=True, null=True)
    score_q3_comment = models.TextField(default=None, blank=True, null=True)
    score_q4_comment = models.TextField(default=None, blank=True, null=True)
    score_q5_comment = models.TextField(default=None, blank=True, null=True)
    score_q6_comment = models.TextField(default=None, blank=True, null=True)
    score_q7_comment = models.TextField(default=None, blank=True, null=True)


class responses_staff_evaluate_tl(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for responses")
    response_question = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT)
    response_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_responding_staff")
    response_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT,
                                             related_name="toyota_kenya_responded_team_leader")
    response_score = models.IntegerField()
    response_comment = models.TextField()


class responses_tl_evaluate_staff(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for responses")
    response_question = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT)
    response_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT,
                                             related_name="toyota_kenya_responding_team_leader")
    response_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_responded_staff")
    response_score = models.IntegerField()
    response_comment = models.TextField()


# Groups ============================================================================================================
class bu(models.Model):
    bu_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for BU")
    bu_name = models.CharField(max_length=200)
    bu_abbreviation = models.CharField(max_length=10, null=True, blank=True)
    bu_mail = models.CharField(max_length=50, null=True, blank=True)
    bu_contact = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.bu_name


class branch(models.Model):
    branch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for branch")
    branch_name = models.CharField(max_length=200)
    branch_abbreviation = models.CharField(max_length=10)
    branch_mail = models.CharField(max_length=50)
    branch_contact = models.CharField(max_length=50)

    def __str__(self):
        """String for representing the Model object."""
        return self.branch_name


class department(models.Model):
    department_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for department")
    department_name = models.CharField(max_length=200)
    department_abbreviation = models.CharField(max_length=10)
    department_mail = models.CharField(max_length=50)
    department_contact = models.CharField(max_length=50)

    def __str__(self):
        """String for representing the Model object."""
        return self.department_name


class team(models.Model):
    team_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for department")
    team_name = models.CharField(max_length=200)
    team_motto = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.team_name


# BSC
class bsc(models.Model):
    bsc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique id for bsc")
    bsc_pms = models.ForeignKey('pms', on_delete=models.RESTRICT, null=True)
    bsc_name = models.CharField(max_length=50)
    bsc_weight = models.FloatField()

    def __str__(self):
        return self.bsc_name


class bu_bsc(models.Model):
    bu_bsc_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bu_bsc_pillar = models.ForeignKey('bsc', on_delete=models.RESTRICT)
    bu_bsc_bu = models.ForeignKey('bu', on_delete=models.RESTRICT)
    bsc_pillar_weight = models.FloatField()

    def __str__(self):
        return str(self.bu_bsc_bu) + " - " + str(self.bu_bsc_pillar)


# KPIs ===============================================================================================================
class individual_Kpi(models.Model):
    individual_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                         help_text="Unique Identifier for individual KPI")
    individual_kpi_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    individual_kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_user_submitting")

    # Approvals
    individual_kpi_team_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                            related_name="toyota_kenya_team_leader_approval", null=True,
                                                            blank=True)
    individual_kpi_bu_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                          related_name="toyota_kenya_bu_leader_approval", null=True,
                                                          blank=True)
    # end approvals

    individual_kpi_title = models.CharField(max_length=200)
    individual_kpi_details = models.TextField(null=True, blank=True)
    individual_kpi_criteria = models.CharField(max_length=100)
    individual_kpi_weight = models.FloatField(default=20)
    individual_kpi_units = models.CharField(max_length=5, null=True, blank=True)

    function = (
        ('maximize', 'maximize'),
        ('minimize', 'minimize'),
    )
    individual_kpi_function = models.CharField(max_length=10, choices=function, blank=True, default='maximize',
                                               help_text='KPI categorize function')
    individual_kpi_april_score = models.FloatField(null=True, blank=True)
    individual_kpi_may_score = models.FloatField(null=True, blank=True)
    individual_kpi_june_score = models.FloatField(null=True, blank=True)
    individual_kpi_july_score = models.FloatField(null=True, blank=True)
    individual_kpi_august_score = models.FloatField(null=True, blank=True)
    individual_kpi_september_score = models.FloatField(null=True, blank=True)
    individual_kpi_october_score = models.FloatField(null=True, blank=True)
    individual_kpi_november_score = models.FloatField(null=True, blank=True)
    individual_kpi_december_score = models.FloatField(null=True, blank=True)
    individual_kpi_january_score = models.FloatField(null=True, blank=True)
    individual_kpi_february_score = models.FloatField(null=True, blank=True)
    individual_kpi_march_score = models.FloatField(null=True, blank=True)

    individual_kpi_april_target = models.FloatField(default=None)
    individual_kpi_may_target = models.FloatField(default=None)
    individual_kpi_june_target = models.FloatField(default=None)
    individual_kpi_july_target = models.FloatField(default=None)
    individual_kpi_august_target = models.FloatField(default=None)
    individual_kpi_september_target = models.FloatField(default=None)
    individual_kpi_october_target = models.FloatField(default=None)
    individual_kpi_november_target = models.FloatField(default=None)
    individual_kpi_december_target = models.FloatField(default=None)
    individual_kpi_january_target = models.FloatField(default=None)
    individual_kpi_february_target = models.FloatField(default=None)
    individual_kpi_march_target = models.FloatField(default=None)

    approve = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    )
    individual_kpi_april_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                          default='Not Approved', )
    individual_kpi_may_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                        default='Not Approved', )
    individual_kpi_june_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                         default='Not Approved', )
    individual_kpi_july_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                         default='Not Approved', )
    individual_kpi_august_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                           default='Not Approved', )
    individual_kpi_september_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                              default='Not Approved', )
    individual_kpi_october_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                            default='Not Approved', )
    individual_kpi_november_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    individual_kpi_december_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    individual_kpi_january_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                            default='Not Approved', )
    individual_kpi_february_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    individual_kpi_march_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                          default='Not Approved', )

    individual_kpi_submit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    individual_kpi_approval1_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    individual_kpi_approval2_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    individual_kpi_last_edit = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = (
        ('Pending', 'Pending'),
        ('Approved 1', 'Approval1 - By Team Leader'),
        ('Approved 2', 'Approval2 - By BU Head'),
        ('Rejected 1', 'Rejected - By Team Leader'),
        ('Rejected 2', 'Rejected - By BU Head'),
        ('Edit', 'Edit Mode'),
    )
    individual_kpi_status = models.CharField(max_length=40, choices=status, blank=True, default='Pending',
                                             help_text='KPI categorize function')

    def get_absolute_url(self):
        return reverse('kpi-detail', args=[self.individual_kpi_id])

    def __str__(self):
        return self.individual_kpi_title


class bu_kpi(models.Model):
    bu_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for BU KPI")
    bu_kpi_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    bu_kpi_bsc = models.ForeignKey('bsc', on_delete=models.RESTRICT, default=None)
    bu_kpi_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, related_name="toyota_kenya_Bu_identity")
    # Approvals
    bu_kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_Bu_submitting",
                                       null=True,
                                       blank=True)
    bu_kpi_criteria = models.CharField(max_length=100, null=True, blank=True)
    bu_kpi_team_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                    related_name="toyota_kenya_bu_team_leader_approval", null=True,
                                                    blank=True)
    # end approvals

    bu_kpi_title = models.CharField(max_length=200)
    bu_kpi_details = models.TextField()
    bu_kpi_weight = models.FloatField(null=True, blank=True)
    bu_kpi_units = models.CharField(max_length=5, null=True, blank=True)

    function = (
        ('maximize', 'maximize'),
        ('minimize', 'minimize'),
    )
    bu_kpi_function = models.CharField(max_length=10, choices=function, blank=True, default='Pending',
                                       help_text='KPI categorize function')
    bu_kpi_april_score = models.FloatField(null=True, blank=True)
    bu_kpi_may_score = models.FloatField(null=True, blank=True)
    bu_kpi_june_score = models.FloatField(null=True, blank=True)
    bu_kpi_july_score = models.FloatField(null=True, blank=True)
    bu_kpi_august_score = models.FloatField(null=True, blank=True)
    bu_kpi_september_score = models.FloatField(null=True, blank=True)
    bu_kpi_october_score = models.FloatField(null=True, blank=True)
    bu_kpi_november_score = models.FloatField(null=True, blank=True)
    bu_kpi_december_score = models.FloatField(null=True, blank=True)
    bu_kpi_january_score = models.FloatField(null=True, blank=True)
    bu_kpi_february_score = models.FloatField(null=True, blank=True)
    bu_kpi_march_score = models.FloatField(null=True, blank=True)

    approve = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    )
    bu_kpi_april_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                          default='Not Approved', )
    bu_kpi_may_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                        default='Not Approved', )
    bu_kpi_june_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                         default='Not Approved', )
    bu_kpi_july_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                         default='Not Approved', )
    bu_kpi_august_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                           default='Not Approved', )
    bu_kpi_september_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                              default='Not Approved', )
    bu_kpi_october_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                            default='Not Approved', )
    bu_kpi_november_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    bu_kpi_december_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    bu_kpi_january_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                            default='Not Approved', )
    bu_kpi_february_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                             default='Not Approved', )
    bu_kpi_march_score_approve = models.CharField(max_length=13, choices=approve, blank=True,
                                                          default='Not Approved', )    

    bu_kpi_submit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    bu_kpi_approval_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    bu_kpi_last_edit = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Edit', 'Edit Mode'),
    )
    bu_kpi_status = models.CharField(max_length=10, choices=status, blank=True, default='Pending',
                                     help_text='KPI status')

    type = (
        ('', ''),
        ('Addition', 'Addition'),
        ('Average', 'Average'),
        ('YTD', 'YTD'),
    )
    bu_kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='cumulative', )

    bu_kpi_s_score = models.FloatField(null=True, blank=True)
    bu_kpi_a_score = models.FloatField(null=True, blank=True)
    bu_kpi_b_score = models.FloatField(null=True, blank=True)
    bu_kpi_c_score = models.FloatField(null=True, blank=True)
    bu_kpi_d_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.bu_kpi_title


class company_kpi(models.Model):
    company_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                      help_text="Unique Identifier for company KPI")
    company_kpi_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    company_kpi_bsc = models.ForeignKey('bsc', on_delete=models.RESTRICT, default=None)
    company_kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="toyota_kenya_person_submitting",
                                         null=True,
                                         blank=True)
    company_kpi_title = models.CharField(max_length=200)
    company_kpi_details = models.TextField()
    company_kpi_weight = models.FloatField(null=True, blank=True)
    company_kpi_units = models.CharField(max_length=5, null=True, blank=True)

    function = (
        ('maximize', 'maximize'),
        ('minimize', 'minimize'),
    )
    company_kpi_function = models.CharField(max_length=10, choices=function, blank=True, default='Pending',
                                            help_text='KPI categorize function')
    company_kpi_april_score = models.FloatField(null=True, blank=True)
    company_kpi_may_score = models.FloatField(null=True, blank=True)
    company_kpi_june_score = models.FloatField(null=True, blank=True)
    company_kpi_july_score = models.FloatField(null=True, blank=True)
    company_kpi_august_score = models.FloatField(null=True, blank=True)
    company_kpi_september_score = models.FloatField(null=True, blank=True)
    company_kpi_october_score = models.FloatField(null=True, blank=True)
    company_kpi_november_score = models.FloatField(null=True, blank=True)
    company_kpi_december_score = models.FloatField(null=True, blank=True)
    company_kpi_january_score = models.FloatField(null=True, blank=True)
    company_kpi_february_score = models.FloatField(null=True, blank=True)
    company_kpi_march_score = models.FloatField(null=True, blank=True)

    company_kpi_submit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    company_kpi_last_edit = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    status = (
        ('Pending', 'maximize'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Edit', 'Edit Mode'),
    )
    company_kpi_status = models.CharField(max_length=10, choices=status, blank=True, default='Approved')
    type = (
        ('Average', 'Average'),
        ('YTD', 'YTD'),
        ('Addition', 'Addition'),
    )
    company_kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='cumulative', )
    company_kpi_s_score = models.FloatField(null=True, blank=True)
    company_kpi_a_score = models.FloatField(null=True, blank=True)
    company_kpi_b_score = models.FloatField(null=True, blank=True)
    company_kpi_c_score = models.FloatField(null=True, blank=True)
    company_kpi_d_score = models.FloatField(null=True, blank=True)


# Notifications =====================================================================================================
class notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification_type = models.CharField(max_length=10)
    notification_sender = models.ForeignKey(User, on_delete=models.RESTRICT,
                                            related_name="toyota_kenya_notification_Sender")
    notification_receiver = models.ForeignKey(User, on_delete=models.RESTRICT,
                                              related_name="toyota_kenya_notification_receiver")
    notification_title = models.CharField(max_length=15)
    notification_message = models.TextField()
    notification_date = models.DateField(auto_now=False, auto_now_add=False)

    status = (
        ('unread', 'unread'),
        ('read', 'read'),
        ('deleted', 'deleted'),
    )
    notification_status = models.CharField(max_length=10, choices=status, default="unread")
