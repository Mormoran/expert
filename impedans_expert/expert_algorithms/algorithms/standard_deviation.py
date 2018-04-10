#Every algorithm must return a result and state

# The state is the list of values needed for a continuation of the current run
# where the algorithm must use values previously generated in the last
# iteration to make decisions on what needs to be calculated next

# if the current algorithm has no need for a state, just return a placeholder
# to conform with the standard, e.g. []

import numpy

def do_standard_deviation(data, state):

    numpy_data = numpy.array(data)
    calculated_standard_deviation = numpy_data.std(ddof=1)
    print("Std: ", calculated_standard_deviation)
    results = [calculated_standard_deviation]
    return results,state