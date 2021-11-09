from django.db import models
from django.contrib.auth.models import User
import uuid
from colorfield.fields import ColorField


# Company Info
class CompanyProfile(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    company_logo = models.ImageField(upload_to='company')
    company_profile_active = models.BooleanField(default=False)
    company_color1 = ColorField(default='#00a8b4')
    company_color2 = ColorField(default='#d9d9d9')
    company_color3 = ColorField(default='#33393f')

    def __str__(self):
        return self.company_name


# Staff Account =======================================================================================================
class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_person = models.OneToOneField(User, on_delete=models.RESTRICT)
    staff_Pf_Number = models.CharField(max_length=10)
    staff_grade = models.ForeignKey('StaffGrades', on_delete=models.RESTRICT, null=True)
    staff_active = models.BooleanField(default=True)
    staff_superuser = models.BooleanField(default=False)
    staff_visibility = models.BooleanField(default=True)
    staff_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return self.staff_person.get_full_name()


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
    pms_last_edit = models.DateTimeField(auto_now=True)

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
    
    # KPI calculation
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


'''
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
'''


# Check In =============================================================================================================
class CheckIn(models.Model):
    
    class Meta:
        permissions = [
            ("Can_add_subordinate_CheckIn", "Can add every level down (subordinate) CheckIn"),
            ("Can_change_subordinate_CheckIn", "Can change every level down (subordinate) CheckIn"),
            ("Can_delete_subordinate_CheckIn", "Can delete every level down (subordinate) CheckIn"),
            ("Can_view_subordinate_CheckIn", "Can view every level down (subordinate) CheckIn"),
            ("Can_list_subordinate_CheckIn", "Can list every level down (subordinate) CheckIn"),
        ]
        
    checkIn_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    checkIn_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    checkIn_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    checkIn_submit_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    checkIn_approver = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True,
                                         related_name="cfao_kenya_Approver")
    checkIn_approval_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

    checkIn_performance_area = models.TextField()
    checkIn_progress_discussed = models.TextField()
    checkIn_team_member_actions = models.TextField()
    checkIn_team_leader_support = models.TextField()
    checkIn_team_leader_comment = models.TextField(null=True, blank=True)

    checkIn_months = (
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
    checkIn_month = models.CharField(max_length=15, default=None, choices=checkIn_months, null=True)
    checkIn_status = models.CharField(max_length=10, choices=status, blank=True, default='Pending',
                                      help_text='PMS Status')
    checkIn_last_edit = models.DateTimeField(auto_now=True)


# Assessment ===========================================================================================================
class Assessment(models.Model):
    assessment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique identifier evaluations")
    assessment_name = models.CharField(max_length=50, unique=True)
    assessment_details = models.TextField()
    assessment_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    assessment_start_date = models.DateField(auto_now=False, auto_now_add=False)
    assessment_end_date = models.DateField(auto_now=False, auto_now_add=False)
    assessment_use = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    assessment_min_score = models.FloatField(default=0)
    assessment_max_score = models.FloatField(default=10)
    assessment_scoring_use = models.CharField(max_length=3, default=None, null=True, choices=assessment_use)
    assessment_last_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.assessment_name


class Questions(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question_assessment = models.ForeignKey('Assessment', on_delete=models.RESTRICT)
    question = models.TextField()
    
    direction = (
        ('Top', 'Top'),
        ('Bottom', 'Bottom'),
    )
    question_direction = models.CharField(max_length=6, choices=direction)
    question_last_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class QuestionResponses(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    response_question = models.ForeignKey('Questions', on_delete=models.RESTRICT)
    response_user = models.ForeignKey(User, on_delete=models.RESTRICT,
                                      related_name="cfao_kenya_Response_user")
    response_evaluated = models.ForeignKey(User, on_delete=models.RESTRICT,
                                           related_name="cfao_kenya_Response_evaluated")
    response_comment = models.TextField(blank=True, null=True, default=None)
    response_submitted = models.FloatField(default=None)
    response_last_edit = models.DateTimeField(auto_now=True)
    

# Levels/Groups =======================================================================================================
class Level(models.Model):
    level_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    level_name = models.CharField(max_length=200, unique=True)
    level_description = models.TextField()
    level_parent = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True)
    level_head = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="cfao_kenya_Head_level")
    level_reliever = models.ForeignKey(User, on_delete=models.RESTRICT,
                                       related_name="cfao_kenya_Head_reliever", null=True, blank=True)
    level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT,
                                       related_name="cfao_kenya_level_category", default=None)

    def __str__(self):
        return self.level_name


