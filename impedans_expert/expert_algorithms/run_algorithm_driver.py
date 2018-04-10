#runs algorithms based on data selected by chamber run

import os
import json
from datetime import datetime

from django.conf import settings
from django.db.models import Avg, StdDev

from impedans_expert.expert.models import Chamber, Parameter, Data
from impedans_expert.expert_import.models import Run
from . models import Algorithm, AlgorithmRun, AlgorithmRunResult, AlgorithmState
from impedans_expert.expert_algorithms.algorithms.algorithm import Algorithm

class State():
    def __init__(self, algorithm, last_state):
        self.algorithm = algorithm
        self.current_state = last_state


class RunAlgorithms():
    def run_state(self, chamber, sensors, algorithm, parameter, runs, run_timeframes):
        results = []
        state = State("", "")
        states = []
        valid_runs = []
        run_start_time = datetime.now()

        state_data = [state.current_state]


        for r, run in enumerate(runs):
            print("Run " + str(r) + " : " + str(run_timeframes[r][0]) + " : " + str(run_timeframes[r][1] - run_timeframes[r][0]))
            # Check for built-in database algorithms
            if algorithm.algorithm_name == "mean" :
                result = Data.objects.filter(time__gte=run_timeframes[r][0], time__lte=run_timeframes[r][1], \
                                             sensor__in=sensors, parameter_id=parameter.id).aggregate(average=Avg('parameter_value'))
                # mean function does not keep state
                values = []
                values.append(result['average'])
                results.append(values)
                valid_runs.append(run)
                print("MEAN: ", result['average'])

            elif algorithm.algorithm_name == "standard deviation" :
                result = Data.objects.filter(time__gte=run_timeframes[r][0], time__lte=run_timeframes[r][1], \
                                             sensor__in=sensors, parameter_id=parameter.id).aggregate(std=StdDev('parameter_value'))
                # mean function does not keep state
                values = []
                values.append(result['std'])
                results.append(values)
                valid_runs.append(run)
                print("STD: ", result['std'])

            else :
                # extract the parameter values from the data list
                data_query = Data.objects.filter(time__gte=run_timeframes[r][0], time__lte=run_timeframes[r][1], \
                                                 sensor__in=sensors, parameter_id=parameter.id).order_by("time")
                data = list(data_query)
                del data_query

                run_data = [data]
                del data
                # if the run contains any data
                if len(run_data) > 0 and len(run_data[0]) > 0:
                    valid_runs.append(run)
                    data_values = []
                    for row in run_data:
                        row_values = [value.parameter_value for value in row]
                        data_values.append(row_values)
                    # get the algorithm runner
                    runner = Algorithm(algorithm.algorithm_name)
                    # run the algorithm
                    value = runner.run(data_values, state_data)

                    del data_values

                    states.append(value)
                    state_data = [value]
                    results.append(value[0])

        if parameter.parameter_name != "Z Score":
            name_part_1 = parameter.parameter_name
            name_part_2 = algorithm.algorithm_name
            algorithm_parameter_name = name_part_1 + " " + name_part_2
            algorithm_parameter = Parameter.objects.get_or_create(parameter_name=algorithm_parameter_name, \
                                                                  parameter_position=parameter.parameter_position, \
                                                                  parameter_type=parameter.parameter_type)
            parameter = algorithm_parameter[0]
        # add algorithm run data to the database
        created_algorithm_run = AlgorithmRun.objects.get_or_create(customer=chamber.customer, \
                                                                   algorithm=algorithm, \
                                                                   date_time=run_start_time)
        algorithm_run = created_algorithm_run[0]
        algorithm_run.result_parameter=parameter
        algorithm_run.save(update_fields=(["result_parameter"]))
        run_results = []
        print("Algorithm Instance: ", algorithm_run)        
        for r, result_list in enumerate(results):            
            for result in result_list:
                run_results.append(AlgorithmRunResult(runs=valid_runs[r], algorithm_run= \
                                                       algorithm_run, parameter=parameter, \
                                                       value=result))
        AlgorithmRunResult.objects.bulk_create(run_results)
        for s, state in enumerate(states):
           AlgorithmState.objects.create(algorithm_run=algorithm_run, \
                                         state=state)
        return
