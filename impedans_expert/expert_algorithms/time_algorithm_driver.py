#runs algorithms based on time selected data in a chamber

import os
import json
from datetime import datetime

from django.conf import settings
from impedans_expert.expert.models import Chamber, Parameter, Data
from . models import Algorithm, AlgorithmRun, AlgorithmTimeResult, AlgorithmState
from impedans_expert.expert_algorithms.algorithms.algorithm import Algorithm as AlgorithmRunner

class State():
    def __init__(self, algorithm, last_state):
        self.algorithm = algorithm
        self.current_state = last_state


class TimeAlgorithms():
    def run_state(self, start, end, chamber, algorithm, parameter, data, state):
        results = []
        valid_runs = []
        run_start_time = datetime.now()
        state_data = json.dumps(state)
        if len(data) > 0:
            AlgorithmRun.objects.create(algorithm=algorithm, customer=chamber.customer)
            data_values = []
            for row in data:
                row_values = [value.parameter_value for value in row]
                data_values.append(row_values)

            # get the algorithm runner
            runner = AlgorithmRunner(algorithm.algorithm_name)
            # run the algorithm
            values = runner.run(data_values, state_data)

            # del data_values

            current_state = values[1]
            # to timestamp results - a = get number of results
            # b = get number of entered data points
            # b/a = interval of results
            iter_size = int(len(data)/len(values[0]))
            counter = 0
            result_times = []
            while counter < len(data):
                result_times.append(data[counter][0].time)
                counter = counter + iter_size
            if  iter_size != 1:
                result_times.append(data[-1][0].time)
            del data
            # get run instance and add the results and state to the database
            created_algorithm_run = AlgorithmRun.objects.get(customer=chamber.customer, \
                                                             algorithm=algorithm, \
                                                             date_time__gte=run_start_time)
            print("PARAMETER: ", parameter)
            if not "train" in algorithm.algorithm_name:
                if parameter.parameter_name != "Z Score":
                    name_part_1 = parameter.parameter_name
                    name_part_2 = algorithm.algorithm_name
                    algorithm_parameter_name = name_part_1 + " " + name_part_2
                    algorithm_parameter = Parameter.objects.get_or_create(parameter_name=algorithm_parameter_name, \
                                                                          parameter_position=parameter.parameter_position, \
                                                                          parameter_type=parameter.parameter_type)
                    parameter = algorithm_parameter[0]

                # for every results returned by the run
                if iter_size == 1:
                    created_algorithm_run.result_parameter = parameter
                    created_algorithm_run.save(update_fields=(["result_parameter"]))

                    for v, value in enumerate(values[0]):
                        AlgorithmTimeResult.objects.create(algorithm_run=created_algorithm_run, parameter= \
                                                            parameter, value=value, \
                                                            start_time=result_times[v], \
                                                            end_time=result_times[v], \
                                                            chamber=chamber)
                else:
                    for v, value in enumerate(values[0]):
                        AlgorithmTimeResult.objects.create(algorithm_run=created_algorithm_run, parameter= \
                                                            parameter, value=value, \
                                                            start_time=result_times[v], \
                                                            end_time=result_times[(v+1)], \
                                                            chamber=chamber)
                # every run should only have one related state
                AlgorithmState.objects.create(algorithm_run=created_algorithm_run,
                                              state=current_state)
                return None
            else:
                return values[0]
