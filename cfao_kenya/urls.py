from django.urls import path
from .views import *

app_name = 'cfao_kenya'

urlpatterns = [
    path('', Dashboard.as_view(template_name='cfao_kenya/index.html'), name='Dashboard'),

    # kpi links
    path('KPI/', MyKPI.as_view(template_name='cfao_kenya/KPI/list.html'), name='My_KPI'),
    path('KPI/View/<uuid:pk>', MyKPIView.as_view(template_name='cfao_kenya/KPI/view.html'), name='My_KPI_View'),
    path('KPI/Create', MyKPICreate.as_view(template_name='cfao_kenya/KPI/create.html'), name='My_KPI_Create'),
    path('KPI/Edit/<uuid:pk>', MyKPIEdit.as_view(template_name='cfao_kenya/KPI/edit.html'), name='My_KPI_Edit'),
    path('KPI/Delete/<uuid:pk>', MyKPIDelete.as_view(template_name='cfao_kenya/KPI/delete.html'), name='My_KPI_Delete'),
    path('KPI/View/Results/<uuid:pk>', MyKPIResults.as_view(template_name='cfao_kenya/KPI/results.html'), name='My_KPI_Results'),
    path('KPI/Results', MyKPIResultsList.as_view(template_name='cfao_kenya/KPI/results_list.html'), name='My_KPI_Results_View'),
]
