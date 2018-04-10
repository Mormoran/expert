from datetime import datetime
from django import forms
from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.forms import ModelForm

from crispy_forms.bootstrap import (
    AppendedText,
    FormActions,
    PrependedText
)
from crispy_forms.helper import FormHelper

from crispy_forms.layout import *

from . models import Run, RunParameter, RunProperty, RunValue, RunValueConfiguration
from impedans_expert.expert_upload.models import FileUploadModel, FileType
from impedans_expert.expert.models import Customer, Chamber, Recipe
from impedans_expert.users.models import User

class FileParseForm(forms.Form):
    # baseline_choices = [('yes', 'no'), ('yes', 'no')]
    file = ModelMultipleChoiceField(queryset=None, required=True, label="File: ",
                                    widget=forms.CheckboxSelectMultiple)
    # is_baseline = forms.ChoiceField(choices=baseline_choices, widget=forms.RadioSelect(), label="Baseline Runs: ")
    # description = forms.CharField(max_length=1024, required=True, label="Description: ")
    config = ModelChoiceField(queryset=None, required=True, label="Type: ")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(FileParseForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            file_query = FileUploadModel.objects.filter(customer=customer, parsed=False)
            config_query = FileType.objects.filter(customer=customer)
            self.fields['file'].queryset=file_query
            self.fields['config'].queryset=config_query
        except:
            user = None


class RunPropertiesForm(ModelForm):

    class Meta:
        model = RunProperty
        fields = ['property_name', 'property_value']

class RunValuesForm(ModelForm):

    class Meta:
        model = RunValue
        fields = ['run_parameter', 'value']


class RunsFilterForm(forms.Form):

    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber")
    recipe = ModelChoiceField(queryset=None,  required=False, label="Recipe")
    start = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="Start Time")
    end = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="End Time")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(RunsFilterForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            recipe_query = Recipe.objects.filter(customer=customer)
            self.fields['chamber'].queryset=chamber_query
            self.fields['recipe'].queryset=recipe_query

        except:
            user = None

    def clean_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']

        if end < start:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        End Time is earlier than Start Time")
        return end


class RunRecipeForm(forms.Form):
    recipe = forms.ModelChoiceField(queryset=None, required=True, label="Recipe")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(RunRecipeForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            recipe_query = Recipe.objects.filter(customer=customer)
            self.fields['recipe'].queryset=recipe_query

            self.helper = FormHelper()
            self.helper.form_id = 'run_recipe_form'
            self.helper.form_method = 'post'
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'controls-label'
            self.helper.field_class = 'controls-row'

            self.helper.layout = Layout(
                Div(
                    Div(Field('recipe'), css_class='controls-row'),)
            )

        except:
            user = None
