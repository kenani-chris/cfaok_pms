from django.db import models
from django.contrib.auth.models import User
import uuid
from colorfield.fields import ColorField


# Password Expiry =====================================================================================================
class PasswordChange(models.Model):
    change_id = models.AutoField(primary_key=True)
    change_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    change_last_date = models.DateTimeField(auto_now=False, null=True)


# Company Info
class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    company_logo = models.ImageField(upload_to='company')
    company_status = models.BooleanField(default=False)
    company_color1 = ColorField(default='#00a8b4')
    company_color2 = ColorField(default='#d9d9d9')
    company_color3 = ColorField(default='#33393f')

    def __str__(self):
        return self.company_name


# Staff Account =======================================================================================================
class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_person = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="Staff_person")
    staff_pf_number = models.CharField(max_length=10)
    staff_grade = models.ForeignKey('StaffGrades', on_delete=models.RESTRICT, null=True)
    staff_active = models.BooleanField(default=True)
    staff_superuser = models.BooleanField(default=False)
    staff_visibility = models.BooleanField(default=True)
    staff_company = models.ForeignKey('Company', on_delete=models.RESTRICT)
    staff_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT, null=True, default=None)
    staff_date_created = models.DateTimeField(auto_now=False, null=True)
    staff_bu_override = models.ForeignKey('Level', on_delete=models.RESTRICT, null=True, blank=True, default=None)

    def __str__(self):
        return self.staff_person.get_full_name() + " - PF " + self.staff_pf_number


# Employee Grades =====================================================================================================
class StaffGrades(models.Model):
    staff_grade_id = models.AutoField(primary_key=True)
    staff_grade_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.staff_grade_name


# PMS =============================================================================================================
class PMS(models.Model):
    pms_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    pms_name = models.CharField(max_length=200, unique=True)
    pms_description = models.TextField(max_length=200, help_text="One can use the field to give motto, or focus "
                                                                 "for the year")
    pms_year_start_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_year_end_date = models.DateField(auto_now=False, auto_now_add=False)
    pms_active = models.BooleanField(default=True)
    pms_company = models.ForeignKey('Company', on_delete=models.RESTRICT)
    pms_cap_results = models.BooleanField(default=False, help_text="By checking this all results will not exceed 100%")

    def __str__(self):
        return self.pms_name


# KPI Submission Timeline
class SubmissionKPI(models.Model):
    submission_id = models.AutoField(primary_key=True)
    submission_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    submission_level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)
    submission_start_date = models.DateTimeField(auto_now=False)
    submission_end_date = models.DateTimeField(auto_now=False)
    submission_minimum_number = models.IntegerField(default=5)
    submission_maximum_number = models.IntegerField(default=10)

    # Specify when monthly results should be populated, count by end of month days
    submission_april_results = models.IntegerField(default=15)
    submission_may_results = models.IntegerField(default=15)
    submission_june_results = models.IntegerField(default=15)
    submission_july_results = models.IntegerField(default=15)
    submission_august_results = models.IntegerField(default=15)
    submission_september_results = models.IntegerField(default=15)
    submission_october_results = models.IntegerField(default=15)
    submission_november_results = models.IntegerField(default=15)
    submission_december_results = models.IntegerField(default=15)
    submission_january_results = models.IntegerField(default=15)
    submission_february_results = models.IntegerField(default=15)
    submission_march_results = models.IntegerField(default=15)

    # KPI Populate Override
    submission_april_results_calculation = models.BooleanField(default=True)
    submission_may_results_calculation = models.BooleanField(default=True)
    submission_june_results_calculation = models.BooleanField(default=True)
    submission_july_results_calculation = models.BooleanField(default=True)
    submission_august_results_calculation = models.BooleanField(default=True)
    submission_september_results_calculation = models.BooleanField(default=True)
    submission_october_results_calculation = models.BooleanField(default=True)
    submission_november_results_calculation = models.BooleanField(default=True)
    submission_december_results_calculation = models.BooleanField(default=True)
    submission_january_results_calculation = models.BooleanField(default=True)
    submission_february_results_calculation = models.BooleanField(default=True)
    submission_march_results_calculation = models.BooleanField(default=True)

    # KPI calculation
    submission_april_results_override = models.BooleanField(default=False)
    submission_may_results_override = models.BooleanField(default=False)
    submission_june_results_override = models.BooleanField(default=False)
    submission_july_results_override = models.BooleanField(default=False)
    submission_august_results_override = models.BooleanField(default=False)
    submission_september_results_override = models.BooleanField(default=False)
    submission_october_results_override = models.BooleanField(default=False)
    submission_november_results_override = models.BooleanField(default=False)
    submission_december_results_override = models.BooleanField(default=False)
    submission_january_results_override = models.BooleanField(default=False)
    submission_february_results_override = models.BooleanField(default=False)
    submission_march_results_override = models.BooleanField(default=False)


