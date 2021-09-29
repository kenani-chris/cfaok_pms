from django.apps import apps
from django.contrib import admin
from .models import *
from .urls import app_name


excempt_list = ['Staff']

for name, app in apps.app_configs.items():
    if name == app_name:
        models = app.get_models()
        for model in models:
            if model.__name__ not in excempt_list:
                admin.site.register(model)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_person', 'staff_Pf_Number', 'staff_grade', 'staff_active', 'staff_superuser',
                    'staff_visibility')
    list_filter = ('staff_active', 'staff_superuser', 'staff_visibility')


admin.site.register(Staff, StaffAdmin)
