import os.path
import json
import datetime
import time
import sys
import numpy
import math
import itertools
from operator import itemgetter
from builtins import any as b_any

# BLOCK_SIZE = 20

NUM_OF_EXCLUDED_POINTS_AT_START = 0
NUM_OF_EXCLUDED_POINTS_AT_END = 0



def calculate_median(numpy_data, row_num, column, current_medians, window_size):
    window = row_num - window_size
    if window < 0:
        window = 0
    position = (row_num+1)
    values = numpy_data[window:position, column]
    median = numpy.median(values)
    current_medians.append(median)
    return current_medians


def calculate_mean(sum_of_clean_medians, num_of_clean_medians):
    calculated_means = []
    for m in range(len(sum_of_clean_medians)):
        avg = (sum_of_clean_medians[m] / num_of_clean_medians[m])
        calculated_means.append(avg)

    return calculated_means


# calculate the standard deviation
def calculate_standard_deviation(all_clean_medians):
    count = 0
    numpy_clean_medians = numpy.array(all_clean_medians)

    calculated_standard_deviations = numpy_clean_medians.std(axis=0, ddof=1)
    corrected_sds = list(calculated_standard_deviations)
    for a in range(len(corrected_sds)):
        if corrected_sds[a] == 0:
            count = count + 1

    return corrected_sds


# calculate sigmas (significances)
def calculate_sigmas(current_medians, current_means, current_standard_deviations):

    # calculate sigmas
    sum_of_sigmas_sq = 0
    number_of_sigmas = 0
    current_sigmas = []

    for m, median in enumerate(current_medians):
        mean = current_means[m]
        standard_dev = current_standard_deviations[m]
        sigma = (median - mean) / standard_dev
        current_sigmas.append(sigma)

    return current_sigmas


# calculate the z-score
def calculate_z_score(sigmas):
    # calculate z-score
    sum_of_sigmas_sq = 0
    number_of_sigmas = 0
    for sigma in sigmas:
        sum_of_sigmas_sq = sum_of_sigmas_sq + (pow(sigma, 2))
        number_of_sigmas = number_of_sigmas + 1
    # ( (sqrt | sigma_1^2 + sigma_2^2 + sigma_3^2 + .... sigma_n^2  |) / sqrt |  n  | )
    current_z_score = math.sqrt(sum_of_sigmas_sq / len(sigmas))
    return current_z_score


# load state stored in json string
def import_current_state(state, raw_data):

    state = json.loads(state)

    if len(state) == 2:
        window_size = state[0]
        z_score_limit = state[1]
        return window_size, z_score_limit

    else:
        # prepend data to the dataset
        raw_data_set = state[0] + raw_data
        medians = state[1]
        clean_medians = state[2]
        means = state[3]
        stds = state[4]
        sigmas = state[5]
        z_scores = state[6]
        sum_of_clean_medians = state[7]
        num_of_clean_medians = state[8]
        start_of_data_range = state[9][0]
        window_size = state[9][1]
        z_score_limit = state[9][2]
        return raw_data_set, medians, clean_medians, means, stds, sigmas, z_scores, \
               sum_of_clean_medians, num_of_clean_medians, start_of_data_range, window_size, z_score_limit


# populate json array of current algorithm run state
def create_state(state, raw_data, medians, clean_medians, means, stds, sigmas,z_scores,
                 sum_of_clean_medians, num_of_clean_medians, window_size, z_score_limit):
    state = json.loads(state)

    while len(state) < 10:
        state.append([])
    while len(state) > 10:
        del state[-1]

    # get the last WINDOW_SIZE number of rows from the raw data
    window = window_size
    state[0] = []
    if window < 0:
        window = 0
        state[0] = []
    elif window > len(raw_data):
        window = len(raw_data)
        state[0] = raw_data
    else:
        state[0] = raw_data[-window:]

    state[1] = medians
    state[2] = clean_medians
    state[3] = means
    state[4] = stds
    state[5] = sigmas
    state[6] = z_scores
    state[7] = sum_of_clean_medians
    state[8] = num_of_clean_medians
    state[9] = [window, window_size, z_score_limit]
    state = json.dumps(state)
    return state