# Check In =============================================================================================================
class CheckIn(models.Model):
    check_in_id = models.AutoField(primary_key=True)
    check_in_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    check_in_Staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)
    check_in_submit_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    check_in_approver = models.ForeignKey('Staff', on_delete=models.RESTRICT, null=True, blank=True,
                                          related_name="Approver")
    check_in_approval_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    check_in_performance_area = models.TextField(null=True, blank=True)
    check_in_progress_discussed = models.TextField(null=True, blank=True)
    check_in_team_member_actions = models.TextField(null=True, blank=True)
    check_in_team_leader_support = models.TextField(null=True, blank=True)
    check_in_team_leader_comment = models.TextField(null=True, blank=True)
    check_in_declaration = models.TextField(default=None)

    check_in_months = (
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
        ('Edit', 'Edit'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    check_in_month = models.CharField(max_length=15, default=None, choices=check_in_months, null=True)
    check_in_status = models.CharField(max_length=10, choices=status, blank=True, default='Pending',
                                       help_text='PMS Status')
    check_in_last_edit = models.DateTimeField(auto_now=True)


class SubmissionCheckin(models.Model):
    submission_id = models.AutoField(primary_key=True)
    submission_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    submission_level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)
    
    # Submission checkin submit deadline from end month
    submission_april_results = models.IntegerField(default=0)
    submission_may_results = models.IntegerField(default=0)
    submission_june_results = models.IntegerField(default=0)
    submission_july_results = models.IntegerField(default=0)
    submission_august_results = models.IntegerField(default=0)
    submission_september_results = models.IntegerField(default=0)
    submission_october_results = models.IntegerField(default=0)
    submission_november_results = models.IntegerField(default=0)
    submission_december_results = models.IntegerField(default=0)
    submission_january_results = models.IntegerField(default=0)
    submission_february_results = models.IntegerField(default=0)
    submission_march_results = models.IntegerField(default=0)

    # Specify scores you get in populating a said number of checkin
    submission_zero_results = models.IntegerField(default=0)
    submission_one_results = models.IntegerField(default=0)
    submission_two_results = models.IntegerField(default=0)
    submission_three_results = models.IntegerField(default=10)
    submission_four_results = models.IntegerField(default=20)
    submission_five_results = models.IntegerField(default=30)
    submission_six_results = models.IntegerField(default=40)
    submission_seven_results = models.IntegerField(default=50)
    submission_eight_results = models.IntegerField(default=60)
    submission_nine_results = models.IntegerField(default=70)
    submission_ten_results = models.IntegerField(default=80)
    submission_eleven_results = models.IntegerField(default=90)
    submission_twelve_results = models.IntegerField(default=100)

    # CheckIn to be used in calculation
    submission_april_checkin_calculation = models.BooleanField(default=True)
    submission_may_checkin_calculation = models.BooleanField(default=True)
    submission_june_checkin_calculation = models.BooleanField(default=True)
    submission_july_checkin_calculation = models.BooleanField(default=True)
    submission_august_checkin_calculation = models.BooleanField(default=True)
    submission_september_checkin_calculation = models.BooleanField(default=True)
    submission_october_checkin_calculation = models.BooleanField(default=True)
    submission_november_checkin_calculation = models.BooleanField(default=True)
    submission_december_checkin_calculation = models.BooleanField(default=True)
    submission_january_checkin_calculation = models.BooleanField(default=True)
    submission_february_checkin_calculation = models.BooleanField(default=True)
    submission_march_checkin_calculation = models.BooleanField(default=True)

    # Submission deadline override
    submission_april_checkin_override = models.BooleanField(default=False)
    submission_may_checkin_override = models.BooleanField(default=False)
    submission_june_checkin_override = models.BooleanField(default=False)
    submission_july_checkin_override = models.BooleanField(default=False)
    submission_august_checkin_override = models.BooleanField(default=False)
    submission_september_checkin_override = models.BooleanField(default=False)
    submission_october_checkin_override = models.BooleanField(default=False)
    submission_november_checkin_override = models.BooleanField(default=False)
    submission_december_checkin_override = models.BooleanField(default=False)
    submission_january_checkin_override = models.BooleanField(default=False)
    submission_february_checkin_override = models.BooleanField(default=False)
    submission_march_checkin_override = models.BooleanField(default=False)

    submission_minimum_score_override = models.FloatField(default=None, blank=True, null=True)
    submission_maximum_score_override = models.FloatField(default=None, blank=True, null=True)


# Matrix ===========================================================================================================
class Matrix(models.Model):
    matrix_id = models.AutoField(primary_key=True)
    matrix_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT, null=True)
    matrix_grade = models.ForeignKey('StaffGrades', on_delete=models.RESTRICT, null=True, blank=True)
    matrix_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT, null=True, blank=True)
    matrix_checkin_weight = models.FloatField(null=True, blank=True, default=100)
    matrix_kpi_weight = models.FloatField(null=True, blank=True, default=50)
    matrix_assessment_weight = models.FloatField(null=True, blank=True, default=20)
    matrix_bu_weight = models.FloatField(null=True, blank=True, default=20)
    matrix_company_weight = models.FloatField(null=True, blank=True, default=10)


