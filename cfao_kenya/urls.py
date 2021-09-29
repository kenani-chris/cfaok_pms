from django.urls import path, re_path

from cfaok_pms.views import Home
from . import views
from .views import *

app_name = 'cfao_kenya'

urlpatterns = [
    path('', Dashboard.as_view(template_name='cfao_kenya/index.html'), name='Dashboard'),

    # kpi links
    path('KPI/', MyKPI.as_view(template_name='cfao_kenya/KPI/index.html'), name='My_KPI'),
    path('KPI/Create', MyKPICreate.as_view(template_name='cfao_kenya/KPI/create.html'), name='My_KPI_Create')
]