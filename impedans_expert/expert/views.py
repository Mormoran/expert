# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import operator
import os
from functools import reduce

import pprint

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.forms import formset_factory
from django.http import (Http404, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View
from django_fine_uploader import urls as uploader_urls
from django_fine_uploader.forms import FineUploaderUploadForm
from django_fine_uploader.views import FineUploaderView
from impedans_expert.expert.forms import *
from impedans_expert.expert.models import *
from impedans_expert.expert_algorithms.models import (AlgorithmSettings,
                                                      AlgorithmState,
                                                      AlgorithmVariables,
                                                      StreamAlgorithm)
from impedans_expert.expert_import.models import RunParameter
from impedans_expert.expert_upload.models import *
from impedans_expert.users.models import User
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

# users must be created by a admin user through the admin page
"""
# Create your views here.
def signup(request):
    if request.method == "POST" :
        form = SignUpForm(request.POST)
        if form.is_valid() :
            user_name = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password1']
            user = User.objects.create_user(username=user_name, email=email, password=password, first_name=first_name, last_name=last_name)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            company_name = request.POST['company_name']
            contact_name = first_name + " " + last_name
            customer = Customer.objects.create(company_name=company_name, contact_name=contact_name, contact_email=email, user=user)

            return redirect('details')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
"""

######################################################
# Define class based view for About page GET request #
######################################################

class AboutView(generic.DetailView):
    template_name = 'pages/about.html'

    def get(self, request) :
        return render(request, self.template_name, {})

########################################################
# Define class based view for Details page GET request #
########################################################

class DetailsView(ListAPIView):
    model = Customer
    template_name = 'pages/details.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        cust = Customer.objects.get(user=user)
        files = FileUploadModel.objects.filter(customer=cust)
        chambers = Chamber.objects.filter(customer=cust)
        runs = Run.objects.filter(chamber__in=chambers)
        runs = list(runs)
        sensors = Sensor.objects.filter(chamber_id__in=chambers)
        data = Data.objects.filter(sensor_id__in=sensors)
        query = reduce(operator.and_, (~Q(parameter_name__icontains=list) for list in ['mean', 'standard deviation', 'z score']))
        parameters = Parameter.objects.all().distinct('parameter_name').filter(query)
        positions = parameters.values_list('parameter_position', flat=True).distinct()
        return render(request, self.template_name, {'chambers': chambers, 'files': files, 'runs': runs, 'sensors': sensors, 'data': data, 'parameters': parameters, 'positions': positions})

#########################################################
# Define class based view for Customer page GET request #
#########################################################

class CustomerView(generic.DetailView):
    model = Customer
    template_name = 'expert/customer.html'

    def get(self, request) :
        cust = Customer.objects.get(user=request.user)
        return render(request, self.template_name, {'customer': cust})

########################################################
# Define class based view for Profile page GET request #
########################################################

class ProfileView(generic.DetailView):
    model = Customer
    template_name = 'pages/profile.html'

    def get(self, request) :
        cust = Customer.objects.get(user=request.user)
        return render(request, self.template_name, {'customer': cust})

#############################################################
# Define class based view for Live Z-Score page GET request #
#############################################################

class LiveView(generic.DetailView):
    model = Data
    template_name = 'expert/live.html'

    def get(self, request) :
        user = User.objects.get(username=request.user)
        cust = Customer.objects.get(user=user)
        files = FileUploadModel.objects.filter(customer=cust)
        chambers = Chamber.objects.filter(customer=cust)
        runs = Run.objects.filter(chamber__in=chambers)
        runs = list(runs)
        sensors = Sensor.objects.filter(chamber_id__in=chambers)
        data = Data.objects.filter(sensor_id__in=sensors)
        query = reduce(operator.and_, (~Q(parameter_name__icontains=list) for list in ['mean', 'standard deviation', 'z score']))
        parameters = Parameter.objects.all().distinct('parameter_name').filter(query)
        positions = parameters.values_list('parameter_position', flat=True).distinct()
        return render(request, self.template_name, {'user': user})

####################################################################################
# Define class based view for Chamber Information page, both POST and GET requests #
####################################################################################

class ChamberInfoView(generic.DetailView):
    model = Chamber
    template_name = 'expert/chamber.html'

    def get(self, request, chamber_id) :
        chamber = Chamber.objects.get(pk=chamber_id)
        chamber_properties_form = ChamberPropertiesForm()
        chamber_properties = ChamberProperty.objects.filter(chamber=chamber)
        sensors_list = list(Sensor.objects.filter(chamber=chamber))
        active_sensors = list(Sensor.objects.filter(chamber=chamber, active=True))
        chamber_parameters = SensorParameter.objects.filter(sensor_id__in=active_sensors)
        sensor_form = SensorForm()
        return render(request, self.template_name, {'chamber': chamber,
                                                    'chamber_properties': chamber_properties,
                                                    'sensors_list': sensors_list,
                                                    'chamber_property_form': chamber_properties_form,
                                                    'chamber_parameters': chamber_parameters,
                                                    'sensor_form': sensor_form })

    def post(self, request, chamber_id, *args, **kwargs) :
        if request.user.is_authenticated:

            operation = request.POST.get("property_id")

            if  operation != "new-sensor":
                # Capture the incoming items to either create, update or delete a property
                property_id = request.POST.get("property_id")
                property_name = request.POST.get("parameter_1")
                property_value = request.POST.get("parameter_2")
                delete_flag = "delete"

                # The property_id incoming is either "new-property", "delete-<PKID>" or 
                # a property PK ID depending on the button clicked.
                # Here we determine whether it's an existing ID or not
                if property_id.isdigit():
                    chamber_property = ChamberProperty.objects.get(pk=property_id)
                    chamber_property.property_name = property_name
                    chamber_property.property_value = property_value
                    chamber_property.save(update_fields=(["property_name", "property_value"]))

                elif property_id == "new-property":
                    ChamberProperty.objects.create(chamber_id=chamber_id,
                                                    property_name=property_name,
                                                    property_value=property_value)

                elif delete_flag in property_id:
                    property_id = property_id.split("-")[1]
                    property_to_delete = ChamberProperty.objects.get(id=property_id)
                    property_to_delete.delete()
            else:
                print("Here")
                name = request.POST.get("parameter_1")
                sensor_type_id = request.POST.get("parameter_2")
                sensor_type = SensorType.objects.get(pk=sensor_type_id)
                serial_number = request.POST.get("parameter_3")
                Sensor.objects.create(chamber_id=chamber_id,
                                    name=name,
                                    sensor_type=sensor_type,
                                    serial_number=serial_number)

        return JsonResponse(True, safe=False)

####################################################################################
# Define class based view for Sensor Information page, both POST and GET requests #
####################################################################################

class SensorInfoView(generic.DetailView):
    model = Sensor
    template_name = 'expert/sensor.html'

    def get(self, request, sensor_id):
        sensor = Sensor.objects.get(pk=sensor_id)
        chamber = Chamber.objects.get(sensor=sensor)
        sensor_parameters = SensorParameter.objects.filter(sensor=sensor)
        custom_param_form = CustomParameterForm()
        return render(request, self.template_name, {'sensor': sensor,
                                                    'chamber': chamber,
                                                    'custom_param_form': custom_param_form,
                                                    'sensor_parameters': sensor_parameters})

    def post(self, request, sensor_id, *args, **kwargs):
        if request.user.is_authenticated:
            sensor_parameter_id = int(request.POST.get("sensor_parameter_id"))
            parameter_name_userdef = request.POST.get("parameter_name_userdef")

            sensor_parameter = SensorParameter.objects.get(pk=sensor_parameter_id)
            sensor_parameter.parameter_name_userdef = parameter_name_userdef
            sensor_parameter.save(update_fields=(["parameter_name_userdef"]))

            sensor = Sensor.objects.get(pk=sensor_id)
            chamber = Chamber.objects.get(sensor=sensor)
            sensor_parameters = SensorParameter.objects.filter(sensor=sensor)
            custom_param_form = CustomParameterForm()

            # if custom_param_form.is_valid():
            #     custom_param = custom_param_form.cleaned_data['parameter_name_userdef']
            #     custom_param_form.save()
            #     return redirect(sensor)
        return render(request, self.template_name, {'sensor': sensor,
                                                    'chamber': chamber,
                                                    'custom_param_form': custom_param_form,
                                                    'sensor_parameters': sensor_parameters})

##########################################################################
# Define function view for Sensor Live Values JSON List page GET request #
##########################################################################

def SensorLiveValues(request, sensor_id):

    sensor = Sensor.objects.get(id=sensor_id)
    sensors_parameter_list = SensorParameter.objects.filter(sensor=sensor)
    data = []
    for param in sensors_parameter_list :
        point = {}
        point['Parameter'] = param.parameter.parameter_name
        point['Custom Name'] = param.parameter_name_userdef
        rounded_value = round(param.live_value, 2)
        point['Value'] = rounded_value
        data.append(point)

    return JsonResponse(data, safe=False)

################################################################################
# Define class based view for Run Information page, both POST and GET requests #
################################################################################

class RunInfoView(generic.DetailView):
    model = Run
    template_name = 'expert/run.html'
    def get(self, request, run_id):
        run_property_form = RunPropertiesForm()
        run = Run.objects.get(pk=run_id)
        return render(request, self.template_name, {'run': run, 'run_property_form' : run_property_form})

    def post(self, request, *args, **kwargs) :
        if request.user.is_authenticated:
            #get button id
            button = request.POST.get("button")

            if "remove" in button :
                split_str = button.split("_")
                rp_id_str = split_str[1]
                rp_id = int(rp_id_str)
                rp = RunProperty.objects.get(pk=rp_id)
                rp.delete()
            elif "property_submit" in button :
                property_id = int(request.POST.get("property_id"))
                property_name = request.POST.get("property_name")
                property_value = request.POST.get("property_value")

                if property_id == 0:
                    run_id = int(request.POST.get("run_id"))
                    RunProperty.objects.create(run_id=run_id, property_name=property_name, property_value=property_value)
                else:
                    run_property = RunProperty.objects.get(pk=property_id)
                    run_property.property_name = property_name
                    run_property.property_value = property_value
                    run_property.save(update_fields=(["property_name", "property_value"]))
            else :
                pass
        return JsonResponse(True, safe=False)

##############################################################
# Define class based view for Run Overview page -DEPRECATED- #
##############################################################

# class RunsView(generic.ListView):
#     model = Run
#     template_name = 'expert/runs.html'

#######################################################################
# Define class based view for Parameters Information page GET request #
#######################################################################

class ParameterView(generic.ListView):
    model = Parameter
    template_name = 'expert/parameters.html'

##########################################################
# Define function view for Sensors List page GET request #
##########################################################

def SensorListView(request):
    customer = Customer.objects.get(user=request.user)
    chambers = Chamber.objects.filter(customer=customer)
    sensor_list = Sensor.objects.filter(chamber__in=chambers)
    return render(request, 'expert/sensor_list.html', {'sensor_list': sensor_list})

##########################################################
# Define function view for Chamber List page GET request #
##########################################################

def ChamberListView(request):
    customer = Customer.objects.get(user=request.user)
    chamber_list = Chamber.objects.filter(customer=customer)
    return render(request, 'expert/chamber_list.html', {'chamber_list': chamber_list})

#############################################################################
# Define class based view for Recipes List page, both POST and GET requests #
#############################################################################

class RecipeListView(generic.ListView):
    def get(self, request):
        customer = Customer.objects.get(user=request.user)
        recipe_list = Recipe.objects.filter(customer=customer)
        recipe_form = RecipeForm()
        return render(request, 'expert/recipe_list.html', {'form': recipe_form,
                                                            'recipe_list': recipe_list})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            #get button id
            button = request.POST.get("button")
            if "remove" in button :
                split_str = button.split("_")
                rp_id_str = split_str[1]
                rp_id = int(rp_id_str)
                rp = Recipe.objects.get(pk=rp_id)
                rp.delete()
            elif "recipe_submit" in button :
                recipe_id = int(request.POST.get("recipe_id"))
                name = request.POST.get("name")

                if recipe_id == 0:
                    Recipe.objects.create(name=name, customer=customer)
                else:
                    recipe = Recipe.objects.get(pk=recipe_id)
                    recipe.name = name
                    recipe.save(update_fields=(["name"]))
            else:
                pass
        recipe_list = Recipe.objects.filter(customer=customer)
        recipe_form = RecipeForm()
        return render(request, 'expert/recipe_list.html', {'form': recipe_form,
                                                            'recipe_list': recipe_list})                                                         

################################################################################
# Define class based view for Sensor Creation page, both POST and GET requests #
################################################################################

class SensorCreate(CreateView):
    model = Sensor
    fields = [ 'chamber', 'sensor_type', 'serial_number']

##############################################################
# Define function view for Sensor JSON List page GET request #
##############################################################

# def sensors(request):

#     cust = Customer.objects.filter(user=request.user)
#     chambers = Chamber.objects.filter(customer=cust)
#     sensors_list = Sensor.objects.filter(chamber__in=chambers)
#     all_sensor_objects = []
#     for sens in sensors_list :
#         sensor_object = {}
#         sensor_object['id'] = sens.pk
#         sensor_object['chamber_id']=sens.chamber_id
#         sensor_object['sensor_type_id']=sens.sensor_type_id
#         sensor_object['serial_number']=sens.serial_number
#         all_sensor_objects.append(sensor_object)

#     return JsonResponse(all_sensor_objects, safe=False)

###############################################################
# Define function view for Chamber JSON List page GET request #
###############################################################

# def chambers(request):

#     cust = Customer.objects.filter(user=request.user)
#     chamber_list = Chamber.objects.filter(customer=cust)
#     all_chamber_objects = []
#     for cham in chamber_list:
#         chamber_object = {}
#         chamber_object['id']=cham.pk
#         chamber_object['chamber_name']=cham.chamber_name
#         all_chamber_objects.append(chamber_object)

#     return JsonResponse(all_chamber_objects, safe=False)

#############################################################
# Define function view for Files JSON List page GET request #
#############################################################

def files(request):

    cust = Customer.objects.filter(user=request.user)
    files_list = FileUploadModel.objects.filter(customer=cust)
    all_file_objects = []
    for file in files_list:
        file_object = {}
        file_object['id']=file.pk
        file_object['name']=file.name
        file_object['sensor_id']=file.sensor_id
        file_object['file_type_id']=file.file_type_id
        file_object['processed']=file.parsed
        all_file_objects.append(file_object)

    return JsonResponse(all_file_objects, safe=False)

###################################################################
# Define function view for Files Types JSON List page GET request #
###################################################################

def filetypes(request):
    cust = Customer.objects.filter(user=request.user)
    files_types_list = FileType.objects.filter(customer=cust)
    all_file_type_objects = []
    for file in files_types_list:
        file_type_object = {}
        file_type_object['id']=file.pk
        file_type_object['name']=file.name
        all_file_type_objects.append(file_type_object)

    return JsonResponse(all_file_type_objects, safe=False)

#####################################################
# Define class based view for Home page GET request #
#####################################################

class HomeView(generic.DetailView):
    template_name = 'pages/home.html'

    def get(self, request) :
        return render(request, self.template_name, {})

#################################################################
# Define class based view for Chamber Overview page GET request #
#################################################################

class ChambersView(generic.DetailView):
    template_name = 'pages/chambers.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        chambers_list = list(Chamber.objects.filter(customer=customer).prefetch_related('chamberproperty_set'))

        last_run_list = []
        properties = []
        for chamber in chambers_list:
            try:
                last_run_list.append(chamber.run_set.all().latest('end_time'))
            except:
                last_run_list.append("No runs yet.")

            # if ChamberProperty.objects.filter(chamber=chamber):
            #     properties.append(ChamberProperty.objects.filter(chamber=chamber))

        try:
            last_recipe = "No recipes yet."
        except:
            last_recipe = "No recipes yet."
        
        try:
            last_z_score = AlgorithmTimeResults.objects.latest('id')
        except:
            last_z_score = "No Z-Scores yet."
        
        for chamber in chambers_list:
            properties = chamber.chamberproperty_set.all()

        chambers_runs_list = zip(chambers_list, last_run_list)

        chamber_form = ChamberForm()

        return render(request, self.template_name, {'chamber_form': chamber_form,
                                                    'chambers_runs_list': chambers_runs_list,
                                                    'last_recipe': last_recipe,
                                                    'last_z_score': last_z_score,
                                                    'properties': properties})

    def post(self, request):
        chamber_form = ChamberForm(request.POST)
        if request.user.is_authenticated :
            if chamber_form.is_valid():
                chamber_name = request.POST['chamber_name']
                customer = Customer.objects.get(user=request.user)
                chamber = Chamber.objects.create(chamber_name=chamber_name, customer=customer)
                return HttpResponseRedirect(self.request.path_info)

##############################################################################
# Define view function for Chamber creation page, both POST and GET requests #
##############################################################################

def chamberCreate(request):
    properties_form_set = formset_factory(ChamberPropertiesForm)
    if request.method == "POST" :
        chamber_form = ChamberForm(request.POST)
        properties_formset = properties_form_set(request.POST)
        if request.user.is_authenticated :
            if chamber_form.is_valid() and properties_formset.is_valid():
                chamber_name = request.POST['chamber_name']
                customer = Customer.objects.get(user=request.user)
                chamber = Chamber.objects.create(chamber_name=chamber_name, customer=customer)

                for f in properties_formset :
                    p_form = f.cleaned_data
                    property_name = p_form.get('property_name')
                    property_value = p_form.get('property_value')
                    chamber_property = ChamberProperty.objects.create(property_name=property_name, property_value=property_value, chamber=chamber)

                return redirect('chamber_list')
    else:
        chamber_form = ChamberForm()
        properties_formset = properties_form_set()
    return render(request, 'expert/chamber_form.html', {'chamber_form': chamber_form, 'properties_formset': properties_formset})

################################################################
# Define class based view for Sensor Overview page GET request #
################################################################

class SensorsView(generic.DetailView):
    template_name = 'pages/sensors.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        chamber = Chamber.objects.filter(customer=customer)
        sensors_list = list(Sensor.objects.filter(chamber_id__in=chamber).prefetch_related('chamber', 'sensor_type'))
        sensor_types = []
        for sensor in sensors_list:
            if sensor.sensor_type not in sensor_types:
                sensor_types.append(sensor.sensor_type)
        
        try:
            last_run = Run.objects.latest('end_time')
        except:
            last_run = "No runs yet."

        try:
            last_recipe = RunProperty.objects.latest('id')
        except:
            last_recipe = "No recipes yet."
        
        try:
            last_z_score = AlgorithmTimeResults.objects.latest('id')
        except:
            last_z_score = "No Z-Scores yet."

        sensor_form = SensorForm()

        return render(request, self.template_name, {'sensor_form': sensor_form,
                                                    'sensors_list': sensors_list,
                                                    'sensor_types': sensor_types,
                                                    'last_run': last_run,
                                                    'last_recipe': last_recipe,
                                                    'last_z_score': last_z_score})

    def post(self, request):
        sensor_form = SensorForm(request.POST)
        if request.user.is_authenticated :
            if sensor_form.is_valid():
                name = request.POST['name']
                chamber = Chamber.objects.get(id=request.POST['chamber'])
                serial_number = request.POST['serial_number']
                sensor_type = SensorType.objects.get(id=request.POST['sensor_type'])
                sensor = Sensor.objects.create(name=name, chamber=chamber, serial_number=serial_number, sensor_type=sensor_type)
                return HttpResponseRedirect(self.request.path_info)

################################################################
# Define class based view for Recipe Overview page GET request #
################################################################

class RecipesView(generic.DetailView):
    template_name = 'pages/recipes.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        recipes_list = list(Recipe.objects.filter(customer=customer))
        properties_list = list(RecipeProperties.objects.filter(recipe__in=recipes_list))
        recipe_form = RecipeForm()

        return render(request, self.template_name, {'recipe_form': recipe_form,
                                                    'recipes_list': recipes_list,
                                                    'properties_list': properties_list})

    def post(self, request):
        recipe_form = RecipeForm(request.POST)
        if request.user.is_authenticated :
            if recipe_form.is_valid():
                name = request.POST['name']
                description = request.POST['description']
                customer = Customer.objects.get(user=request.user)
                recipe = Recipe.objects.create(name=name, description=description, customer=customer)
                return HttpResponseRedirect(self.request.path_info)


###################################################################################
# Define class based view for Recipe information page, both POST and GET requests #
###################################################################################

class RecipeInfoView(generic.DetailView):
    model = Recipe
    template_name = 'expert/recipe.html'

    def get(self, request, recipe_id):
        customer                = Customer.objects.get(user=request.user)
        recipe                  = Recipe.objects.get(id=recipe_id)
        recipe_properties       = RecipeProperties.objects.filter(recipe=recipe)
        property_form           = PropertyForm()
        algorithm_settings_form = AlgorithmSettingsForm()
        algorithm_settings      = AlgorithmSettings.objects.filter(recipe=recipe, active=True).order_by('configuration_thread', '-date_time').distinct('configuration_thread')
        return render(request, self.template_name, {'recipe': recipe,
                                                    'recipe_properties': recipe_properties,
                                                    'algorithm_settings': algorithm_settings,
                                                    'algorithm_settings_form': algorithm_settings_form,
                                                    'property_form': property_form})

    def post(self, request, recipe_id, slug=None, *args, **kwargs):
        if request.user.is_authenticated:

            if 'submit' in request.POST:
                algorithm_settings_form = AlgorithmSettingsForm(request.POST)
                if algorithm_settings_form.is_valid():
                    stream_algorithm = StreamAlgorithm.objects.get(id=request.POST['stream_algorithm'])
                    parameter = Parameter.objects.get(id=request.POST['parameter'])
                    recipe = Recipe.objects.get(id=request.POST['recipe'])
                    result_name = request.POST['result_name']
                    start = request.POST['start']
                    stop = request.POST['stop']
                    algorithm_settings = AlgorithmSettings.objects.create(active=True,
                                                                            stream_algorithm=stream_algorithm,
                                                                            parameter=parameter,
                                                                            recipe=recipe,
                                                                            result_name=result_name,
                                                                            start=start,
                                                                            stop=stop)
            else:
                # Capture the incoming items to either create, update or delete a property
                property_id = request.POST.get("property_id")
                property_name = request.POST.get("property_name")
                property_value = request.POST.get("property_value")
                delete_prop = "delete"
                delete_alg = "alg"

                # The property_id incoming is either "new-property", "delete-<PKID>" or 
                # a property PK ID depending on the button clicked.
                # Here we determine whether it's an existing ID or not
                if property_id.isdigit():
                    recipe_property = RecipeProperties.objects.get(pk=property_id)
                    recipe_property.property_name = property_name
                    recipe_property.property_value = property_value
                    recipe_property.save(update_fields=(["property_name", "property_value"]))
                elif property_id == "new-property":
                    RecipeProperties.objects.create(recipe_id=recipe_id,
                                                    property_name=property_name,
                                                    property_value=property_value)
                elif delete_prop in property_id:
                    property_id = property_id.split("-")[1]
                    property_to_delete = RecipeProperties.objects.get(id=property_id)
                    property_to_delete.delete()
                elif delete_alg in property_id:
                    algorithm_id = property_id.split("-")[1]
                    algorithm_to_delete = AlgorithmSettings.objects.get(id=algorithm_id)
                    algorithm_to_delete.delete()

                

        return HttpResponseRedirect(self.request.path_info)

#####################################################################################
# Define class based view for Recipe configuration page, both POST and GET requests #
#####################################################################################

class RecipeConfigView(generic.DetailView):
    model = AlgorithmSettings
    template_name = 'expert/recipe_config.html'

    def get(self, request, recipe_id, slug):
        customer            = Customer.objects.get(user=request.user)
        recipe              = Recipe.objects.get(id=recipe_id)
        recipe_properties   = RecipeProperties.objects.filter(recipe=recipe)
        algorithm_settings  = AlgorithmSettings.objects.filter(recipe=recipe, configuration_thread=slug).latest('date_time')
        algorithm_type      = StreamAlgorithm.objects.all()
        chambers_list       = list(Chamber.objects.filter(customer=customer).prefetch_related('chamberproperty_set'))

        for chamber in chambers_list:
            properties = chamber.chamberproperty_set.all()

        last_baseline_list = []
        for chamber in chambers_list:
            try:
                baseline = AlgorithmVariables.objects.filter(chamber=chamber, active=True).latest('date_time')
                last_baseline_list.append(baseline)
            except:
                last_baseline_list.append("No baselines configured yet.")

        chambers_baselines_list = zip(chambers_list, last_baseline_list)

        return render(request, self.template_name, {'algorithm_settings': algorithm_settings,
                                                    'algorithm_type': algorithm_type,
                                                    'chambers_baselines_list': chambers_baselines_list,
                                                    'properties': properties,
                                                    'recipe': recipe,
                                                    'recipe_properties': recipe_properties})

    def post(self, request, recipe_id, slug, *args, **kwargs):
        if request.user.is_authenticated:

            customer            = Customer.objects.get(user=request.user)
            recipe              = Recipe.objects.get(id=recipe_id)
            recipe_properties   = RecipeProperties.objects.filter(recipe=recipe)
            algorithm_settings  = AlgorithmSettings.objects.filter(recipe=recipe, configuration_thread=slug).latest('date_time')
            algorithm_type      = StreamAlgorithm.objects.all()
            chambers_list       = list(Chamber.objects.filter(customer=customer).prefetch_related('chamberproperty_set'))

            for chamber in chambers_list:
                properties = chamber.chamberproperty_set.all()

            last_baseline_list = []
            for chamber in chambers_list:
                try:
                    baseline = AlgorithmVariables.objects.filter(chamber=chamber, active=True).latest('date_time')
                    last_baseline_list.append(baseline)
                except:
                    last_baseline_list.append("No baselines configured yet.")

            chambers_baselines_list = zip(chambers_list, last_baseline_list)

            start = request.POST.get("start")
            stop = request.POST.get("stop")
            configuration_thread = request.POST.get("configuration_thread")
            stream_algorithm = StreamAlgorithm.objects.get(algorithm_name=request.POST.get("stream_algorithm"))
            result_name = request.POST.get("result_name")
            parameter = Parameter.objects.get(id=request.POST.get("parameter"))

            AlgorithmSettings.objects.create(stream_algorithm=stream_algorithm,
                                            configuration_thread=configuration_thread,
                                            parameter=parameter,
                                            recipe=recipe,
                                            result_name=result_name,
                                            start=start,
                                            stop=stop)


            return render(request, self.template_name, {'algorithm_settings': algorithm_settings,
                                                        'algorithm_type': algorithm_type,
                                                        'chambers_baselines_list': chambers_baselines_list,
                                                        'properties': properties,
                                                        'recipe': recipe,
                                                        'recipe_properties': recipe_properties})

#######################################################################################
# Define class based view for Baseline Configuration page, both POST and GET requests #
#######################################################################################

class BaselineConfigView(generic.DetailView):
    model = AlgorithmVariables
    template_name = 'expert/baselines.html'

    def get(self, request, recipe_id, stream_algorithm_id, slug):
        stream_algorithm = StreamAlgorithm.objects.get(id=stream_algorithm_id)
        recipe = Recipe.objects.get(id=recipe_id)
        chamber_ids = request.GET.getlist('id')
        chambers = Chamber.objects.filter(pk__in=chamber_ids)
        baselines = AlgorithmVariables.objects.all()
        runs = Run.objects.all()
        sensor_list = Sensor.objects.filter(chamber__in=chambers)
        run_parameters = SensorParameter.objects.filter(sensor__in=sensor_list)
        # print("------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------")
        # for i, param in enumerate(run_parameters):
        #     print(i, param)
        # print("------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------")
        # print("------------------------------------------------------------------------------")

        return render(request, self.template_name, {'stream_algorithm': stream_algorithm,
                                                    'baselines': baselines,
                                                    'chambers': chambers,
                                                    'recipe': recipe,
                                                    'runs': runs,
                                                    'run_parameters': run_parameters})

    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:

    #         ids_array = (request.POST.get("list[]"))

    #         print("Array is ", ids_array)
            
    #         runs = []

    #         for run_id in ids_array:
    #             print(run_id)
    #             runs.append(Run.objects.filter(pk=run_id))
            
    #         print(runs)

            

    #     return render(request, self.template_name, {'runs': runs})

def RunsTableView(request, chamber_id):

    sensor = Sensor.objects.get(id=sensor_id)
    sensors_parameter_list = SensorParameter.objects.filter(sensor=sensor)
    data = []
    for param in sensors_parameter_list :
        point = {}
        point['Parameter'] = param.parameter.parameter_name
        point['Custom Name'] = param.parameter_name_userdef
        rounded_value = round(param.live_value, 2)
        point['Value'] = rounded_value
        data.append(point)

    return JsonResponse(data, safe=False)

#############################################################
# Define class based view for Run Overview page GET request #
#############################################################

class RunsView(generic.DetailView):
    template_name = 'pages/runs.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        chamber = Chamber.objects.filter(customer=customer)
        sensors = Sensor.objects.filter(chamber__in=chamber)
        runs_list = list(Run.objects.filter(chamber__in=chamber))
        run_length = []
        for run in runs_list:
            run_length.append(str(run.end_time - run.start_time))

        runs_lengths_list = list(zip(runs_list, run_length))

        try:
            last_z_score = AlgorithmTimeResults.objects.latest('id')
        except:
            last_z_score = "No Z-Scores yet."

        return render(request, self.template_name, {'runs_lengths_list': runs_lengths_list,
                                                    'last_z_score': last_z_score})

#################################################################
# Define class based view for Reports Overview page GET request #
#################################################################

class ReportsView(generic.DetailView):
    template_name = 'pages/reports.html'

    def get(self, request) :
        return render(request, self.template_name, {})

##########################################################
# Define class based view for Dashboard page GET request #
##########################################################

class DashboardsView(generic.DetailView):
    template_name = 'pages/dashboards.html'

    def get(self, request) :
        return render(request, self.template_name, {})
