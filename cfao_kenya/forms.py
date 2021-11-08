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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = LevelCategory
        fields = '__all__'


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = '__all__'


class LevelMemberForm(forms.ModelForm):
    class Meta:
        model = LevelMembers
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LevelMemberForm, self).__init__(*args, **kwargs)
        level_members = LevelMembers.objects.filter(level_member_active=True).values('level_member_user')
        self.fields['level_member_user'].queryset = User.objects.exclude(id__in=level_members)