# Assessment ===========================================================================================================
class Assessment(models.Model):
    assessment_id = models.AutoField(primary_key=True)
    assessment_name = models.CharField(max_length=50, unique=True)
    assessment_details = models.TextField()
    assessment_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    assessment_start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    assessment_end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    assessment_use = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    assessment_min_score = models.FloatField(default=0)
    assessment_max_score = models.FloatField(default=10)
    assessment_scoring_use = models.CharField(max_length=3, default=None, null=True, choices=assessment_use)

    def __str__(self):
        return self.assessment_name


# Questions ===========================================================================================================
class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_assessment = models.ForeignKey('Assessment', on_delete=models.RESTRICT)
    question = models.TextField()

    direction = (
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
    )
    question_direction = models.CharField(max_length=6, choices=direction)

    def __str__(self):
        return self.question


# Question Responses===================================================================================================
class QuestionResponses(models.Model):
    response_id = models.AutoField(primary_key=True)
    response_question = models.ForeignKey('Questions', on_delete=models.RESTRICT)
    response_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT, related_name="Response_staff")
    response_evaluated = models.ForeignKey('Staff', on_delete=models.RESTRICT, related_name="Response_staff_evaluated")
    response_comment = models.TextField(blank=True, null=True, default=None)
    response_submitted = models.FloatField(default=None)
    response_submitted_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    response_last_edit = models.DateTimeField(auto_now=True)


# Levels/Groups =======================================================================================================
class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=200, unique=True)
    level_description = models.TextField()
    level_parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    level_head = models.ForeignKey('Staff', on_delete=models.RESTRICT, related_name="Head_level")
    level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT,
                                       related_name="level_category", default=None)

    def __str__(self):
        return self.level_name


# Levels/Groups =======================================================================================================
class LevelCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200, unique=True)
    category_description = models.TextField()
    category_parent = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    category_kpi_view = models.BooleanField(default=False)
    category_company = models.ForeignKey('Company', on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return self.category_name


# LevelMembership =====================================================================================================
class LevelMembership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    membership_level = models.ForeignKey('Level', on_delete=models.RESTRICT)
    membership_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)
    membership_is_active = models.BooleanField(default=True)


