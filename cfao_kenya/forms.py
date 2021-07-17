from django import forms
from .models import *


class SubmitKpiForm(forms.ModelForm):
    class Meta:
        model = individual_Kpi
        fields = ['individual_kpi_title', 'individual_kpi_criteria', 'individual_kpi_function',
                  'individual_kpi_details', 'individual_kpi_target', 'individual_kpi_weight', 'individual_kpi_type',
                  'individual_kpi_pms', 'individual_kpi_user', 'individual_kpi_submit_date', 'individual_kpi_last_edit',
                  'individual_kpi_status']

    individual_kpi_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=True)
    individual_kpi_criteria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)
    individual_kpi_function = forms.ChoiceField(choices=individual_Kpi.function,
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    individual_kpi_type = forms.ChoiceField(choices=individual_Kpi.type,
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    individual_kpi_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px'}), required=True)
    individual_kpi_target = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    individual_kpi_weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super(SubmitKpiForm, self).clean()
        title = cleaned_data.get('individual_kpi_title')
        criteria = cleaned_data.get('individual_kpi_criteria')
        function = cleaned_data.get('individual_kpi_function')
        details = cleaned_data.get('individual_kpi_details')
        target = cleaned_data.get('individual_kpi_target')
        k_type = cleaned_data.get('individual_kpi_type')
        weight = cleaned_data.get('individual_kpi_weight')
        if not title or not criteria or not function or not details or not target or not weight or not k_type:
            raise forms.ValidationError('You have some blank fields')


class IndividualKpiUpdateForm(forms.ModelForm):
    class Meta:
        model = individual_Kpi
        fields = ['individual_kpi_title', 'individual_kpi_criteria', 'individual_kpi_function',
                  'individual_kpi_details', 'individual_kpi_target']

    individual_kpi_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=True)
    individual_kpi_criteria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)
    individual_kpi_function = forms.ChoiceField(choices=individual_Kpi.function,
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    individual_kpi_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px'}), required=True)
    individual_kpi_target = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super(IndividualKpiUpdateForm, self).clean()
        title = cleaned_data.get('individual_kpi_title')
        criteria = cleaned_data.get('individual_kpi_criteria')
        function = cleaned_data.get('individual_kpi_function')
        details = cleaned_data.get('individual_kpi_details')
        target = cleaned_data.get('individual_kpi_target')
        if not title and not criteria and not function and not details and not target:
            raise forms.ValidationError('You have some blank fields')


class ApproveKpiUpdateForm(forms.ModelForm):
    class Meta:
        model = individual_Kpi
        fields = ['individual_kpi_title', 'individual_kpi_criteria', 'individual_kpi_function',
                  'individual_kpi_details', 'individual_kpi_target']

    individual_kpi_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=True)
    individual_kpi_criteria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)
    individual_kpi_function = forms.ChoiceField(choices=individual_Kpi.function,
                                                widget=forms.Select(attrs={'class': 'form-control'}))
    individual_kpi_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px'}), required=True)
    individual_kpi_target = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super(IndividualKpiUpdateForm, self).clean()
        title = cleaned_data.get('individual_kpi_title')
        criteria = cleaned_data.get('individual_kpi_criteria')
        function = cleaned_data.get('individual_kpi_function')
        details = cleaned_data.get('individual_kpi_details')
        target = cleaned_data.get('individual_kpi_target')
        if not title and not criteria and not function and not details and not target:
            raise forms.ValidationError('You have some blank fields')


class IndividualKpiResultsForm(forms.ModelForm):
    class Meta:
        model = individual_Kpi
        fields = ['individual_kpi_january_score', 'individual_kpi_february_score', 'individual_kpi_march_score',
                  'individual_kpi_april_score', 'individual_kpi_may_score', 'individual_kpi_june_score',
                  'individual_kpi_july_score', 'individual_kpi_august_score', 'individual_kpi_september_score',
                  'individual_kpi_october_score', 'individual_kpi_november_score', 'individual_kpi_december_score', ]

    individual_kpi_january_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_february_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_march_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_april_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_may_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_june_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_july_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_august_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_september_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_october_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_november_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    individual_kpi_december_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)


# =============================================================================================================
#                                            Bu KPI
# =============================================================================================================


