from django.urls import path
from .views import *

app_name = 'cfao_kenya'

urlpatterns = [
    path('', Dashboard.as_view(template_name='cfao_kenya/index.html'), name='Dashboard'),

    # kpi links
    path('KPI/', MyKPI.as_view(template_name='cfao_kenya/KPI/my_kpi/list.html'), name='My_KPI'),
    path('KPI/View/<uuid:pk>', MyKPIView.as_view(template_name='cfao_kenya/KPI/my_kpi/view.html'), name='My_KPI_View'),
    path('KPI/Create', MyKPICreate.as_view(template_name='cfao_kenya/KPI/my_kpi/create.html'), name='My_KPI_Create'),
    path('KPI/Edit/<uuid:pk>', MyKPIEdit.as_view(template_name='cfao_kenya/KPI/my_kpi/edit.html'), name='My_KPI_Edit'),
    path('KPI/Delete/<uuid:pk>', MyKPIDelete.as_view(template_name='cfao_kenya/KPI/my_kpi/delete.html'), name='My_KPI_Delete'),
    path('KPI/View/Results/<uuid:pk>', MyKPIResults.as_view(template_name='cfao_kenya/KPI/my_kpi/results.html'), name='My_KPI_Results'),
    path('KPI/Results', MyKPIResultsList.as_view(template_name='cfao_kenya/KPI/my_kpi/results_list.html'), name='My_KPI_Results_View'),

    # Category KPI links
    path('KPI/Category/<uuid:pk>', KPICategory.as_view(template_name='cfao_kenya/KPI/level_up_kpi/list_levels.html'), name='KPI_Category'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:pk>', KPICategoryLevel.as_view(template_name='cfao_kenya/KPI/level_up_kpi/list.html'), name='KPI_Category_Level'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:lev_id>/View/<uuid:pk>', KPICategoryLevelOne.as_view(template_name='cfao_kenya/KPI/level_up_kpi/view.html'), name='KPI_Category_Level_One'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:lev_id>/View/<uuid:pk>/Results', KPICategoryLevelOneResults.as_view(template_name='cfao_kenya/KPI/level_up_kpi/results.html'), name='KPI_Category_Level_One_Results'),
    path('KPI/Category/<uuid:pk>/Results', KPICategoryResults.as_view(template_name='cfao_kenya/KPI/level_up_kpi/results_list_levels.html'), name='KPI_Category_Results'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:lev_id>/Create', KPICategoryLevelNew.as_view(template_name='cfao_kenya/KPI/level_up_kpi/create.html'), name='KPI_Category_Level_New'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:lev_id>/Edit/<uuid:pk>', KPICategoryLevelEdit.as_view(template_name='cfao_kenya/KPI/level_up_kpi/edit.html'), name='KPI_Category_Level_One_Edit'),
    path('KPI/Category/<uuid:cat_id>/Level/<uuid:lev_id>/Delete/<uuid:pk>', KPICategoryLevelDelete.as_view(template_name='cfao_kenya/KPI/level_up_kpi/delete.html'), name='KPI_Category_Level_One_Delete'),


    # CheckIn Links
    path('CheckIn/', MyCheckIn.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/list.html'), name='My_CheckIn'),
    path('CheckIn/Create', MyCheckInCreate.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/create.html'), name='My_CheckIn_Create'),
    path('CheckIn/View/<uuid:pk>', MyCheckInView.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/view.html'), name='My_CheckIn_View'),
    path('CheckIn/Edit/<uuid:pk>', MyCheckInEdit.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/edit.html'), name='My_CheckIn_Edit'),
    path('CheckIn/Delete/<uuid:pk>', MyCheckInDelete.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/delete.html'), name='My_CheckIn_Delete'),

    path('Assessment/', AssessmentList.as_view(template_name='cfao_kenya/Assessment/list.html'), name='Assessment_List'),
    path('Assessment/View/<uuid:pk>', AssessmentView.as_view(template_name='cfao_kenya/Assessment/view.html'), name='Assessment_View'),
    path('Assessment/Vie,,w', MyCheckInCreate.as_view(template_name='cfao_kenya/Assessment/view'), name='My_CheckIn_Create'),
    path('CheckIn/View/<uuid:pk>', MyCheckInView.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/view.html'), name='My_CheckIn_View'),
    path('CheckIn/Edit/<uuid:pk>', MyCheckInEdit.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/edit.html'), name='My_CheckIn_Edit'),
    path('CheckIn/Delete/<uuid:pk>', MyCheckInDelete.as_view(template_name='cfao_kenya/CheckIn/my_CheckIn/delete.html'), name='My_CheckIn_Delete'),


    # No Active PMS
    path('PMS/', NoActivePMS.as_view(template_name='cfao_kenya/errors/no_active_pms.html'), name='No_Active_PMS'),

    # Admin links
    path('Admin/', AdminDashboard.as_view(template_name='cfao_kenya/Admin/pms/list.html'), name='Admin_Home'),
    path('Admin/PMS/Create', AdminDashboardPMSCreate.as_view(template_name='cfao_kenya/Admin/pms/create.html'), name='Admin_PMS_Create'),
    path('Admin/PMS/View/<uuid:pk>', AdminDashboardPMSView.as_view(template_name='cfao_kenya/Admin/pms/view.html'), name='Admin_PMS_View'),
    path('Admin/PMS/Edit/<uuid:pk>', AdminDashboardPMSEdit.as_view(template_name='cfao_kenya/Admin/pms/edit.html'), name='Admin_PMS_Edit'),
    path('Admin/PMS/Delete/<uuid:pk>', AdminDashboardPMSDelete.as_view(template_name='cfao_kenya/Admin/pms/delete.html'), name='Admin_PMS_Delete'),

    path('Admin/Users', AdminUser.as_view(template_name='cfao_kenya/Admin/user/list.html'), name='Admin_Users'),
    path('Admin/Users/Create', AdminUserCreate.as_view(template_name='cfao_kenya/Admin/user/create.html'), name='Admin_Users_Create'),
    path('Admin/Users/View/<int:pk>', AdminUserView.as_view(template_name='cfao_kenya/Admin/user/view.html'), name='Admin_Users_View'),
    path('Admin/Users/Edit/<int:pk>', AdminUserEdit.as_view(template_name='cfao_kenya/Admin/user/edit.html'), name='Admin_Users_Edit'),
    path('Admin/Users/Delete/<int:pk>', AdminUserDelete.as_view(template_name='cfao_kenya/Admin/user/delete.html'), name='Admin_Users_Delete'),
    path('Admin/Staff/Create/<int:pk>', AdminStaffCreate.as_view(template_name='cfao_kenya/Admin/staff/create.html'), name='Admin_Staff_Create'),
    path('Admin/Staff/Edit/<int:pk>', AdminStaffEdit.as_view(template_name='cfao_kenya/Admin/staff/edit.html'), name='Admin_Staff_Edit'),
    path('Admin/Staff/Delete/<int:pk>', AdminStaffDelete.as_view(template_name='cfao_kenya/Admin/staff/delete.html'), name='Admin_Staff_Delete'),

    path('Admin/Category', AdminCategory.as_view(template_name='cfao_kenya/Admin/category/list.html'), name='Admin_Category'),
    path('Admin/Category/Create', AdminCategoryCreate.as_view(template_name='cfao_kenya/Admin/category/create.html'), name='Admin_Category_Create'),
    path('Admin/Category/View/<uuid:pk>', AdminCategoryView.as_view(template_name='cfao_kenya/Admin/category/view.html'), name='Admin_Category_View'),
    path('Admin/Category/Edit/<uuid:pk>', AdminCategoryEdit.as_view(template_name='cfao_kenya/Admin/category/edit.html'), name='Admin_Category_Edit'),
    path('Admin/Category/Delete/<uuid:pk>', AdminCategoryDelete.as_view(template_name='cfao_kenya/Admin/category/delete.html'), name='Admin_Category_Delete'),

    path('Admin/Level', AdminLevel.as_view(template_name='cfao_kenya/Admin/level/list.html'), name='Admin_Level'),
    path('Admin/Level/Create', AdminLevelCreate.as_view(template_name='cfao_kenya/Admin/level/create.html'), name='Admin_Level_Create'),
    path('Admin/Level/View/<uuid:pk>', AdminLevelView.as_view(template_name='cfao_kenya/Admin/level/view.html'), name='Admin_Level_View'),
    path('Admin/Level/Edit/<uuid:pk>', AdminLevelEdit.as_view(template_name='cfao_kenya/Admin/level/edit.html'), name='Admin_Level_Edit'),
    path('Admin/Level/Delete/<uuid:pk>', AdminLevelDelete.as_view(template_name='cfao_kenya/Admin/level/delete.html'), name='Admin_Level_Delete'),

    path('Admin/Level/View/<uuid:pk>/Member/<int:mem_id>', level_member_status, name='Admin_Level_Member_Status'),
    path('Admin/Level/View/<uuid:pk>/Member/<int:mem_id>/Delete', level_member_remove, name='Admin_Level_Member_Delete'),
    path('Admin/Level/View/<uuid:pk>/Member/New', AdminLevelMemberCreate.as_view(template_name='cfao_kenya/Admin/levelmember/create.html'), name='Admin_Level_Member_Create'),


    path('Admin/<uuid:pk>/Assessment', AdminAssessment.as_view(template_name='cfao_kenya/Admin/assessment/list.html'), name='Admin_Assessment'),
    path('Admin/<uuid:pk>/Assessment/Create', AdminAssessmentCreate.as_view(template_name='cfao_kenya/Admin/assessment/create.html'), name='Admin_Assessment_Create'),
    path('Admin/<uuid:pk>/Assessment/View/<uuid:aid>', AdminAssessmentView.as_view(template_name='cfao_kenya/Admin/assessment/view.html'), name='Admin_Assessment_View'),
    path('Admin/<uuid:pk>/Assessment/Edit/<uuid:aid>', AdminAssessmentEdit.as_view(template_name='cfao_kenya/Admin/assessment/edit.html'), name='Admin_Assessment_Edit'),
    path('Admin/<uuid:pk>/Assessment/Delete/<uuid:aid>', AdminAssessmentDelete.as_view(template_name='cfao_kenya/Admin/assessment/delete.html'), name='Admin_Assessment_Delete'),
    path('Admin/<uuid:pk>/Assessment/<uuid:aid>/Question/New', AdminAssessmentQuestionCreate.as_view(template_name='cfao_kenya/Admin/question/create.html'), name='Admin_Assessment_Question_Create'),
    path('Admin/<uuid:pk>/Assessment/<uuid:aid>/Question/Edit/<uuid:qid>', AdminAssessmentQuestionEdit.as_view(template_name='cfao_kenya/Admin/question/edit.html'), name='Admin_Assessment_Question_Edit'),
    path('Admin/<uuid:pk>/Assessment/<uuid:aid>/Question/Delete/<uuid:qid>', AdminAssessmentQuestionDelete.as_view(template_name='cfao_kenya/Admin/question/delete.html'), name='Admin_Assessment_Question_Delete'),





]
