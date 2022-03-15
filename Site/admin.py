from django.apps import apps
from django.contrib import admin
from .models import *
from .urls import app_name


excempt_list = ['Staff', 'PMS', 'LevelCategory', 'KPIType', 'CheckIn', 'Level', 'KPI']

for name, app in apps.app_configs.items():
    if name == app_name:
        models = app.get_models()
        for model in models:
            if model.__name__ not in excempt_list:
                admin.site.register(model)


class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_person', 'staff_pf_number', 'staff_grade', 'staff_active', 'staff_superuser',
                    'staff_visibility', 'staff_category', 'staff_company')
    list_filter = ('staff_active', 'staff_superuser', 'staff_visibility', 'staff_company')


class PMSAdmin(admin.ModelAdmin):
    list_display = ('pms_name', 'pms_year_start_date', 'pms_year_end_date', 'pms_active', 'pms_company')


class LevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_parent', 'category_kpi_view', 'category_company')


class KPITypeAdmin(admin.ModelAdmin):
    list_display = ('type_pms', 'type_category', 'type_kpi')


class CheckInAdmin(admin.ModelAdmin):
    list_display = ('check_in_Staff', 'check_in_month', 'check_in_submit_date', 'check_in_status')


class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_name', 'level_description', 'level_head', 'level_parent', 'level_category')


class KPIAdmin(admin.ModelAdmin):
    list_display = ('kpi_staff', 'kpi_title', 'kpi_function', 'kpi_type', 'kpi_pms', 'kpi_status')

    list_filter = ('kpi_staff', 'kpi_pms', 'kpi_status')


admin.site.register(Staff, StaffAdmin)
admin.site.register(PMS, PMSAdmin)
admin.site.register(LevelCategory, LevelCategoryAdmin)
admin.site.register(KPIType, KPITypeAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(KPI, KPIAdmin)