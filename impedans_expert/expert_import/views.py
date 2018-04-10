import os
import os.path

import django_filters

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic.edit import CreateView, View, FormView
from django.views import generic
from django.template import loader

from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer, Chamber, Sensor, SensorParameter
from impedans_expert.expert_upload.models import FileType, FileUploadModel

from . models import Run, RunParameter, RunProperty, RunValue, RunValueConfiguration
from . forms import FileParseForm, RunPropertiesForm, RunsFilterForm, RunRecipeForm, RunValuesForm
from . utils import run_csv_parser
from . octiv_parser import OctivParser


class FileParser(generic.DetailView):
    template = 'expert_import/fileparser.html'
    def get(self, request):
        parser_form = FileParseForm(request=request)
        print(settings.APPS_DIR)
        return render(request, self.template, {'parse_form': parser_form})

    def post(self, request, *args, **kwargs):
        form = FileParseForm(request.POST, request=request)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            parse_files = form.cleaned_data['file']
            config_file = form.cleaned_data['config']
            parse_files = list(parse_files)
            for parse_file in parse_files:
                file = parse_file.file.url
                file = file.split("/files")
                file_dir = settings.FILES_ROOT + file[1]
                if config_file.name == "Octiv":
                    parser = OctivParser()
                    OctivParser.process_file.delay(parser, file_dir, parse_file)
                    # OctivParser.process_file(parser, file_dir, parse_file)
                else:
                    conf = config_file.parser_config.url
                    conf = conf.split("/media")
                    print(config_file.parser_config)
                    config_dir = settings.MEDIA_ROOT + "/" +str(config_file.parser_config)
                    print(config_dir)
                    run_csv_parser.delay(customer, file_dir, config_dir)
        else:
            print("Invalid form")
        parser_form = FileParseForm(request=request)
        return render(request, self.template, {'parse_form': parser_form})

class RunInfoView(generic.DetailView):
    model = Run
    template_name = 'expert_import/run.html'
    def get(self, request, runs_id):
        run_property_form = RunPropertiesForm()
        run_value_form = RunValuesForm()
        run = Run.objects.get(pk=runs_id)
        chamber = Chamber.objects.get(run=run)
        sensor_list = Sensor.objects.filter(chamber=chamber)
        run_length = str(run.end_time - run.start_time)
        run_properties = list(RunProperty.objects.filter(run=run))
        run_values = list(RunValue.objects.filter(run=run))
        range_period = [run.start_time, run.end_time]
        print(range_period)
        sensor_parameters = SensorParameter.objects.filter(sensor__in=sensor_list, data__time__range=range_period).distinct()
        return render(request, self.template_name, {'run': run,
                                                    'run_length': run_length,
                                                    'run_properties': run_properties,
                                                    'run_values': run_values,
                                                    'sensor_parameters': sensor_parameters,
                                                    'run_property_form' : run_property_form,
                                                    'run_value_form': run_value_form})

    def post(self, request, runs_id, *args, **kwargs) :
        if request.user.is_authenticated:
            operation = (request.POST.get("operation")).split("-")
            # Capture the incoming items to either create, update or delete a property or value
            property_id = operation[0]
            property_name = request.POST.get("parameter_1")
            property_value = request.POST.get("parameter_2")

            if  "property" in operation:
                if property_id.isdigit() and "delete" not in operation:
                    run_property = RunProperty.objects.get(pk=property_id)
                    run_property.property_name = property_name
                    run_property.property_value = property_value
                    run_property.save(update_fields=(["property_name", "property_value"]))

                elif property_id == "property":
                    RunProperty.objects.create(run_id=runs_id,
                                                property_name=property_name,
                                                property_value=property_value)

                elif property_id.isdigit() and "delete" in operation:
                    property_to_delete = RunProperty.objects.get(id=property_id)
                    property_to_delete.delete()

            elif  "value" in operation:
                if property_id.isdigit() and "delete" not in operation:
                    run_value = RunValue.objects.get(pk=property_id)
                    run_value.value = property_value
                    run_value.save(update_fields=(["value"]))

                elif property_id == "value":
                    RunValue.objects.create(run_id=runs_id,
                                            run_parameter_id=property_name,
                                            value=property_value)

                elif property_id.isdigit() and "delete" in operation:
                    property_to_delete = RunValue.objects.get(id=property_id)
                    property_to_delete.delete()

        return JsonResponse(True, safe=False)

class RunsView(generic.DetailView):
    model = Run
    template_name = 'expert_import/runs.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        chambers = Chamber.objects.filter(customer=customer)
        run_list = Run.objects.filter(chamber__in=chambers)
        form = RunsFilterForm(request=request)
        return render(request, self.template_name, {'filter_form':form, 'run_list': run_list})

    def post(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        form = RunsFilterForm(request.POST, request=request)
        if form.is_valid():
            chambers = form.cleaned_data['chamber']
            recipe = form.cleaned_data['recipe']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            runs = None
            if recipe == None:
                runs = Run.objects.filter(chamber=chambers, start_time__gte=start, end_time__lte=end)
            else:
                runs = Run.objects.filter(chamber=chambers, recipe=recipe, start_time__gte=start, end_time__lte=end)

            template = loader.get_template('expert_import/runs.html')
            results_form = RunsFilterForm(request=request)
            return HttpResponse(template.render({'filter_form':results_form, 'run_list':runs}, request))

class ChartRunsView(generic.DetailView):
    model = Run
    template_name = 'expert_import/chart_runs.html'

    def get(self, request):

        # Get a list of run objects, that are passed through the request
        run_ids = request.GET.getlist('id')
        runs = Run.objects.filter(pk__in=run_ids)

        # Get a list of all chambers that own those runs
        chamber = Chamber.objects.filter(run__in=runs).distinct()

        # Get a list of all sensors that belong to those chambers
        sensor = Sensor.objects.filter(chamber=chamber)

        # Initialize run_start and run_end lists
        run_start_list = []
        run_end_list = []

        # Append start_time(s) and end_time(s) for all runs
        for run in runs:
            run_start_list.append(run.start_time)
            run_end_list.append(run.end_time)

        # Determine the earliest and latest time stamps for all the extracted run times
        # Using Python's min() and max() list methods
        runs_start = min(run_start_list)
        runs_end = max(run_end_list)

        # Build a new list with the earliest run_start and latest run_end
        range_period = [runs_start, runs_end]
        
        # Build query that will filter all SensorParameter objects against sensor, and data
        # Using the __range filter method, which takes a list as input.
        # This will return all SensorParameter objects in that time range, which could potentially
        # be thousands. Applying the .distinct() filter method on the resulting queryset gives us
        # only unique results
        sensor_parameters = SensorParameter.objects.filter(sensor__in=sensor, data__time__range=range_period).distinct()

        return render(request, self.template_name, {'runs': runs,
                                                    'sensor_parameters': sensor_parameters})