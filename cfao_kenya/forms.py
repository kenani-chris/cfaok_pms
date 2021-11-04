from django import forms
from .models import *


class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = '__all__'


class PMSForm(forms.ModelForm):
    class Meta:
        model = PMS
        fields = '__all__'


class CheckInForm(forms.ModelForm):
    class Meta:
        model = CheckIn
        fields = '__all__'