# loop to manage calculations stepping through the read data row by row and returning the results (medians,
# clean medians, means, standard deviations, sigmas(significances), z-scores)
def do_z_score(data, state):
    print("z")
    start_of_data_range = 0
    window_size = 5
    z_score_limit = 6
    sum_of_clean_medians = []
    num_of_clean_medians = []
    all_avgs = []
    stds = []
    all_medians = []
    all_clean_medians = []

    clean_medians_for_export = []
    all_sigmas = []
    zscores = []

    is_first_run = True

    initial_standard_deviations = []

    numpy_data = numpy.array(data)
    first_zscore_calculation = True
    current_means=[]
    current_stds = []
    print("zz")

    # return medians, clean_medians, means, stds, sigmas, z_scores, sum_of_clean_medians, num_of_clean_medians
    current_state = import_current_state(state, data)
    if len(current_state) == 2:
        window_size = current_state[0]
        z_score_limit = current_state[1]
        # initial values for to sigma calculation
        for columns in data[0]:
            sum_of_clean_medians.append(0)
            num_of_clean_medians.append(0)
    else:
        data = current_state[0]
        all_medians = current_state[1]
        all_clean_medians = current_state[2]
        all_avgs = current_state[3]
        stds = current_state[4]
        all_sigmas = current_state[5]
        zscores = current_state[6]
        sum_of_clean_medians = current_state[7]
        num_of_clean_medians = current_state[8]

        start_of_data_range = current_state[9]
        window_size = current_state[10]
        z_score_limit = current_state[11]

        is_first_run = False
        first_zscore_calculation = False
        current_means = all_avgs[-1]
        current_stds = stds[-1]
    print("zzz")
    numpy_data = numpy.array(data)

    for r in range(start_of_data_range, len(data)) :
        current_medians = []
        current_sigmas = []
        for i in range(len(data[r])):
            # calculate median for each column
            current_medians = calculate_median(numpy_data, r, i, current_medians, window_size)
        all_medians.append(current_medians)

        if (len(current_means) > 0 and len(current_stds) > 0 and r > 1) or not is_first_run:
            current_sigmas = calculate_sigmas(current_medians, current_means, current_stds)
        else:
            initial_clean_medians = current_medians
            all_clean_medians.append(initial_clean_medians)

            for counter in range(len(current_medians)):
                current_sigmas.append(0)

        all_sigmas.append(current_sigmas)
        current_z_score = calculate_z_score(current_sigmas)
        zscores.append(current_z_score)

        if current_z_score <= z_score_limit or r < 20:
            all_clean_medians.append(current_medians)
            clean_medians_for_export.append(current_medians)
            for m, median in enumerate(current_medians):
                sum_of_clean_medians[m] = sum_of_clean_medians[m] + median
                num_of_clean_medians[m] = num_of_clean_medians[m] + 1

            current_means = calculate_mean(sum_of_clean_medians, num_of_clean_medians)
            current_stds = calculate_standard_deviation(all_clean_medians)
        else:
            clean_medians_for_export.append(clean_medians_for_export[-1])
        all_avgs.append(current_means)
        stds.append(current_stds)

        # checking progress of script
        if (r % 200) == 0:
            print("PROGRESS UPDATE - data rows processed: ", r, "/", len(data))
    print("COMPLETE: ", len(data), "/", len(data))
    # populate the json array to store as the algorithm run state
    state = create_state(state, data, all_medians, all_clean_medians, all_avgs, stds, all_sigmas,
                         zscores, sum_of_clean_medians, num_of_clean_medians, window_size, z_score_limit)

    # zscores are results
    return zscores, state


