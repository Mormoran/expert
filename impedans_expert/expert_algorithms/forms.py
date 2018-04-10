import time

from datetime import (
    datetime,
    timezone,
    timedelta
)

from django import forms

from django.forms import (
    IntegerField,
    ModelChoiceField,
    ModelMultipleChoiceField,
    DateTimeField,
    ChoiceField
)

from django.forms import ModelForm

from django.contrib.admin import widgets

from crispy_forms.bootstrap import (
    AppendedText,
    FormActions,
    PrependedText
)
from crispy_forms.helper import FormHelper

from crispy_forms.layout import *

# from bootstrap4_datetime.widgets import DateTimePicker

from impedans_expert.expert_algorithms.models import (
    Algorithm,
    AlgorithmRun,
)

from impedans_expert.expert.models import (
    Customer,
    Chamber,
    Parameter,
    Recipe,
    Step
)

from impedans_expert.users.models import User

class AlgorithmForm(forms.Form):
    mode_choices = [('runs', 'Runs'), ('time', 'Time')]
    offset_choices = [('start', 'Start'), ('end', 'End')]
    # time_now = time_now.replace(tzinfo=pytz.utc)
    algorithm = ModelChoiceField(queryset=None, required=True, label="Algorithm: ")
    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber: ")
    parameter = ModelMultipleChoiceField(queryset=None, required=True, label="Parameter Selection", widget=forms.CheckboxSelectMultiple)
    start = forms.SplitDateTimeField(initial=datetime.now(), required=True, label = "Start Time: ")
    end = forms.SplitDateTimeField(initial=datetime.now(), required=True, label = "End Time: ")
    skip_start = forms.IntegerField(initial=0, required=True, max_value=200, min_value=0,
                                  label="Seconds to Skip at Start: ")
    skip_end = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                label="Seconds to Skip at End: ")

    offset_type = ChoiceField(choices=offset_choices, widget=forms.RadioSelect(), label = "Offset From: ")

    mode = ChoiceField(choices=mode_choices, widget=forms.RadioSelect(), label = "Mode: ")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(AlgorithmForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            parameter_query = Parameter.objects.all()
            algorithm_query = Algorithm.objects.all()
            self.fields['algorithm'].queryset=algorithm_query
            self.fields['chamber'].queryset=chamber_query
            self.fields['parameter'].queryset=parameter_query

            # self.fields['start'].widget = widgets.AdminSplitDateTime()
            # self.fields['end'].widget = widgets.AdminSplitDateTime()

            self.helper = FormHelper()
            self.helper.form_id = 'chamber-form'
            self.helper.form_method = 'post'
            # self.helper.add_input(Submit('submit', 'Submit'))
            self.helper.form_class = 'form-horizontal'
            # self.helper.label_class = 'col-lg-4'
            # self.helper.field_class = 'col-lg-8'
            # self.helper.form_class = 'form-inline'
            # helper.field_template = 'bootstrap4/layout/inline_field.html'
            self.helper.layout = Layout(
                Div(
                    Div(
                        Div(
                            'algorithm', 
                            css_class='col-md-6'),
                        Div(
                            'chamber', 
                            css_class='col-md-6'), 
                        css_class='row'), 
                    css_class='container'),
                    Div('parameter',
                        css_class='col-md-12'),
                    HTML("""<input type="checkbox" onClick="toggle(this)" /> Toggle All<br/>"""),
                Div(
                    Div(
                        Div('start', css_class='col-md-3'),
                        Div('skip_start', css_class='col-md-3'),
                        Div('end', css_class='col-md-3'),
                        Div('skip_end', css_class='col-md-3')
                    , css_class='row'), css_class='container timers'),
                Div('offset_type', css_class='col-md-6 mx-auto'),
                Div('mode', css_class='col-md-6 mx-auto'),
                Div(Submit('save', 'Save'), css_class='col-md-12 offset-md-6'),
            )


        except:
            user = None

    def clean_parameter(self):
        parameter = self.cleaned_data['parameter']
        if(len(parameter) == 0):
            print("ERROR RAISED: ")
            raise forms.ValidationError("No Parameters Selected")
        else:
            pass

        return parameter

    def clean_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']
        if end < start:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        End Time is earlier than Start Time")
        return end

    def clean_skip_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']
        skip_start = self.cleaned_data['skip_start']
        skip_end = self.cleaned_data['skip_end']

        end_of_set = end - timedelta(seconds=skip_end)
        start_of_set = start - timedelta(seconds=skip_start)
        if end_of_set < start_of_set:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        (End time - Seconds to Skip at End)  is earlier than \
                                        (Start time + Seconds to Skip at Start)")
        return skip_end


class RecipeForm(ModelForm):

    name = forms.CharField(max_length=255, required=True, label="Recipe Name: ")

    class Meta:
        model = Recipe
        fields = ['name']

class TrainingForm(forms.Form):

    recipe = ModelChoiceField(queryset=None, required=True, label="Recipe: ")

    step = forms.IntegerField(min_value = 1, label = "Step: ")
    step_start = forms.SplitDateTimeField(initial=datetime.now(), required=True, label = "Step Start Time: ")
    step_end = forms.SplitDateTimeField(initial=datetime.now(), required=True, label = "Step End Time: ")

    algorithm = ModelChoiceField(queryset=None, required=True, label="Algorithm: ")
    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber: ")
    parameter = ModelMultipleChoiceField(queryset=None, required=True, label="Parameter Selection",
                                         widget=forms.CheckboxSelectMultiple)
    skip_start = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                  label="Seconds to Skip at Start: ")

    skip_end = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                label="Seconds to Skip at End: ")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TrainingForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            recipe_query = Recipe.objects.all()
            parameter_query = Parameter.objects.all()
            algorithm_query = Algorithm.objects.all()
            self.fields['algorithm'].queryset=algorithm_query
            self.fields['chamber'].queryset=chamber_query
            self.fields['recipe'].queryset=recipe_query
            self.fields['parameter'].queryset=parameter_query
            print("success_____________")

            # self.fields['start'].widget = widgets.AdminSplitDateTime()
            # self.fields['end'].widget = widgets.AdminSplitDateTime()

            self.helper = FormHelper()
            self.helper.form_id = 'chamber-form'
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Submit'))
            self.helper.form_class = 'form-horizontal'
            # self.helper.form_class = 'form-inline'
            # self.helper.field_template = 'bootstrap4/layout/inline_field.html'
            # self.helper.label_class = 'col-sm-4'
            # self.helper.field_class = 'col-sm-8'
            self.helper.layout = Layout(
                Div(
                    Div(
                        Div('recipe', 'step_start', css_class='col-md-6'),
                        Div('step', 'step_end', css_class='col-md-6'), css_class='row'
                    ), css_class='container'),
                Div(
                    Div(
                        Div('skip_start', css_class='col-md-6'),
                        Div('skip_end', css_class='col-md-6'), css_class='row'
                    ), css_class='container'),
                Div(
                    Div(
                        Div('algorithm', css_class='col-md-6'),
                        Div('chamber', css_class='col-md-6'), css_class='row'
                    ), css_class='container'),
                Div(
                    Div('parameter', css_class='col-md-12'),
                    HTML("""<input type="checkbox" onClick="toggle(this)" /> Toggle All<br/>"""),
                ),
            )

        except:
            user = None

    def clean_parameter(self):
        parameter = self.cleaned_data['parameter']
        if(len(parameter) == 0):
            print("ERROR RAISED: ")
            raise forms.ValidationError("No Parameters Selected")
        else:
            pass

        return parameter

    def clean_step_end(self):
        end = self.cleaned_data['step_end']
        start = self.cleaned_data['step_start']
        if end < start:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        End Time is earlier than Start Time")
        return end

    def clean_skip_end(self):
        end = self.cleaned_data['step_end']
        start = self.cleaned_data['step_start']
        skip_start = self.cleaned_data['skip_start']
        skip_end = self.cleaned_data['skip_end']

        end_of_set = end - timedelta(seconds=skip_end)
        start_of_set = start - timedelta(seconds=skip_start)
        if end_of_set < start_of_set:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        (End time - Seconds to Skip at End)  is earlier than \
                                        (Start time + Seconds to Skip at Start)")
        return skip_end



