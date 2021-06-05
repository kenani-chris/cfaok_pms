from django.db import models
from django.contrib.auth.models import User
import uuid
from django.urls import reverse


# Extend User Model ==================================================================================================
class staff(models.Model):
    staff_person = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tydia_staff_person")
    staff_Pf_Number = models.CharField(max_length=10)
    staff_email_address = models.CharField(max_length=100)

    # Groups the staff belongs to
    staff_department = models.ForeignKey('department', on_delete=models.RESTRICT, null=True, blank=True,
                                         related_name="tydia_belongs_to_dept")
    staff_branch = models.ForeignKey('branch', on_delete=models.RESTRICT, null=True, blank=True,
                                     related_name="tydia_belongs_to_branch")
    staff_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, null=True, blank=True, related_name="tydia_belongs_to_bu")
    staff_team = models.ForeignKey('team', on_delete=models.RESTRICT, null=True, blank=True,
                                   related_name="tydia_belongs_to_team")

    # Staff leading groups
    staff_head_department = models.ForeignKey('department', on_delete=models.RESTRICT, blank=True, null=True,
                                              related_name="tydia_is_head_dept")
    staff_head_branch = models.ForeignKey('branch', on_delete=models.RESTRICT, null=True, blank=True,
                                          related_name="tydia_is_head_branch")
    staff_head_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, null=True, blank=True, related_name="tydia_is_head_bu")
    staff_head_team = models.ForeignKey('team', on_delete=models.RESTRICT, null=True, blank=True,
                                        related_name="tydia_is_head_team")

    md = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    staff_md = models.CharField(max_length=10, choices=md, blank=True, default='No', help_text='If user is MD')

    grade = {
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('T3', 'T3'),
        ('T4', 'T4'),
        ('T5', 'T5'),
        ('T6', 'T6'),
    }
    staff_grade = models.CharField(max_length=5, choices=grade, blank=True, help_text='user grade')

    company = {
        ('cfao_kenya', 'cfao_kenya'),
        ('cfao_agri', 'cfao_agri'),
        ('tamk', 'tamk'),
        ('toyota_kenya', 'toyota_kenya'),
        ('tydia', 'tydia'),
    }
    staff_company = models.CharField(max_length=15, choices=company, blank=True, help_text='user grade')


def __str__(self):
    return self.staff_person.get_full_name


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

    # Bu KPI Config
    bu_individual_kpi_number = models.IntegerField(help_text='Number Of KPIs to be submitted by a BU')
    bu_individual_submit_start_date = models.DateField(auto_now=False, auto_now_add=False)
    bu_individual_submit_end_date = models.DateField(auto_now=False, auto_now_add=False)

    # Company Config
    company_individual_kpi_number = models.IntegerField(help_text='Number Of KPIs to be submitted by the company')
    company_individual_submit_start_date = models.DateField(auto_now=False, auto_now_add=False)
    company_individual_submit_end_date = models.DateField(auto_now=False, auto_now_add=False)

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
        ('Non_BU', 'Non_BU'),
        ('staff', 'staff'),
    )
    matrix_class = models.CharField(max_length=10, choices=m_class, blank=True, help_text='PMS class')
    matrix_company_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_bu_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_individual_kpi_weight = models.FloatField(null=True, blank=True)
    matrix_assessment_weight = models.FloatField(null=True, blank=True)


# Check In =============================================================================================================
class checkIn(models.Model):
    checkIn_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    checkIn_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    checkIn_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_individual_user")
    checkIn_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_team_leader", null=True,
                                            blank=True)
    checkIn_submit_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    checkIn_confirm_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    # Check In details
    checkIn_performance_area = models.TextField()
    checkIn_progress_discussed = models.TextField()
    checkIn_team_member_actions = models.TextField()
    checkIn_team_leader_support = models.TextField()
    checkIn_team_leader_comment = models.TextField()

    status = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )
    checkIn_month = models.CharField(max_length=15, default=None)
    checkIn_status = models.CharField(max_length=10, choices=status, blank=True, default='Pending',
                                      help_text='PMS Status')


# Assessments / Evaluation ============================================================================================
class evaluation(models.Model):
    evaluation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    evaluation_name = models.CharField(max_length=50)
    evaluation_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    evaluation_start_date = models.DateField(auto_now=False, auto_now_add=False)
    evaluation_end_date = models.DateField(auto_now=False, auto_now_add=False)

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


