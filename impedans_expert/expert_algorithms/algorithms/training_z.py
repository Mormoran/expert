import numpy

#calculate the mean for each parameter passed selected (column by column)
def calculate_mean(data):
    print("Calculating Mean")
    numpy_data = numpy.array(data)
    calculated_means = numpy_data.mean(axis=0)
    means = list(calculated_means)
    print("Mean Calculated")

    return means


# calculate the standard deviation for each parameter selected (column by column)
def calculate_standard_deviation(data):
    numpy_data = numpy.array(data)
    calculated_stds = numpy_data.std(axis=0, ddof=1)
    print("STDs: ", calculated_stds)
    stds = list(calculated_stds)

    return stds

#call functions, create container for the results and return them
def do_training(data, state):
    mean = calculate_mean(data)
    std = calculate_standard_deviation(data)
    results = [mean, std]
    print("RESULTS: ", results)
    return results, state
