from django.urls import path
from .views import *

app_name = 'Site'

urlpatterns = [
    path('<int:companyId>', Dashboard.as_view(template_name='Site/index.html'), name='Dashboard'),
]
