#Every algorithm must return a result and state

# The state is the list of values needed for a continuation of the current run
# where the algorithm must use values previously generated in the last
# iteration to make decisions on what needs to be calculated next

# if the current algorithm has no need for a state, just return a placeholder 
# to conform with the standard, e.g. []

def do_mean(data, state):
    sum_of_data = sum(dat for dat in data[0])
    mean = sum_of_data/len(data[0])
    results = []
    results.append(mean)
    print("MEAN: ", mean)
    return results,state