class ResultsForm(forms.Form):

    mode_choices = [('runs', 'runs'), ('time', 'time')]
    algorithm = ModelChoiceField(queryset=None, required=True, label="Algorithm: ")
    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber: ")
    parameter = ModelChoiceField(queryset=None, required=True, label="Parameter: ")
    mode = ChoiceField(choices=mode_choices, widget=forms.RadioSelect(), label = "Mode")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ResultsForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            parameter_query = Parameter.objects.all()
            algorithm_query = Algorithm.objects.all()
            self.fields['algorithm'].queryset=algorithm_query
            self.fields['chamber'].queryset=chamber_query
            self.fields['parameter'].queryset=parameter_query
        except:
            user = None


class RunResultsForm(forms.Form):

    algorithm_run = ModelChoiceField(queryset=None, required=True, label="Algorithm Run: ")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(RunResultsForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            algorithm_run_query = AlgorithmRun.objects.filter(customer=customer)
            self.fields['algorithm_run'].queryset=algorithm_run_query
        except:
            user = None


class ZScoreForm(forms.Form):

    # mode_choices = [('runs', 'runs'), ('time', 'time')]
    # time_now = time_now.replace(tzinfo=pytz.utc)
    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber")
    parameter = ModelMultipleChoiceField(queryset=None, required=True, label="Parameter Selection",
                                         widget=forms.CheckboxSelectMultiple)
    start = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="Start Time")
    end = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="End Time")
    skip_start = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                  label="Seconds to Skip at Start")
    skip_end = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                label="Seconds to Skip at End")

    window_size = forms.IntegerField(initial=5, required=True, max_value=100, min_value=2)
    z_score_limit = forms.IntegerField(initial=6, required=True, max_value=100, min_value=1)
    # mode = ChoiceField(choices=mode_choices, widget=forms.RadioSelect(), label="Mode")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ZScoreForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            parameter_query = Parameter.objects.all()
            # algorithm_query = Algorithm.objects.all()
            # self.fields['algorithm'].queryset=algorithm_query
            self.fields['chamber'].queryset=chamber_query
            
            self.fields['parameter'].queryset=parameter_query

        except:
            user = None

    def clean_parameter(self):
        parameter = self.cleaned_data['parameter']
        for param in parameter:
            if "F1 (Mhz)" in param.parameter_name:
                invalid_entry = param.parameter_name + " is an invalid parameter selection"
                raise forms.ValidationError(invalid_entry)
            elif "Harmonic Phase" in param.parameter_name:
                invalid_entry = param.parameter_name + " is an invalid parameter selection"
                raise forms.ValidationError(invalid_entry)
            else:
                pass
        return parameter

    def clean_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']

        if end < start:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        End Time is earlier than Start Time")
        return end

    def clean_skip_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']
        skip_start = self.cleaned_data['skip_start']
        skip_end = self.cleaned_data['skip_end']

        end_of_set = end - timedelta(seconds=skip_end)
        start_of_set = start - timedelta(seconds=skip_start)
        if end_of_set < start_of_set:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        (End time - Seconds to Skip at End)  is earlier than \
                                        (Start time + Seconds to Skip at Start)")
        return skip_end


