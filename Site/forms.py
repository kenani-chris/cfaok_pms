from django import forms
from .models import KPI, CheckIn, Assessment, QuestionResponses, Help


class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = '__all__'


class KPIResultsForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['kpi_id', 'kpi_april_score', 'kpi_april_target', 'kpi_april_score_approve',
                  'kpi_may_score', 'kpi_may_target', 'kpi_may_score_approve',
                  'kpi_june_score', 'kpi_june_target', 'kpi_june_score_approve',
                  'kpi_july_score', 'kpi_july_target', 'kpi_july_score_approve',
                  'kpi_august_score', 'kpi_august_target', 'kpi_august_score_approve',
                  'kpi_september_score', 'kpi_september_target', 'kpi_september_score_approve',
                  'kpi_october_score', 'kpi_october_target', 'kpi_october_score_approve',
                  'kpi_november_score', 'kpi_november_target', 'kpi_november_score_approve',
                  'kpi_december_score', 'kpi_december_target', 'kpi_december_score_approve',
                  'kpi_january_score', 'kpi_january_target', 'kpi_january_score_approve',
                  'kpi_february_score', 'kpi_february_target', 'kpi_february_score_approve',
                  'kpi_march_score', 'kpi_march_target', 'kpi_march_score_approve'

                  ]


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = '__all__'


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'


class QuestionResponseForm(forms.ModelForm):
    class Meta:
        model = QuestionResponses
        fields = '__all__'


class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = '__all__'
