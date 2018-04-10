from datetime import datetime, timezone

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import (CharField, DateTimeField, ModelChoiceField,
                          ModelForm, ModelMultipleChoiceField)
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *                          
from django_fine_uploader.forms import (FineUploaderUploadForm,
                                        FineUploaderUploadSuccessForm)
from impedans_expert.expert_algorithms.models import AlgorithmSettings
from impedans_expert.expert_import.models import Run, RunProperty
from impedans_expert.expert_upload.models import FileUploadModel as UploadedFile
from .models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    company_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'company_name')

class ChamberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChamberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post' # this line sets your form's method to post
        # self.helper.form_action = reverse_lazy('your_post_url') # this line sets the form action
        # self.helper.form_class = 'form-horizontal' # if you want to have a horizontally layout form
        self.helper.label_class = 'col-md-4' # this css class attribute will be added to all of the labels in your form. For instance, the "Username: " label will have 'col-md-3'
        self.helper.field_class = 'col-md-12' # this css class attribute will be added to all of the input fields in your form. For isntance, the input text box for "Username" will have 'col-md-9'
        self.helper.layout = Layout( # the order of the items in this layout is important
            'chamber_name',  # field1 will appear first in HTML
            # this is how to add the submit button to your form and since it is the last item in this tuple, it will be rendered last in the HTML
            Div(
                Button('cancel', u'Cancel', css_class='btn btn-secondary', data_dismiss="modal"),
                Submit('submit', u'Submit', css_class='btn btn-primary'),
                css_class='modal-footer'
            )
        )

    class Meta:
        model = Chamber
        fields = ['chamber_name']

class ChamberPropertiesForm(ModelForm):
    property_name = forms.CharField(max_length=100)
    property_value = forms.CharField(max_length=100)

    class Meta:
        model = ChamberProperty
        fields = ['property_name', 'property_value']

class RecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            'name',
            'description',
            Div(
                Button('cancel', u'Cancel', css_class='btn btn-secondary', data_dismiss="modal"),
                Submit('submit', u'Submit', css_class='btn btn-primary'),
                css_class='modal-footer'
            )
        )

    class Meta:
        model = Recipe
        fields = ['name', 'description']

class CustomParameterForm(ModelForm):
    parameter_name_userdef = forms.CharField(max_length=100, label="Enter Custom Name")

    class Meta:
        model = SensorParameter
        fields = ['parameter_name_userdef']

class PropertyForm(ModelForm):
    property_name = forms.CharField(max_length=100, label="Enter new name", required=True)
    property_value = forms.CharField(max_length=100, label="Enter new value", required=True)

    class Meta:
        model = RecipeProperties
        fields = ['property_name', 'property_value']

class AlgorithmSettingsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AlgorithmSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3'
        # self.helper.field_class = 'col-md-9'
        # self.helper.form_class = 'form-inline'
        # self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.layout = Layout(
            'stream_algorithm',
            'parameter',
            Div(
                Div(
                    'recipe',
                    css_class='col-md-6',
                    css_id='no-padding'
                ),
                Div(
                    'result_name',
                    css_class='col-md-6'
                ),
                css_class='row',
                css_id='no-margins'
            ),
            Div(
                Div(
                    'start',
                    css_class='col-md-6'
                ),
                Div(
                    'stop',
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
            Div(
                Button('cancel', u'Cancel', css_class='btn btn-secondary', data_dismiss="modal"),
                Submit('submit', u'Submit', css_class='btn btn-primary'),
                css_class='modal-footer'
            )
        )

    class Meta:
        model = AlgorithmSettings
        fields = ['active', 'stream_algorithm', 'parameter', 'recipe', 'result_name', 'start', 'stop',]

class SensorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-md-4'
        self.helper.field_class = 'col-md-12'
        self.helper.layout = Layout(
            'name',
            'chamber',
            'sensor_type',
            'serial_number',
            Div(
                Button('cancel', u'Cancel', css_class='btn btn-secondary', data_dismiss="modal"),
                Submit('submit', u'Submit', css_class='btn btn-primary'),
                css_class='modal-footer'
            )
        )

    class Meta:
        model = Sensor
        fields = ['name', 'chamber', 'sensor_type', 'serial_number']

class FileUploadForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        customer = Customer.objects.filter(user = user)
        chambers = Chamber.objects.filter(customer=customer)
        chamber = forms.ModelChoiceField(queryset=chambers, empty_label="-", required=True)

    class Meta:
        model = UploadedFile
        fields = ['chamber']

class FineUploaderForm(FineUploaderUploadForm):
    #This form represents a basic request from Fine Uploader.
    #The required fields will **always** be sent, the other fields are optional
    #based on your setup.

    #Extend this if you want to add custom parameters in the body of the POST
    #request.
    #sensor = forms.ModelChoiceField(queryset=Sensor.objects.all(), empty_label="-",  required=False)
    #file_type = forms.ModelChoiceField(queryset=File_Type.objects.all(), empty_label="-",  required=False)
    chamber = forms.ModelChoiceField(queryset=Chamber.objects.all(), empty_label="-", required=True)
"""
class FileTypeForm(forms.Form) :
    file_type_name=forms.NumberInput()
    header
    is_time_absolute
    time_column
    time_zone
    relative_time_cell
    chamber_column
    chamber_properties_column
    marker_column
    run_column
    run_properties_column
    sensor_column
    frequency_column
    voltage_column
    current_column
    phase_column
    temerature_column

"""

###################################
# Define filter form for Chambers #
###################################

class ChambersFilterForm(forms.Form):

    chamber = ModelChoiceField(queryset=None, required=True, label="Chamber")
    property_name = ModelChoiceField(queryset=None,  required=False, label="Property Name")
    property_value = ModelChoiceField(queryset=None,  required=False, label="Property Value")

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ChambersFilterForm, self).__init__(*args, **kwargs)
        try:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            chamber_query = Chamber.objects.filter(customer=customer)
            properties_query = ChamberProperty.objects.filter(chamber=chamber)
            self.fields['chamber'].queryset=chamber_query
            self.fields['property_name'].queryset=properties_query
            self.fields['property_name'].queryset=properties_query
        except:
            user = None