class done_staff_evaluates_tl(models.Model):
    done_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier done evaluation")
    done_evaluation = models.ForeignKey('evaluation', on_delete=models.RESTRICT)
    done_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_staff_evaluating")
    done_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_tl_evaluated")

    results = (
        ('Strongly Agree', 'Strongly Agree'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Strongly Disagree', 'Strongly Disagree'),
    )

    done_q1 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q1", blank=True,
                                default=None, null=True)
    done_q2 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q2", blank=True,
                                default=None, null=True)
    done_q3 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q3", blank=True,
                                default=None, null=True)
    done_q4 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q4", blank=True,
                                default=None, null=True)
    done_q5 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q5", blank=True,
                                default=None, null=True)
    done_q6 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q6", blank=True,
                                default=None, null=True)
    done_q7 = models.ForeignKey('question_staff_evaluate_tl', on_delete=models.RESTRICT, related_name="tydia_q7", blank=True,
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
    done_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_tl_evaluating")
    done_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_staff_evaluated")

    results = (
        ('Strongly Agree', 'Strongly Agree'),
        ('Agree', 'Agree'),
        ('Disagree', 'Disagree'),
        ('Strongly Disagree', 'Strongly Disagree'),
    )

    done_q1 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q1", blank=True,
                                default=None, null=True)
    done_q2 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q2", blank=True,
                                default=None, null=True)
    done_q3 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q3", blank=True,
                                default=None, null=True)
    done_q4 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q4", blank=True,
                                default=None, null=True)
    done_q5 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q5", blank=True,
                                default=None, null=True)
    done_q6 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q6", blank=True,
                                default=None, null=True)
    done_q7 = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT, related_name="tydia_q7", blank=True,
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
    response_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_responding_staff")
    response_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_responded_team_leader")
    response_score = models.IntegerField()
    response_comment = models.TextField()


class responses_tl_evaluate_staff(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier for responses")
    response_question = models.ForeignKey('question_tl_evaluate_staff', on_delete=models.RESTRICT)
    response_team_leader = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_responding_team_leader")
    response_staff = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_responded_staff")
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


# KPIs ===============================================================================================================
class individual_Kpi(models.Model):
    individual_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                         help_text="Unique Identifier for individual KPI")
    individual_kpi_pms = models.ForeignKey('pms', on_delete=models.RESTRICT)
    individual_kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_user_submitting")

    # Approvals
    individual_kpi_team_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                            related_name="tydia_team_leader_approval", null=True, blank=True)
    individual_kpi_bu_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                          related_name="tydia_bu_leader_approval", null=True, blank=True)
    # end approvals

    individual_kpi_title = models.CharField(max_length=200)
    individual_kpi_details = models.TextField(null=True, blank=True)
    individual_kpi_criteria = models.CharField(max_length=100)
    individual_kpi_target = models.FloatField()
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
    type = (
        ('cumulative', 'cumulative'),
        ('YTD', 'YTD'),
    )
    individual_kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='cumulative', )

    def get_absolute_url(self):
        return reverse('kpi-detail', args=[self.individual_kpi_id])

    def __str__(self):
        return self.individual_kpi_title


class bu_kpi(models.Model):
    bu_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Identifier for BU KPI")
    bu_kpi_pms_id = models.ForeignKey('pms', on_delete=models.RESTRICT)
    bu_kpi_bu = models.ForeignKey('bu', on_delete=models.RESTRICT, related_name="tydia_Bu_identity")
    # Approvals
    bu_kpi_bu_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_Bu_submitting", null=True,
                                       blank=True)
    bu_kpi_team_leader_approval = models.ForeignKey(User, on_delete=models.RESTRICT,
                                                    related_name="tydia_bu_team_leader_approval", null=True, blank=True)
    # end approvals

    bu_kpi_title = models.CharField(max_length=200)
    bu_kpi_details = models.TextField()
    bu_kpi_target = models.FloatField()
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
        ('cumulative', 'cumulative'),
        ('YTD', 'YTD'),
    )
    bu_kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='cumulative', )

    def __str__(self):
        return self.bu_kpi_title


class company_kpi(models.Model):
    company_kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                      help_text="Unique Identifier for company KPI")
    company_kpi_pms_id = models.ForeignKey('pms', on_delete=models.RESTRICT)
    company_kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_person_submitting", null=True,
                                         blank=True)
    company_kpi_title = models.CharField(max_length=200)
    company_kpi_details = models.TextField()
    company_kpi_target = models.FloatField()
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
        ('cumulative', 'cumulative'),
        ('YTD', 'YTD'),
    )
    company_kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='cumulative', )


# Notifications =====================================================================================================
class notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    notification_type = models.CharField(max_length=10)
    notification_sender = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_notification_Sender")
    notification_receiver = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="tydia_notification_receiver")
    notification_title = models.CharField(max_length=15)
    notification_message = models.TextField()
    notification_date = models.DateField(auto_now=False, auto_now_add=False)

    status = (
        ('unread', 'unread'),
        ('read', 'read'),
        ('deleted', 'deleted'),
    )
    notification_status = models.CharField(max_length=10, choices=status, default="unread")