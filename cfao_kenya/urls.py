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
    path('KPI/Create', MyKPICreate.as_view(template_name='cfao_kenya/KPI/my_kpi/create.html'), name='My_KPI_Create'),
    path('KPI/Edit/<uuid:pk>', MyKPIEdit.as_view(template_name='cfao_kenya/KPI/my_kpi/edit.html'), name='My_KPI_Edit'),
    path('KPI/Delete/<uuid:pk>', MyKPIDelete.as_view(template_name='cfao_kenya/KPI/my_kpi/delete.html'), name='My_KPI_Delete'),
    path('KPI/View/Results/<uuid:pk>', MyKPIResults.as_view(template_name='cfao_kenya/KPI/my_kpi/results.html'), name='My_KPI_Results'),
    path('KPI/Results', MyKPIResultsList.as_view(template_name='cfao_kenya/KPI/my_kpi/results_list.html'), name='My_KPI_Results_View'),

]
