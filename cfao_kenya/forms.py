from django import forms
from django.contrib.auth.forms import UserCreationForm

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


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = '__all__'


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'is_superuser', 'is_active']


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = '__all__'
