from django.apps import apps
from django.contrib import admin
from .models import Staff, PMS, LevelCategory, KPIType, CheckIn, Level, KPI, LevelMembership, Assessment, Questions, \
    QuestionResponses, PasswordChange, SubmissionCheckin, SubmissionKPI, Matrix
from .urls import app_name


excempt_list = ['Staff', 'PMS', 'LevelCategory', 'KPIType', 'CheckIn', 'Level', 'KPI', 'LevelMembership', 'Assessment',
                'Questions', 'QuestionResponses', 'PasswordChange', 'SubmissionKPI', 'SubmissionCheckin', 'Matrix']

for name, app in apps.app_configs.items():
    if name == app_name:
        models = app.get_models()
        for model in models:
            if model.__name__ not in excempt_list:
                admin.site.register(model)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'staff_pf_number', 'staff_grade', 'staff_active', 'staff_superuser',
                    'staff_visibility', 'staff_category', 'staff_company')
    list_filter = ('staff_active', 'staff_superuser', 'staff_visibility', 'staff_company')
    search_fields = ('staff_person__get_full_name', 'staff_pf_number')


class PMSAdmin(admin.ModelAdmin):
    list_display = ('pms_name', 'pms_year_start_date', 'pms_year_end_date', 'pms_active', 'pms_company')


class LevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_parent', 'category_kpi_view', 'category_company')


class KPITypeAdmin(admin.ModelAdmin):
    list_display = ('type_pms', 'type_category', 'type_kpi')


class CheckInAdmin(admin.ModelAdmin):
    list_display = ('check_in_Staff', 'check_in_month', 'check_in_submit_date', 'check_in_status')
    list_filter = ('check_in_month',)
    search_fields = ('check_in_Staff__staff_person__first_name', 'check_in_Staff__staff_person__last_name',
                     'check_in_Staff__staff_pf_number')


class KPIAdmin(admin.ModelAdmin):
    list_display = ('kpi_staff', 'kpi_title', 'kpi_function', 'kpi_type', 'kpi_pms', 'kpi_status')

    list_filter = ('kpi_pms', 'kpi_status')
    search_fields = ('kpi_staff__staff_person__first_name', 'kpi_staff__staff_person__last_name',
                     'kpi_staff__staff_pf_number', 'kpi_title')
    

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('membership_staff', 'membership_level', 'membership_is_active')
    list_filter = ('membership_is_active',)
    search_fields = ('membership_staff__staff_person__first_name', 'membership_staff__staff_person__last_name',
                     'membership_staff__staff_pf_number')


class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_name', 'level_parent', 'level_head', 'level_category')
    list_filter = ('level_category',)
    search_fields = ('level_name', 'level_head__staff_person__first_name', 'level_head__staff_person__last_name',
                     'level_head__staff_pf_number')


class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment_name', 'assessment_pms', 'assessment_start_date',
                    'assessment_end_date', 'assessment_min_score', 'assessment_max_score', 'assessment_scoring_use')
    list_filter = ('assessment_pms__pms_company__company_name', 'assessment_pms', 'assessment_scoring_use')


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_assessment', 'question_direction',)
    list_filter = ('question_assessment__assessment_pms__pms_company', 'question_direction')
    search_fields = ('question',)


class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('response_staff', 'response_evaluated', 'response_question', 'response_submitted',
                    'response_comment', 'response_submitted_date', )
    list_filter = ('response_question__question_direction', 'response_question__question_assessment')
    search_fields = ('response_staff__staff_person__first_name', 'response_staff__staff_person__last_name',
                     'response_staff__staff_pf_number', 'response_evaluated__staff_person__first_name',
                     'response_evaluated__staff_person__last_name', 'response_evaluated__staff_pf_number')


class PasswordChangeAdmin(admin.ModelAdmin):
    list_display = ('change_user', 'change_last_date')
    ordering = ('-change_last_date',)
    search_fields = ('change_user__first_name', 'change_user__last_name', 'change_user__email')


class SubmissionKPIAdmin(admin.ModelAdmin):
    list_display = ('submission_pms', 'submission_level_category', 'submission_start_date', 'submission_end_date',
                    'submission_minimum_number', 'submission_maximum_number',
                    'submission_april_results_calculation', 'submission_may_results_calculation',
                    'submission_june_results_calculation', 'submission_july_results_calculation',
                    'submission_august_results_calculation', 'submission_september_results_calculation',
                    'submission_october_results_calculation', 'submission_november_results_calculation',
                    'submission_december_results_calculation', 'submission_january_results_calculation',
                    'submission_february_results_calculation', 'submission_march_results_calculation',)
    list_filter = ('submission_pms', 'submission_level_category',)
    search_fields = ('submission_level_category',)


class SubmissionCheckinAdmin(admin.ModelAdmin):
    list_display = ('submission_pms', 'submission_level_category',
                    'submission_one_results', 'submission_two_results', 'submission_three_results',
                    'submission_four_results', 'submission_five_results', 'submission_six_results',
                    'submission_seven_results', 'submission_eight_results', 'submission_nine_results',
                    'submission_ten_results', 'submission_eleven_results', 'submission_twelve_results',)
    list_filter = ('submission_pms',  'submission_level_category',)
    search_fields = ('submission_level_category',)


class MatrixAdmin(admin.ModelAdmin):
    list_display = ('matrix_pms', 'matrix_category', 'matrix_grade', 'matrix_kpi_weight', 'matrix_bu_weight',
                    'matrix_company_weight', 'matrix_assessment_weight', 'matrix_checkin_weight')
    list_filter = ('matrix_pms',)


admin.site.register(Staff, StaffAdmin)
admin.site.register(PMS, PMSAdmin)
admin.site.register(LevelCategory, LevelCategoryAdmin)
admin.site.register(KPIType, KPITypeAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(KPI, KPIAdmin)
admin.site.register(LevelMembership, MembershipAdmin)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(QuestionResponses, ResponsesAdmin)
admin.site.register(PasswordChange, PasswordChangeAdmin)
admin.site.register(SubmissionCheckin, SubmissionCheckinAdmin)
admin.site.register(SubmissionKPI, SubmissionKPIAdmin)
admin.site.register(Matrix, MatrixAdmin)