class SubmitBuKpiForm(forms.ModelForm):
    class Meta:
        model = bu_kpi
        fields = ['bu_kpi_bu', 'bu_kpi_title', 'bu_kpi_criteria', 'bu_kpi_function', 'bu_kpi_details',
                  'bu_kpi_target', 'bu_kpi_weight', 'bu_kpi_type', 'bu_kpi_pms', 'bu_kpi_user', 'bu_kpi_submit_date',
                  'bu_kpi_last_edit', 'bu_kpi_status']

    bu_kpi_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=True)
    bu_kpi_criteria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)
    bu_kpi_function = forms.ChoiceField(choices=bu_kpi.function, widget=forms.Select(attrs={'class': 'form-control'}))
    bu_kpi_type = forms.ChoiceField(choices=bu_kpi.type, widget=forms.Select(attrs={'class': 'form-control'}))
    bu_kpi_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px'}), required=True)
    bu_kpi_target = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    bu_kpi_weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super(SubmitBuKpiForm, self).clean()
        title = cleaned_data.get('bu_kpi_title')
        criteria = cleaned_data.get('bu_kpi_criteria')
        function = cleaned_data.get('bu_kpi_function')
        details = cleaned_data.get('bu_kpi_details')
        target = cleaned_data.get('bu_kpi_target')
        k_type = cleaned_data.get('bu_kpi_type')
        weight = cleaned_data.get('bu_kpi_weight')
        if not title or not criteria or not function or not details or not target or not weight or not k_type:
            raise forms.ValidationError('You have some blank fields')


class BuKpiResultsForm(forms.ModelForm):
    class Meta:
        model = bu_kpi
        fields = ['bu_kpi_january_score', 'bu_kpi_february_score', 'bu_kpi_march_score',
                  'bu_kpi_april_score', 'bu_kpi_may_score', 'bu_kpi_june_score',
                  'bu_kpi_july_score', 'bu_kpi_august_score', 'bu_kpi_september_score',
                  'bu_kpi_october_score', 'bu_kpi_november_score', 'bu_kpi_december_score', ]

    bu_kpi_january_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_february_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_march_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_april_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_may_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_june_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_july_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_august_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_september_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_october_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_november_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bu_kpi_december_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)


# =============================================================================================================
#                                            Company KPI
# =============================================================================================================

class SubmitCompanyKpiForm(forms.ModelForm):
    class Meta:
        model = company_kpi
        fields = ['company_kpi_title', 'company_kpi_criteria', 'company_kpi_function', 'company_kpi_details',
                  'company_kpi_target', 'company_kpi_weight', 'company_kpi_type', 'company_kpi_pms', 'company_kpi_user', 'company_kpi_submit_date',
                  'company_kpi_last_edit', 'company_kpi_status']

    company_kpi_title = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                           required=True)
    company_kpi_criteria = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)
    company_kpi_function = forms.ChoiceField(choices=company_kpi.function, widget=forms.Select(attrs={'class': 'form-control'}))
    company_kpi_type = forms.ChoiceField(choices=company_kpi.type, widget=forms.Select(attrs={'class': 'form-control'}))
    company_kpi_details = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 80px'}), required=True)
    company_kpi_target = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    company_kpi_weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super(SubmitCompanyKpiForm, self).clean()
        title = cleaned_data.get('company_kpi_title')
        criteria = cleaned_data.get('company_kpi_criteria')
        function = cleaned_data.get('company_kpi_function')
        details = cleaned_data.get('company_kpi_details')
        target = cleaned_data.get('company_kpi_target')
        k_type = cleaned_data.get('company_kpi_type')
        weight = cleaned_data.get('company_kpi_weight')
        if not title or not criteria or not function or not details or not target or not weight or not k_type:
            raise forms.ValidationError('You have some blank fields')


class CompanyKpiResultsForm(forms.ModelForm):
    class Meta:
        model = company_kpi
        fields = ['company_kpi_january_score', 'company_kpi_february_score', 'company_kpi_march_score',
                  'company_kpi_april_score', 'company_kpi_may_score', 'company_kpi_june_score',
                  'company_kpi_july_score', 'company_kpi_august_score', 'company_kpi_september_score',
                  'company_kpi_october_score', 'company_kpi_november_score', 'company_kpi_december_score', ]

    company_kpi_january_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_february_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_march_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_april_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_may_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_june_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_july_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_august_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_september_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_october_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_november_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    company_kpi_december_score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)


# =============================================================================================================
#                                            Check-in form
# =============================================================================================================


class SubmitCheckInForm(forms.ModelForm):
    class Meta:
        model = checkIn
        fields = ['checkIn_performance_area', 'checkIn_progress_discussed', 'checkIn_team_member_actions',
                  'checkIn_team_leader_support', 'checkIn_submit_date', 'checkIn_status', 'checkIn_month',
                  'checkIn_pms', 'checkIn_staff']

    checkIn_performance_area = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', 'id': 'pax'}),
                                               required=True)
    checkIn_progress_discussed = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', }), required=True)
    checkIn_team_member_actions = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', }), required=True)
    checkIn_team_leader_support = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', }), required=True)
    checkIn_month = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                              required=True)

    def clean(self):
        cleaned_data = super(SubmitCheckInForm, self).clean()
        pa = cleaned_data.get('checkIn_performance_area')
        pd = cleaned_data.get('checkIn_progress_discussed')
        tm = cleaned_data.get('checkIn_team_member_actions')
        tl = cleaned_data.get('checkIn_team_leader_support')
        cm = cleaned_data.get('checkIn_team_leader_support')
        if not pa and not pd and not tm and not tl and not cm:
            raise forms.ValidationError('You have some blank fields')