class TrainedZScoreForm(forms.Form):

    # mode_choices = [('runs', 'runs'), ('time', 'time')]
    # time_now = time_now.replace(tzinfo=pytz.utc)
    algorithm = ModelChoiceField(queryset=None, required=True, label="Algorithm: ")
    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber")
    step = ModelChoiceField(queryset=None, required=True, label="Step")
    parameter = ModelMultipleChoiceField(queryset=None, required=True, label="Parameter Selection",
                                         widget=forms.CheckboxSelectMultiple)
    start = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="Start Time")
    end = forms.SplitDateTimeField(initial=datetime.now(), required=True, label="End Time")
    skip_start = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                  label="Seconds to Skip at Start")
    skip_end = forms.FloatField(initial=0, required=True, max_value=200, min_value=0,
                                label="Seconds to Skip at End")

    window_size = forms.IntegerField(initial=5, required=True, max_value=100, min_value=2)
    z_score_limit = forms.IntegerField(initial=6, required=True, max_value=100, min_value=1)
    # mode = ChoiceField(choices=mode_choices, widget=forms.RadioSelect(), label="Mode")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TrainedZScoreForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            algorithm_query = Algorithm.objects.all()
            chamber_query = Chamber.objects.filter(customer=customer)
            recipes = Recipe.objects.filter(customer=customer)
            step_query = Step.objects.filter(recipe__in=recipes)
            parameter_query = Parameter.objects.all()
            # algorithm_query = Algorithm.objects.all()
            # self.fields['algorithm'].queryset=algorithm_query
            self.fields['algorithm'].queryset = algorithm_query
            self.fields['chamber'].queryset=chamber_query
            self.fields['step'].queryset=step_query
            self.fields['parameter'].queryset=parameter_query

        except:
            user = None

    def clean_parameter(self):
        parameter = self.cleaned_data['parameter']
        for param in parameter:
            if "F1 (Mhz)" in param.parameter_name:
                invalid_entry = param.parameter_name + " is an invalid parameter selection"
                raise forms.ValidationError(invalid_entry)
            elif "Harmonic Phase" in param.parameter_name:
                invalid_entry = param.parameter_name + " is an invalid parameter selection"
                raise forms.ValidationError(invalid_entry)
            else:
                pass
        return parameter

    def clean_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']

        if end < start:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        End Time is earlier than Start Time")
        return end

    def clean_skip_end(self):
        end = self.cleaned_data['end']
        start = self.cleaned_data['start']
        skip_start = self.cleaned_data['skip_start']
        skip_end = self.cleaned_data['skip_end']

        end_of_set = end - timedelta(seconds=skip_end)
        start_of_set = start - timedelta(seconds=skip_start)
        if end_of_set < start_of_set:
            print("ERROR RAISED: ")
            raise forms.ValidationError("The time interval selected is invalid: \
                                        (End time - Seconds to Skip at End)  is earlier than \
                                        (Start time + Seconds to Skip at Start)")
        return skip_end