# Levels/Groups =======================================================================================================
class LevelCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category_name = models.CharField(max_length=200, unique=True)
    category_description = models.TextField()
    category_parent = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    category_kpi_view = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name


# Levels/Groups =======================================================================================================
class LevelMembers(models.Model):
    level_member_id = models.AutoField(primary_key=True)
    level_member_level = models.ForeignKey('Level', on_delete=models.RESTRICT)
    level_member_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    level_member_active = models.BooleanField(default=True)


# KPIs ===============================================================================================================
class KPI(models.Model):

    class Meta:
        permissions = [
            ("add_subordinate_kpi", "Can add every level down (subordinate) kpi"),
            ("change_subordinate_kpi", "Can change every level down (subordinate) kpi"),
            ("delete_subordinate_kpi", "Can delete every level down (subordinate) kpi"),
            ("view_subordinate_kpi", "Can view every level down (subordinate) kpi"),
            ("list_subordinate_kpi", "Can list every level down (subordinate) kpi"),

            ("add_level_up_kpi", "Can add every level category up kpi"),
            ("change_level_up_kpi", "Can change every level category up kpi"),
            ("delete_level_up_kpi", "Can delete every level up kpi"),
            ("view_level_up_kpi", "Can view every level up kpi"),
            ("list_level_up_kpi", "Can list every level up kpi"),
        ]

    kpi_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    kpi_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    kpi_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    kpi_title = models.CharField(max_length=200)
    kpi_details = models.TextField(null=True, blank=True)
    kpi_criteria = models.TextField(null=True, blank=True)
    kpi_target = models.FloatField()
    kpi_weight = models.FloatField(default=20)
    kpi_units = models.CharField(max_length=5, null=True, blank=True)

    function = (
        ('maximize', 'maximize'),
        ('minimize', 'minimize'),
    )
    kpi_function = models.CharField(max_length=8, choices=function, blank=True, default='maximize')
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

    kpi_submit_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    kpi_last_edit = models.DateTimeField(auto_now=True)
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


class ApprovalKPI(models.Model):
    approval_id = models.AutoField(primary_key=True)
    approval_kpi = models.ForeignKey('KPI', on_delete=models.RESTRICT)
    approval_action = models.CharField(choices=KPI.status, default=None, blank=True, null=True, max_length=9)
    approval_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    approval_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)

    def __str__(self):
        return self.approval_action


class ApprovalLevelsKPI(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_category = models.ForeignKey('LevelCategory', on_delete=models.RESTRICT)
    level_pms = models.ForeignKey('PMS', on_delete=models.RESTRICT)
    approval_type = (
        ('Intermediate', 'Intermediate Approval'),
        ('Final', 'Final Approval'),

    )
    level_approval_type = models.CharField(choices=approval_type, default='Intermediate', max_length=12)

    def __str__(self):
        return self.level_category


class ActionsKPI(models.Model):
    action_id = models.AutoField(primary_key=True)
    action_kpi = models.ForeignKey('KPI', on_delete=models.RESTRICT)
    action_name = models.CharField(max_length=100)
    action_description = models.TextField()
    action_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    action_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.action_name


# Notifications =====================================================================================================
class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = (
        ('Error', 'Error'),
        ('KPI', 'KPI'),
        ('CheckIn', 'CheckIn'),
        ('Assessment', 'Assessment'),
        ('Notification', 'Notification'),
    )

    notification_type = models.CharField(max_length=12, choices=type)
    notification_sender = models.ForeignKey(User, on_delete=models.RESTRICT,
                                            related_name="cfao_kenya_Notification_Sender")
    notification_receiver = models.ForeignKey(User, on_delete=models.RESTRICT,
                                              related_name="cfao_kenya_Notification_Receiver")
    notification_title = models.CharField(max_length=15)
    notification_message = models.TextField()
    notification_date = models.DateField(auto_now=True)

    status = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Read', 'Read'),
    )
    notification_status = models.CharField(max_length=10, choices=status, default=None)


# logs
class Logs(models.Model):
    log_id = models.AutoField(primary_key=True)
    log_user = models.ForeignKey(User, on_delete=models.RESTRICT)
    log_date_time = models.DateTimeField(auto_now=True)
    log_category = models.CharField(max_length=10)
    log_description = models.TextField()
