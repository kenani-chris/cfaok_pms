from django.contrib import admin
from .models import *

# Register your models here.
# Register your models here.


admin.site.register(pms)
admin.site.register(staff)
admin.site.register(department)
admin.site.register(branch)
admin.site.register(team)
admin.site.register(bu)
admin.site.register(checkIn)
admin.site.register(evaluation)
admin.site.register(done_tl_evaluates_staff)
admin.site.register(done_staff_evaluates_tl)
admin.site.register(question_tl_evaluate_staff)
admin.site.register(question_staff_evaluate_tl)
admin.site.register(responses_tl_evaluate_staff)
admin.site.register(responses_staff_evaluate_tl)
admin.site.register(bu_kpi)
admin.site.register(individual_Kpi)
admin.site.register(company_kpi)
admin.site.register(notification)
admin.site.register(score_matrix)