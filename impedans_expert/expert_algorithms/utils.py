import json
import statistics
from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings

from celery import shared_task
from celery.decorators import task

from impedans_expert.expert_import.models import Run
from impedans_expert.expert.models import Chamber, Parameter, Sensor, Data
from impedans_expert.expert_algorithms.models import Algorithm, AlgorithmRun, AlgorithmRunResult, AlgorithmTimeResult

from . run_algorithm_driver import RunAlgorithms
from . time_algorithm_driver import TimeAlgorithms

@task(name="Prepare Algorithm Data")
# algorithm preparation - retrieves and formats data for processing
class PrepareAlgorithmData():
    # pull all requested data from the database
    def get_data(self, parameters, start_time, end_time, chamber):
        all_data = []
        sensors =  Sensor.objects.filter(chamber=chamber)
        for parameter in parameters:
            data_query = Data.objects.filter(time__gte=start_time, time__lte=end_time, \
                                             sensor__in=sensors, parameter_id=parameter.id).order_by("time")
            data = list(data_query)
            all_data.append(data)
        del sensors
        return all_data

    # format data into a 2D array - 1 column per parameter selected
    def format_data(self, data):
        data = list(zip(*data))
        formatted_data = []
        if len(data) == 0:
            return None
        for row in data:
            formatted_data.append(list(row))
        del data
        return formatted_data

    # check data if valid for the algorithm
    # remove invalid data points
    # data = 2D row (this is executed before the format_data step)
    # this function ensures all rows in the 2D array are of equal length
    # to prevent index errors in calculations
    def check_and_correct_data(self, data, parameters):
        if len(data) == 0:
            return 0
        data_count = 0
        shortest_data_count = 0

        list_of_lengths = []
        for data_list in data:
            list_of_lengths.append(len(data_list))
        # gets the most common row length - removes any parameters where data
        # count is not equal to the mode
        mode_value = statistics.mode(list_of_lengths)
        remove_indices = []
        for d, data_list in enumerate(data):
            if len(data_list) != mode_value:
                remove_indices.append(d)
        for i in remove_indices:
            del data[i]
            del parameters[i]

        return data, parameters


@task(name="Prepare Z Score Run")
def prepare_z_score_run(parameters, start, end, chamber, window_size, z_score_limit):
    data_preparer = PrepareAlgorithmData()
    # retrieve data selected for the calculation
    all_data = data_preparer.get_data(parameters, start, end, chamber)
    # ensure all parameter datasets are of a uniform length
    checked_data, parameters = data_preparer.check_and_correct_data(all_data, parameters)
    # flip the 2D array so each column corresponds to a single parameter
    formatted_data = data_preparer.format_data(checked_data)
    # if there is no data return
    if formatted_data == None:
        return
    state = [window_size, z_score_limit]
    runner = TimeAlgorithms()
    z_parameter = Parameter.objects.get_or_create(parameter_name="Z Score",
                                                  parameter_position="None",
                                                  parameter_type="double")
    z_parameter = z_parameter[0]
    algorithm = Algorithm.objects.get(algorithm_name="z score")
    # run the algorithm handler
    runner.run_state(start, end, chamber, algorithm, z_parameter, formatted_data, state)
    return


@task(name="Prepare Algorithm")
def prepare_algorithm(list_of_parameters, chamber, start, end, sensors, algorithm, mode, skip_start, skip_end, offset_type):
    # run through the algorithm one parameter at a time
    for parameter in list_of_parameters:
        if mode == "runs":
            # get all runs in the selected chamber and timeframe
            runs_query = Run.objects.filter(chamber=chamber, start_time__gte=start,
                                             end_time__lte=end).order_by("start_time")
            runs = list(runs_query)
            del runs_query
            run_timeframes = []
            valid_runs = []

            # =================================================================================================================
            # for each run, calculate the selected time frame (run start and end +/- the skip start and skip ennd variables)
            # =================================================================================================================
            for run in runs:
                run_start = run.start_time + timedelta(seconds=skip_start)
                
                if offset_type == "start":
                    if skip_end > skip_start:
                        run_end = run.start_time + timedelta(seconds=skip_end)
                        if run_end > run.end_time :
                            run_end = run.end_time
                else:
                    run_end = run.end_time - timedelta(seconds=skip_end)
                    if run_end < run_start:
                        run_end = run_start
                if run_start < run_end :
                    timeframe = [run_start, run_end]                
                    run_timeframes.append(timeframe)
                    valid_runs.append(run)
                    
            # =================================================================================================================

            runner = RunAlgorithms()
            runner.run_state(chamber, sensors, algorithm, parameter, valid_runs, run_timeframes)

        else:
            # get all the data from the timeframe
            data_query = Data.objects.filter(time__gte=start, time__lte=end, \
                                             sensor__in=sensors, parameter_id=parameter.id).order_by("time")
            data = list(data_query)
            print("DATA COUNT: ", len(data))
            del data_query

            if(len(data) == 0):
                continue

            # sort in chronological order
            time_runner = TimeAlgorithms()
            state = []
            data = [data]
            # run the algorithm handler
            TimeAlgorithms.run_state(time_runner, start, end, chamber, algorithm, parameter, data, state)

        return