# KPIs ===============================================================================================================
class KPI(models.Model):
    kpi_id = models.AutoField(primary_key=True)
    kpi_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    kpi_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)
    kpi_title = models.CharField(max_length=200)
    kpi_details = models.TextField(null=True, blank=True)
    kpi_criteria = models.TextField(null=True, blank=True)
    kpi_target = models.FloatField(default=0)
    kpi_weight = models.FloatField(default=20)
    kpi_bsc_pillar = models.ForeignKey('BSCPillar', on_delete=models.RESTRICT, null=True, blank=True)
    kpi_units = models.CharField(max_length=5, null=True, blank=True)

    function = (
        ('maximize', 'maximize'),
        ('minimize', 'minimize'),
    )
    kpi_function = models.CharField(max_length=8, choices=function, blank=True, default='maximize')

    kpi_april_target = models.FloatField(null=True, blank=True)
    kpi_may_target = models.FloatField(null=True, blank=True)
    kpi_june_target = models.FloatField(null=True, blank=True)
    kpi_july_target = models.FloatField(null=True, blank=True)
    kpi_august_target = models.FloatField(null=True, blank=True)
    kpi_september_target = models.FloatField(null=True, blank=True)
    kpi_october_target = models.FloatField(null=True, blank=True)
    kpi_november_target = models.FloatField(null=True, blank=True)
    kpi_december_target = models.FloatField(null=True, blank=True)
    kpi_january_target = models.FloatField(null=True, blank=True)
    kpi_february_target = models.FloatField(null=True, blank=True)
    kpi_march_target = models.FloatField(null=True, blank=True)
    
    kpi_april_score = models.FloatField(null=True, blank=True)
    kpi_may_score = models.FloatField(null=True, blank=True)
    kpi_june_score = models.FloatField(null=True, blank=True)
    kpi_july_score = models.FloatField(null=True, blank=True)
    kpi_august_score = models.FloatField(null=True, blank=True)
    kpi_september_score = models.FloatField(null=True, blank=True)
    kpi_october_score = models.FloatField(null=True, blank=True)
    kpi_november_score = models.FloatField(null=True, blank=True)
    kpi_december_score = models.FloatField(null=True, blank=True)
    kpi_january_score = models.FloatField(null=True, blank=True)
    kpi_february_score = models.FloatField(null=True, blank=True)
    kpi_march_score = models.FloatField(null=True, blank=True)

    kpi_bsc_s_target = models.FloatField(null=True, blank=True)
    kpi_bsc_a_target = models.FloatField(null=True, blank=True)
    kpi_bsc_b_target = models.FloatField(null=True, blank=True)
    kpi_bsc_c_target = models.FloatField(null=True, blank=True)
    kpi_bsc_d_target = models.FloatField(null=True, blank=True)

    kpi_april_score_approve = models.BooleanField(default=False)
    kpi_may_score_approve = models.BooleanField(default=False)
    kpi_june_score_approve = models.BooleanField(default=False)
    kpi_july_score_approve = models.BooleanField(default=False)
    kpi_august_score_approve = models.BooleanField(default=False)
    kpi_september_score_approve = models.BooleanField(default=False)
    kpi_october_score_approve = models.BooleanField(default=False)
    kpi_november_score_approve = models.BooleanField(default=False)
    kpi_december_score_approve = models.BooleanField(default=False)
    kpi_january_score_approve = models.BooleanField(default=False)
    kpi_february_score_approve = models.BooleanField(default=False)
    kpi_march_score_approve = models.BooleanField(default=False)

    kpi_submit_date = models.DateTimeField(auto_now=False)

    status = (
        ('Submitted', 'Submitted'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Edit', 'Edit Mode'),
    )
    kpi_status = models.CharField(max_length=40, choices=status, blank=True, default='Submitted')

    type = (
        ('', ''),
        ('Addition', 'Addition'),
        ('Average', 'Average'),
        ('YTD', 'YTD'),
    )
    kpi_type = models.CharField(max_length=10, choices=type, blank=True, default='Average', )

    kpi_all_results_approve = models.BooleanField(default=False)

    def __str__(self):
        return self.kpi_title


class BSCPillar(models.Model):
    pillar_id = models.AutoField(primary_key=True)
    pillar_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    pillar_name = models.CharField(max_length=20)

    def __str__(self):
        return self.pillar_name


class ApprovalKPI(models.Model):
    approval_id = models.AutoField(primary_key=True)
    approval_kpi = models.ForeignKey('KPI', on_delete=models.RESTRICT)
    approval_action = models.CharField(choices=KPI.status, default=None, blank=True, null=True, max_length=9)
    approval_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)
    approval_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)

    def __str__(self):
        return self.approval_action


class ApprovalLevelsKPI(models.Model):
    approval_level_id = models.AutoField(primary_key=True)
    approval_level_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    approval_type = (
        ('Intermediate', 'Intermediate Approval'),
        ('Final', 'Final Approval'),

    )
    approval_level_type = models.CharField(choices=approval_type, default='Intermediate', max_length=12)
    approval_level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)


