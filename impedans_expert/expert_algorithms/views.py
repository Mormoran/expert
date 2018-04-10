import os
import ast
import json
import os.path
from datetime import datetime, timedelta

from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from django.template import loader
from django.views import generic

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from impedans_expert.expert.models import Customer, Chamber, Sensor, Parameter, Data, Recipe, Step
from impedans_expert.expert.forms import *
from impedans_expert.users.models import User
from impedans_expert.expert_import.models import Run, RunProperty

from . models import Algorithm, GoldenSet
from . forms import AlgorithmForm, RunResultsForm, ResultsForm, ZScoreForm, TrainingForm, RecipeForm, TrainedZScoreForm
from . utils import PrepareAlgorithmData, prepare_z_score_run, prepare_algorithm
from . run_algorithm_driver import RunAlgorithms
from . time_algorithm_driver import TimeAlgorithms

# select and run algorithms
class SelectAlgorithm(generic.DetailView):
    template = 'expert_algorithms/algorithm_select.html'
    def get(self, request):
        algorithm_form = AlgorithmForm(request=request)
        return render(request, self.template, {'form': algorithm_form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        form = AlgorithmForm(request.POST, request=request)
        if form.is_valid():
            # read data from the form
            start = form.cleaned_data['start']
            end  = form.cleaned_data['end']
            list_of_parameters = form.cleaned_data['parameter']
            chamber = form.cleaned_data['chamber']
            algorithm = form.cleaned_data['algorithm']
            mode = form.cleaned_data['mode']
            offset_type = form.cleaned_data['offset_type']
            skip_start = form.cleaned_data['skip_start']
            skip_end = form.cleaned_data['skip_end']
            sensors = Sensor.objects.filter(chamber=chamber)
            # Z Score running from this form does not function correctly at the moment
            if "z score" in algorithm.algorithm_name:
                pass
            # =================================================================================
            # work on running z score from this form -> not currently functional
            # =================================================================================

            #     if mode == "runs":
            #         runs_query = Run.objects.filter(chamber=chamber, start_time__gte=start, \
            #                                          end_time__lte=end)
            #         runs = list(runs_query)
            #         runs.sort(key=lambda x: x.start_time)

            #         run_timeframes = []
            #         for run in runs:
            #             run_start = run.start_time + skip_start
            #             run_end = run.end_time - skip_end
            #             timeframe = [run_start, run_end]
            #             run_timeframes.append(timeframe)
            #         runner = RunAlgorithms()
            #         RunAlgorithms.run_state(runner, chamber, sensors, algorithm, parameters[0], runs, run_timeframes)
            #     else:
            #         start = start + timedelta(seconds=skip_start)
            #         end = end - timedelta(seconds=skip_end)
            #         data_preparer = PrepareAlgorithmData()
            #         all_data = data_preparer.get_data(list_of_parameters, start, end, chamber)
            #         checked_data = data_preparer.check_and_correct_data(all_data)
            #         formatted_data = data_preparer.format_data(checked_data)
            #         if formatted_data == None:
            #             algorithm_form = AlgorithmForm(request=request)
            #             return render(request, self.template, {'form': algorithm_form})

            #         state = []
            #         runner = TimeAlgorithms()
            #         z_parameter = Parameter.objects.get_or_create(parameter_name="Z Score",
            #                                                       parameter_position="None",
            #                                                       parameter_type="double")
            #         TimeAlgorithms.run_state(runner, start, end, chamber, algorithm, z_parameter, formatted_data, state)

            # =================================================================================

            else:
                # prepare the algorithm to run (get data, format it, run the algorithm) .delay kicks it off as a celery (asynchronous) task
                prepare_algorithm.delay(list_of_parameters, chamber, start, end, sensors, algorithm, mode, skip_start, skip_end, offset_type)
            algorithm_form = AlgorithmForm(request=request)
            return render(request, self.template, {'form': algorithm_form})
        else:
            algorithm_form = AlgorithmForm(request=request)
            return render(request, self.template, {'form': algorithm_form})


class TrainingPage(generic.DetailView):
    permission_classes = (IsAuthenticated,)
    template = 'expert_algorithms/training_page.html'

    param_names = []
    param_ids = []
    means = []
    stds = []
    step = []
    step_start = None
    step_end = None
    chambers = []

    def get(self, request):
        # data that will need to be kept in memory until a step's golden data is approved
        if len(self.param_names) > 0:
            for i in range((len(self.param_names)-1), -1, -1):
                self.param_names.pop(i)
                self.param_ids.pop(i)
                self.means.pop(i)
                self.stds.pop(i)
        self.step = []
        self.step_start = None
        self.step_end = None
        self.chambers = []

        recipe_form = RecipeForm()
        training_form = TrainingForm(request=request)
        return render(request, self.template, {'form': training_form, 'recipe_form': recipe_form, 'params':self.param_names, 'param_ids':self.param_ids, 'means':self.means, 'stds':self.stds})

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            customer = Customer.objects.get(user=user)
            form = RecipeForm(request.POST)
            was_training_algorithm_run = False
            # if the recipe form is submitted create a recipe instance
            if form.is_valid():
                Recipe.objects.create(name=form.cleaned_data["name"], customer=customer)
            # else configure the training algorithm and run it
            else:
                form = TrainingForm(request.POST, request=request)
                if form.is_valid():
                    # if there are any set variables still available, discard them
                    if len(self.param_names) > 0:
                        for i in range((len(self.param_names)-1), -1, -1):
                            self.param_names.pop(i)
                            self.param_ids.pop(i)
                            self.means.pop(i)
                            self.stds.pop(i)
                    # indicate that the training algorithm is being run
                    was_training_algorithm_run = True
                    # read the form data
                    recipe = form.cleaned_data['recipe']
                    algorithm = form.cleaned_data['algorithm']
                    step_number = form.cleaned_data['step']
                    self.step_start = form.cleaned_data['step_start']
                    self.step_end = form.cleaned_data['step_end']
                    self.chambers.append(form.cleaned_data['chamber'])
                    parameters = form.cleaned_data['parameter']
                    parameters = list(parameters)
                    # get step if it already exists / create new step
                    try:
                        self.step.append(Step.objects.get(recipe=recipe, step_number=step_number))
                        self.step[-1].start = self.step_start
                        self.step[-1].end = self.step_end
                    except:
                        self.step.append(Step(recipe=recipe, step_number=step_number))
                    # run training algorithm
                    # - gather and format data correctly - start, stop, parameters, chamber

                    # get the data
                    preparation = PrepareAlgorithmData()
                    data = preparation.get_data(parameters, self.step_start, self.step_end, self.chambers[-1])
                    if len(data[0]) != 0:
                        #  if data set is not empty, check if it is correct and remove invalid parameter data
                        data, parameters = preparation.check_and_correct_data(data, parameters)
                        # format the data (1 column per parameter)
                        data = preparation.format_data(data)
                        # - algorithm_runner() - formatted data
                        # no state is required - so pass a placeholder
                        state = []
                        runner = TimeAlgorithms()
                        # run the algorithm
                        results = runner.run_state(self.step_start, self.step_end, self.chambers[-1], algorithm, parameters, data, state)
                        # display results

                        # save Golden Set
                        results.insert(0, parameters)
                        for p, param in enumerate(results[0]):
                            self.param_names.append(param.parameter_name)
                            self.param_ids.append(param.id)
                            self.means.append(results[1][p])
                            self.stds.append(results[2][p])
                    else:
                        print("ERROR: no data found to create a valid baseline")
                else:
                    if 'params[]' in request.POST:
                        # if the golden set is approved - save it
                        self.step[-1].save()
                        step = Step.objects.get(recipe=self.step[-1].recipe, step_number=self.step[-1].step_number)
                        golden_data = [self.param_ids, self.means, self.stds]
                        golden_json = json.dumps(golden_data)
                        try:
                            gold_set = GoldenSet.objects.get(step=step , chamber=self.chambers[-1])
                            gold_set.data = golden_data
                            gold_set.save()
                        except:
                            GoldenSet.objects.create(data=golden_json, step=step , chamber=self.chambers[-1])

                    else:
                        print("Failed.")
        recipe_form = RecipeForm()
        training_form = TrainingForm(request=request)
        if was_training_algorithm_run:
            return render(request, self.template, {'form': training_form, 'recipe_form': recipe_form, 'params':self.param_names, 'param_ids':self.param_ids, 'means':self.means, 'stds':self.stds, \
                                                   'chamber': self.chambers[-1], 'start_time': self.step_start, 'end_time': self.step_end})
        else:
            return render(request, self.template, {'form': training_form, 'recipe_form': recipe_form, 'params':self.param_names, 'param_ids':self.param_ids, 'means':self.means, 'stds':self.stds})


# select and display the algorithm results
class ResultsDisplay(APIView): # APIView

    permission_classes = (IsAuthenticated,)
    template = 'expert_algorithms/results_select.html'

    def get(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        # instantiate the form and get the page
        results_form = ResultsForm(request=request)
        run_results_form = RunResultsForm(request=request)
        return render(request, self.template, {'advanced_select': "false", 'algorithm_run_id':-1, \
                                               'customer':customer.id, 'algorithm':-1, 'chamber':-1, 'parameter':-1, 'mode':"", \
                                               'run_form': run_results_form, 'form': results_form})

    def post(self, request):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        form = ResultsForm(request.data, request=request)
        run_form = RunResultsForm(request.data, request=request)

        if form.is_valid():
            # get form data
            parameter = form.cleaned_data['parameter']
            chamber = form.cleaned_data['chamber']
            algorithm = form.cleaned_data['algorithm']
            mode = form.cleaned_data['mode']

            template = loader.get_template('expert_algorithms/results_display.html')
            results_form = ResultsForm(request=request)
            run_results_form = RunResultsForm(request=request)
            return HttpResponse(template.render({'algorithm_run_id':-1, 'advanced_select':"true", 'algorithm': algorithm.id, 'chamber': chamber.id, \
                                                 'customer':customer.id, 'parameter': parameter.id, 'mode': mode, 'form': results_form, \
                                                 'run_form': run_results_form}, request))
        elif run_form.is_valid():
            algorithm_run = run_form.cleaned_data['algorithm_run']

            template = loader.get_template('expert_algorithms/results_display.html')
            results_form = ResultsForm(request=request)
            run_results_form = RunResultsForm(request=request)
            return HttpResponse(template.render({'advanced_select':"false", 'algorithm_run_id':algorithm_run.id, 'form': results_form, \
                                                 'customer':customer.id, 'algorithm':-1, 'chamber':-1, 'parameter':-1, 'mode': "", \
                                                 'run_form': run_results_form}, request))
        # if not valid just refresh the form page
        else:
            template = loader.get_template(self.template)
            results_form = ResultsForm(request=request)
            run_results_form = RunResultsForm(request=request)
            return HttpResponse(template.render({'advanced_select':"false", 'algorithm_run_id':-1, 'form': results_form, \
                                                'customer':customer.id, 'algorithm':-1, 'chamber':-1, 'parameter':-1, 'mode': "",  \
                                                'run_form': run_results_form}, request))

class RunZScore(generic.DetailView):
    template = 'expert_algorithms/z_score_form.html'
    def get(self, request):
        z_score_form = ZScoreForm(request=request)
        return render(request, self.template, {'form': z_score_form})


    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        form = ZScoreForm(request.POST, request=request)

        if form.is_valid():
            # read form data
            parameters = form.cleaned_data['parameter']
            parameters = list(parameters)
            chamber = form.cleaned_data['chamber']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            skip_start = form.cleaned_data['skip_start']
            skip_end = form.cleaned_data['skip_end']
            window_size = form.cleaned_data['window_size']
            z_score_limit = form.cleaned_data['z_score_limit']
            start = start + timedelta(seconds=skip_start)
            end = end - timedelta(seconds=skip_end)
            # prepare data for processing and run the algorithm
            prepare_z_score_run.delay(parameters, start, end, chamber, window_size, z_score_limit)
        template = loader.get_template(self.template)
        return HttpResponse(template.render({'form': form}, request))

class RunTrainedZScore(generic.DetailView):
    template = 'expert_algorithms/trained_z_score_form.html'
    def get(self, request):
        z_score_form = TrainedZScoreForm(request=request)
        return render(request, self.template, {'form': z_score_form})


    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        customer = Customer.objects.get(user=user)
        form = TrainedZScoreForm(request.POST, request=request)

        if form.is_valid():
            # read form data
            algorithm = form.cleaned_data['algorithm']
            step = form.cleaned_data['step']
            parameters = form.cleaned_data['parameter']
            parameters = list(parameters)
            chamber = form.cleaned_data['chamber']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            skip_start = form.cleaned_data['skip_start']
            skip_end = form.cleaned_data['skip_end']
            window_size = int(form.cleaned_data['window_size'])
            z_score_limit = int(form.cleaned_data['z_score_limit'])
            start = start + timedelta(seconds=skip_start)
            end = end - timedelta(seconds=skip_end)

            # get golden set
            gold_data = GoldenSet.objects.get(step=step, chamber=chamber)
            gold_data = ast.literal_eval(gold_data.data)

            allowed_parameters = gold_data[0]
            golden_means = gold_data[1]
            golden_stds = gold_data[2]

            # remove invalid parameters from selection
            # if the parameters selected are not in the golden set then they cannot be processed
            # so therefore they are removed at the stage
            disallowed_parameter_indices = []
            allowed_parameter_ids = []

            for p, param in enumerate(parameters):
                if not param.id in allowed_parameters:
                    disallowed_parameter_indices.append(p)
                else:
                    allowed_parameter_ids.append(param.id)

            # also if a parameter from the golden set is not used remove the related "golden values"
            # associated with it
            for index in reversed(disallowed_parameter_indices):
                del golden_means[index]
                del golden_stds[index]

            # thin out parameters, means and stds to match the selected data
            params_to_process = []
            for par_id in allowed_parameter_ids:
                param = [par for par in parameters if par.id == par_id]
                params_to_process.append(param[0])

            # delete variables that are no longer necessary
            del gold_data
            del parameters
            del allowed_parameters
            del disallowed_parameter_indices
            del allowed_parameter_ids

            # prepare data and run the algorithm as a celery (asynchronous) task
            prepare_z_score_run.delay(params_to_process, start, end, chamber, window_size, \
                                      z_score_limit)

        template = loader.get_template(self.template)
        return HttpResponse(template.render({'form': form}, request))

