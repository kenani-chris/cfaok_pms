from django.apps import apps
from django.contrib import admin
from .models import *
from .urls import app_name


excempt_list = ['Staff', 'PMS']

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


class PMSAdmin(admin.ModelAdmin):
    list_display = ('pms_name', 'pms_year_start_date', 'pms_year_end_date', 'pms_active',)


admin.site.register(Staff, StaffAdmin)
admin.site.register(PMS, PMSAdmin)
