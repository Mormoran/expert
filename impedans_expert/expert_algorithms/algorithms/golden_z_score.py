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
import ast

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

# calculate sigmas (significances)
def calculate_sigmas(current_medians, current_means, current_standard_deviations):

    # calculate sigmas
    sum_of_sigmas_sq = 0
    number_of_sigmas = 0
    current_sigmas = []
    print("Length of Means: ", len(current_means))
    print("Length of Medians: ", len(current_medians))
    print("Medians: ", current_medians)
    print("Means: ", current_means)
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

# loop to manage calculations stepping through the read data row by row and returning the results (medians,
# clean medians, means, standard deviations, sigmas(significances), z-scores)
def do_golden_z_score(data, state):
    start_of_data_range = 0
    window_size = 5
    z_score_limit = 6
    all_medians = []

    all_sigmas = []
    zscores = []

    numpy_data = numpy.array(data)
    golden_means=[]
    golden_stds = []

    # --------------------- for testing -----------------

    state = ast.literal_eval(state)
    golden_means = state[0]
    golden_stds = state[1]

    window_size = state[2][0]
    z_score_limit = state[3][0]

    # golden_means = [152.1808544,10.05850402,-74.40647404,11.59258464,0.170090008,56.95803682,20.64643004,0.075726509,18.70633034,1.926061864,0.008181948,-61.81401322,0.900175811,0.009672454,-108.8312214]
    # golden_stds = [0.521796832,0.017200143,0.249869906,0.244493674,0.003742144,0.064896708,0.271628509,0.00534551,0.098151819,0.066914801,0.000381356,0.37562692,0.012523299,6.90056E-05,1.87548908]

    # window_size = 5
    # z_score_limit = 6


    # ---------------------------------------------------

    numpy_data = numpy.array(data)
    print("Data length: ", len(data))
    print("Row Length: ", len(data[0]))
    for r in range(len(data)) : # 0-8127
        current_medians = []
        current_sigmas = []
        for i in range(len(data[r])):  # 2-54
            # calculate median for each column
            current_medians = calculate_median(numpy_data, r, i, current_medians, window_size)
        all_medians.append(current_medians)

        current_sigmas = calculate_sigmas(current_medians, golden_means, golden_stds)

        all_sigmas.append(current_sigmas)
        current_z_score = calculate_z_score(current_sigmas)
        zscores.append(current_z_score)

        # checking progress of script
        if (r % 200) == 0:
            print("PROGRESS UPDATE - data rows processed: ", r, "/", len(data))
    print("COMPLETE: ", len(data), "/", len(data))
    print("|_____RESULTS: ", zscores, " _________|")
    # zscores are results
    return zscores, state


