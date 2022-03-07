from django.urls import path
from .views import *

app_name = 'Site'

urlpatterns = [
    path('<int:company_id>', Dashboard.as_view(template_name='Site/index.html'), name='Dashboard'),
    path('<int:company_id>/Error/<str:error_code>', ErrorPage.as_view(template_name='Site/errors/index.html'),
         name='Error'),

    path('<int:company_id>/KPI/', MyKPI.as_view(template_name='Site/KPI/my_kpi/list.html'), name='My_KPI'),
    path('<int:company_id>/KPI/View/<int:pk>', MyKPIView.as_view(template_name='Site/KPI/my_kpi/view.html'),
         name='My_KPI_View'),
    path('<int:company_id>/KPI/Create', MyKPICreate.as_view(template_name='Site/KPI/my_kpi/create.html'),
         name='My_KPI_Create'),
    path('<int:company_id>/KPI/Edit/<int:pk>', MyKPIEdit.as_view(template_name='Site/KPI/my_kpi/edit.html'),
         name='My_KPI_Edit'),
    path('<int:company_id>/KPI/Delete/<int:pk>', MyKPIDelete.as_view(template_name='Site/KPI/my_kpi/delete.html'),
         name='My_KPI_Delete'),
    path('<int:company_id>/KPI/View/Results/<int:pk>',
         MyKPIResults.as_view(template_name='Site/KPI/my_kpi/results.html'), name='My_KPI_Results'),
    path('<int:company_id>/KPI/Results', MyKPIResultsList.as_view(template_name='Site/KPI/my_kpi/results_list.html'),
         name='My_KPI_Results_View'),

    # Level Down KPI links
    path('<int:company_id>/KPI/LevelDown',
         KPILevelDown.as_view(template_name='Site/KPI/level_down_kpi/list_levels.html'), name='KPI_LevelDown'),
    path('<int:company_id>/KPI/LevelDown/<int:pk>',
         KPILevelDownDetail.as_view(template_name='Site/KPI/level_down_kpi/list.html'), name='KPI_LevelDownDetail'),
    path('<int:company_id>/KPI/LevelDown/<int:lev_id>/Staff/<int:pk>',
         KPILevelDownDetailStaff.as_view(template_name='Site/KPI/level_down_kpi/staff.html'),
         name='KPI_LevelDownDetailStaff'),
    path('<int:company_id>/KPI/LevelDown/<int:lev_id>/Staff/<int:staff_id>/StaffResults/<int:pk>',
         staff_kpi_results, name='Staff_KPI_Results'),

    # Category UP KPI links
    path('<int:company_id>/KPI/CategoryUP/<int:pk>',
         KPICategory.as_view(template_name='Site/KPI/category_up_kpi/list_levels.html'), name='KPI_Category'),
    path('<int:company_id>/KPI/Category/<int:cat_id>/Level/<int:pk>',
         KPICategoryLevel.as_view(template_name='Site/KPI/category_up_kpi/list.html'), name='KPI_Category_Level'),

    # Check-Ins
    path('<int:company_id>/CheckIn/', MyCheckIn.as_view(template_name='Site/CheckIn/my_CheckIn/list.html'),
         name='My_CheckIn'),
    path('<int:company_id>/CheckIn/Create',
         MyCheckInCreate.as_view(template_name='Site/CheckIn/my_CheckIn/create.html'), name='My_CheckIn_Create'),
    path('<int:company_id>/CheckIn/View/<int:pk>',
         MyCheckInView.as_view(template_name='Site/CheckIn/my_CheckIn/view.html'), name='My_CheckIn_View'),
    path('<int:company_id>/CheckIn/Edit/<int:pk>',
         MyCheckInEdit.as_view(template_name='Site/CheckIn/my_CheckIn/edit.html'), name='My_CheckIn_Edit'),
    path('<int:company_id>/CheckIn/Delete/<int:pk>',
         MyCheckInDelete.as_view(template_name='Site/CheckIn/my_CheckIn/delete.html'), name='My_CheckIn_Delete'),
    path('<int:company_id>/KPI/LevelDown/<int:lev_id>/<int:type_id>/Staff/<int:staff_id>/StaffResults/<int:pk>',
         staff_check_in_approve, name='Staff_Check_in_Results'),

    # Level Down Check-In links
    path('<int:company_id>/Check-In/LevelDown',
         CheckInLevelDown.as_view(template_name='Site/CheckIn/level_down_check_in/list_levels.html'),
         name='Check_in_LevelDown'),
    path('<int:company_id>/Check-In/LevelDown/<int:pk>/<int:type_id>',
         CheckInLevelDownDetail.as_view(template_name='Site/CheckIn/level_down_check_in/list.html'),
         name='Check_in_LevelDownDetail'),
    path('<int:company_id>/Check-In/LevelDown/<int:lev_id>/<int:type_id>/Staff/<int:pk>',
         CheckInLevelDownDetailStaff.as_view(template_name='Site/CheckIn/level_down_check_in/staff.html'),
         name='Check_in_LevelDownDetailStaff'),
    path('<int:company_id>/Check-In/LevelDown/<int:lev_id>/Staff/<int:staff_id>/StaffResults/<int:pk>',
         staff_kpi_results, name='Check_in_Detail'),

    # Assessment
    path('<int:company_id>/Assessment/', AssessmentList.as_view(template_name='Site/Assessment/list.html'),
         name='Assessment_List'),
    path('<int:company_id>/Assessment/View/<int:pk>', AssessmentView.as_view(template_name='Site/Assessment/view.html'),
         name='Assessment_View'),
    path('<int:company_id>/Assessment/View/<int:pk>/Member/<int:uid>/<slug:dir>',
         AssessmentViewMember.as_view(template_name='Site/Assessment/view_staff.html'),
         name='Assessment_View_Member'),
    path('<int:company_id>/Assessment/View/<int:aid>/Member/<int:staff_id>/<slug:dir>/Question/<int:qid>/Create',
         staff_create_question_response, name='Assessment_Create_Response'),
    path('<int:company_id>/Assessment/View/<int:aid>/Member/<int:staff_id>/<slug:dir>/Question/<int:rid>/Edit',
         staff_edit_question_response, name='Assessment_Edit_Response'),
    path('<int:company_id>/Assessment/View/<int:pk>/Member/<int:uid>/<slug:dir>/Question/<int:qid>',
         AssessmentViewMemberResponseCreate.as_view(template_name='Site/Assessment/create.html'),
         name='Assessment_View_Member_Response'),
    path('<int:company_id>/Assessment/View/<int:pk>/Member/<int:uid>/<slug:dir>/Response/<int:qrid>/Edit',
         AssessmentViewMemberResponseEdit.as_view(template_name='Site/Assessment/edit.html'),
         name='Assessment_View_Member_Response_Edit'),

    path('<int:company_id>/Assessment/View/<int:pk>/My/<slug:dir>',
         AssessmentViewMy.as_view(template_name='Site/Assessment/view_my.html'), name='Assessment_View_My'),

    # Profile
    path('<int:company_id>/Profile', Profile.as_view(template_name='Site/Profile/list.html'), name='Profile'),

    # Help
    path('<int:company_id>/Help', HelpList.as_view(template_name='Site/Help/list.html'), name='Help_List'),
    path('<int:company_id>/Help/Create', HelpCreate.as_view(template_name='Site/Help/create.html'), name='Help_Create'),
    path('<int:company_id>/Help/Edit/<int:pk>', HelpEdit.as_view(template_name='Site/Help/edit.html'),
         name='Help_Edit'),

    path('<int:company_id>/Report', Report.as_view(template_name='Site/Reports/list.html'), name='Report'),
    path('<int:company_id>/Report/KPIResult', ReportKPIResults.as_view(template_name='Site/Reports/kpi_results.html'),
         name='Report_KPI_Results'),
    path('<int:company_id>/Report/AssessmentResult', ReportAssessments.as_view(
        template_name='Site/Reports/assessment.html'), name='Report_Assessment_Results'),
    path('<int:company_id>/Report/AssessmentResult/<int:pk>', ReportAssessmentsDetails.as_view(
        template_name='Site/Reports/assessment_details.html'), name='Report_Assessment_Results_Detail'),
    path('<int:company_id>/Report/Check-In', ReportCheckIn.as_view(template_name='Site/Reports/checkin.html'),
         name='Report_Check-In'),
    path('<int:company_id>/Report/KPI-Submission', ReportKPISubmissions.as_view(
        template_name='Site/Reports/kpi_submission.html'), name='Report_KPI_Submission'),
    path('<int:company_id>/Report/Check-In', ReportKPIResults.as_view(template_name='Site/Reports/kpi_results.html'),
         name='Report_KPI_Results'),path('<int:company_id>/Report/KPIResult', ReportKPIResults.as_view(
        template_name='Site/Reports/kpi_results.html'), name='Report_KPI_Results'),


    path('<int:company_id>/Communication', Communication.as_view(template_name='Site/Communication/message.html'),
         name='Communication'),
    path('<int:company_id>/Communicate', communicate, name='Communicate'),
]
