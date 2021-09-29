from django import forms
from .models import *


class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = '__all__'
