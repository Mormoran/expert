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

def calculate_median(numpy_data, column, current_medians):
    position = numpy_data.shape[0]
    # position = position -1
    values = numpy_data[0:position, column]
    median = numpy.median(values)
    current_medians.append(median)
    return current_medians

# calculate sigmas (significances)
def calculate_sigmas(current_medians, golden_means, golden_standard_deviations):

    # calculate sigmas
    sum_of_sigmas_sq = 0
    number_of_sigmas = 0
    current_sigmas = []

    for m, median in enumerate(current_medians):
        golden_mean = golden_means[m]
        standard_dev = golden_standard_deviations[m]
        sigma = (median - golden_mean) / standard_dev
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
def do_golden_z_score_by_median(data, state):
    start_of_data_range = 0
    window_size = 5
    z_score_limit = 6
    medians = []
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

    # golden_means = [151.9135535, 10.04936584, -74.34460961, 11.58608595, 0.169966754, 56.96622528, 20.62634432, 0.075679931, 18.73061274, 1.934094398, 0.008220614, -61.76730832, 0.898653055,  0.009658092, -108.4218929]
    # golden_stds = [6.122918989, 0.259747282, 1.367252585, 0.370862749, 0.005952895, 0.092189351, 0.770968675, 0.005831592, 0.376096839, 0.096162035,  0.000473808, 0.47689836, 0.044179935, 0.00043524, 6.657979027]
    # window_size = 5
    # z_score_limit = 6


    # ---------------------------------------------------

    for i in range(len(golden_means)):
        medians.append(0)

    numpy_data = numpy.array(data)

    current_sigmas = []
    # for r in range(len(data)):  # 2-54
    current_medians = []
        # calculate median for each column
    for i in range(len(data[0])):
        current_medians = calculate_median(numpy_data, i, current_medians)

    current_sigmas = calculate_sigmas(current_medians, golden_means, golden_stds)

    all_sigmas.append(current_sigmas)
    current_z_score = calculate_z_score(current_sigmas)
    zscores.append(current_z_score)
    print("|_____RESULTS: ", zscores, " _________|")

    # zscores are results
    return zscores, state