# Notifications =====================================================================================================
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    type = (
        ('Error', 'Error'),
        ('KPI', 'KPI'),
        ('CheckIn', 'CheckIn'),
        ('Assessment', 'Assessment'),
        ('Notification', 'Notification'),
    )

    notification_type = models.CharField(max_length=12, choices=type)
    notification_reference_key = models.CharField(max_length=30, null=True)
    notification_user_name = models.CharField(max_length=50, default="Staff")
    notification_email = models.CharField(max_length=50, null=True)
    notification_title = models.CharField(max_length=50)
    notification_message = models.TextField()
    notification_date = models.DateField(auto_now=True)
    status = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Read', 'Read'),
    )
    notification_status = models.CharField(max_length=10, choices=status, default=None)


class KPIType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    type_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)

    types = (
        ('Annual Target', 'Annual Target'),
        ('Monthly Target', 'Monthly Target'),
        ('BSC', 'BSC'),
        ('BSC1', 'BSC1'),
    )
    type_kpi = models.CharField(max_length=20, choices=types, default="Annual Target")


class Help(models.Model):
    help_id = models.AutoField(primary_key=True)
    help_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)

    status = (
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('Resolved', 'Closed')
    )

    category = (
        ('KPI', 'KPI'),
        ('Check-In', 'Check-In'),
        ('Assessment', 'Assessment'),
        ('Reports', 'Reports'),
        ('Results', 'Results'),
        ('Other', 'Other')
    )
    help_category = models.CharField(choices=category, max_length=20, default='KPI')
    help_log_date = models.DateTimeField(auto_now=False, null=True)
    help_last_edit = models.DateTimeField(auto_now=True, null=True)
    help_close_edit = models.DateTimeField(auto_now=True, null=True)
    help_status = models.CharField(choices=status, max_length=20)
    help_requested = models.TextField()

    def __str__(self):
        return "Help " + str(self.help_id)


class PillarsApplications(models.Model):
    application_id = models.AutoField(primary_key=True)
    application_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    application_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT, null=True, blank=True, related_name="pillar_application_level_category")
    application_grade = models.ForeignKey('StaffGrades', on_delete=models.RESTRICT, null=True, blank=True, related_name="pillar_application_staff_grade")
    application_pillar = models.ForeignKey('BSCPillar', on_delete=models.RESTRICT, related_name="pillar_application_select_pillar")
    application_minimum_kpis = models.IntegerField()
    application_maximum_kpis = models.IntegerField()


class KPIApprovals(models.Model):
    approval_id = models.AutoField(primary_key=True)
    approval_status = models.CharField(max_length=10, choices=KPI.status, default=None)
    approval_head = models.ForeignKey('Staff', on_delete=models.RESTRICT)
    approval_kpi = models.ForeignKey('KPI', on_delete=models.RESTRICT)
    approval_submit_edit_date = models.DateTimeField(auto_now=False, default=None, null=True)
    approval_date = models.DateTimeField(auto_now=False, null=True, blank=True)


class KPIApprovalStages(models.Model):
    stage_id = models.AutoField(primary_key=True)
    stage_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)
    stage_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    stages = (
        ('Initial', 'Initial'),
        ('Intermediate', 'Intermediate'),
        ('Final', 'Final'),
    )
    stage_approval = models.CharField(max_length=15, choices=stages)


class CDPCycle(models.Model):
    cycle_id = models.AutoField(primary_key=True)
    cycle_name = models.CharField(max_length=100, default=None)
    cycle_minimum_required_competency = models.IntegerField()
    cycle_maximum_required_competency = models.IntegerField()
    cycle_start = models.DateTimeField(auto_now=False)
    cycle_end = models.DateTimeField(auto_now=False)
    cycle_company = models.ForeignKey('Company', on_delete=models.RESTRICT)


class Competency(models.Model):
    competency_id = models.AutoField(primary_key=True)
    competency_name = models.CharField(max_length=100)
    competency_description = models.TextField(blank=True, null=True)
    competency_cycle = models.ForeignKey('CDPCycle', on_delete=models.RESTRICT)


class CompetencyAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT, null=True, blank=True)
    assignment_grade = models.ForeignKey('StaffGrades', on_delete=models.RESTRICT, null=True, blank=True)
    assignment_competency = models.ForeignKey('Competency', on_delete=models.RESTRICT)


class AppliedCompetency(models.Model):
    applied_id = models.AutoField(primary_key=True)
    applied_competency = models.ForeignKey('Competency', on_delete=models.RESTRICT)
    applied_staff = models.ForeignKey('Staff', on_delete=models.RESTRICT)