class ApproveCheckInForm(forms.ModelForm):
    class Meta:
        model = checkIn
        fields = ['checkIn_confirm_date', 'checkIn_status', 'checkIn_team_leader_comment', 'checkIn_team_leader']

    checkIn_team_leader_comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea', 'id': 'pax'}),
                                                  required=True)

# =============================================================================================================
#                                            Assessments
# =============================================================================================================


class AsssessmentSTlForm(forms.ModelForm):
    class Meta:
        model = done_staff_evaluates_tl
        fields = ['done_evaluation', 'done_staff', 'done_team_leader', 'score_q1', 'score_q2', 'score_q3', 'score_q4',
                  'score_q5', 'score_q6', 'score_q7', 'score_q1_comment', 'score_q2_comment', 'score_q3_comment',
                  'score_q4_comment', 'score_q5_comment', 'score_q6_comment', 'score_q7_comment', 'done_q1', 'done_q2',
                  'done_q3', 'done_q4', 'done_q5', 'done_q6', 'done_q7', ]

    score_q1 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q1', }),
                                 required=False)
    score_q2 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q2', }),
                                 required=False)
    score_q3 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q3', }),
                                 required=False)
    score_q4 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q4', }),
                                 required=False)
    score_q5 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q5', }),
                                 required=False)
    score_q6 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q6', }),
                                 required=False)
    score_q7 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q7', }),
                                 required=False)

    """def clean(self):
        cleaned_data = super(edit_Check_In_Form, self).clean()
        pa = cleaned_data.get('checkIn_performance_area')
        pd = cleaned_data.get('checkIn_progress_discussed')
        tm = cleaned_data.get('checkIn_team_member_actions')
        tl = cleaned_data.get('checkIn_team_leader_support')
        if not pa and not pd and not tm and not tl:
            raise forms.ValidationError('You have some blank fields')"""


class AssessmentTlSForm(forms.ModelForm):
    class Meta:
        model = done_tl_evaluates_staff
        fields = ['done_evaluation', 'done_staff', 'done_team_leader', 'score_q1', 'score_q2', 'score_q3', 'score_q4',
                  'score_q5', 'score_q6', 'score_q7', 'score_q1_comment', 'score_q2_comment', 'score_q3_comment',
                  'score_q4_comment', 'score_q5_comment', 'score_q6_comment', 'score_q7_comment', 'done_q1', 'done_q2',
                  'done_q3', 'done_q4', 'done_q5', 'done_q6', 'done_q7', ]

    score_q1 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q1', }),
                                 required=False)
    score_q2 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q2', }),
                                 required=False)
    score_q3 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q3', }),
                                 required=False)
    score_q4 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q4', }),
                                 required=False)
    score_q5 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q5', }),
                                 required=False)
    score_q6 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q6', }),
                                 required=False)
    score_q7 = forms.ChoiceField(choices=done_staff_evaluates_tl.results,
                                 widget=forms.RadioSelect(attrs={'class': 'form-check-input score_q7', }),
                                 required=False)

    """def clean(self):
        cleaned_data = super(edit_Check_In_Form, self).clean()
        pa = cleaned_data.get('checkIn_performance_area')
        pd = cleaned_data.get('checkIn_progress_discussed')
        tm = cleaned_data.get('checkIn_team_member_actions')
        tl = cleaned_data.get('checkIn_team_leader_support')
        if not pa and not pd and not tm and not tl:
            raise forms.ValidationError('You have some blank fields')"""


# =============================================================================================================
#                                            Admin
# =============================================================================================================


class PmsForm(forms.ModelForm):
    class Meta:
        model = pms
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class IndividualKpiForm(forms.ModelForm):
    class Meta:
        model = individual_Kpi
        fields = '__all__'


class BUKpiForm(forms.ModelForm):
    class Meta:
        model = bu_kpi
        fields = '__all__'


class CompanyKpiForm(forms.ModelForm):
    class Meta:
        model = company_kpi
        fields = '__all__'


class CheckInForm(forms.ModelForm):
    class Meta:
        model = checkIn
        fields = '__all__'


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = evaluation
        fields = '__all__'


class QuestionTlSForm(forms.ModelForm):
    class Meta:
        model = question_tl_evaluate_staff
        fields = '__all__'


class QuestionSTlForm(forms.ModelForm):
    class Meta:
        model = question_staff_evaluate_tl
        fields = '__all__'


class DoneStaffEvaluateTl(forms.ModelForm):
    class Meta:
        model = done_staff_evaluates_tl
        fields = '__all__'


class DoneTlEvaluateStaff(forms.ModelForm):
    class Meta:
        model = done_tl_evaluates_staff
        fields = '__all__'


class MatrixScore(forms.ModelForm):
    class Meta:
        model = score_matrix
        fields = '__all__'


class MatrixKpi(forms.ModelForm):
    class Meta:
        model = kpi_months
        fields = '__all__'

