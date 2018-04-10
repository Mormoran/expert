from .mean import do_mean
from .z_score import do_z_score
from .standard_deviation import do_standard_deviation
from .golden_z_score_by_mean import do_golden_z_score_by_mean
from .golden_z_score_by_median import do_golden_z_score_by_median
from .golden_z_score import do_golden_z_score
from .training_z import do_training

algorithms = {
    'mean' : do_mean,
    'standard deviation' : do_standard_deviation,
    'z score' : do_z_score,
    'golden z score by mean' : do_golden_z_score_by_mean,
    'golden z score by median' : do_golden_z_score_by_median,
    'golden running z score' : do_golden_z_score,
    'training z' : do_training,
}

def dummy_algorithm(self, data, state):
    """This method will be run if no function has been selected."""
    result = 0
    return result, state


class Algorithm(object):
    """Algorithm instance holds pointer to selected algorithm function."""
    def __init__(self, name="") :
        if name in algorithms :
            self.func = algorithms[name]
            self.name = name
        else:
            self.func = dummy_algorithm
            self.name = "None"

    def __str__(self):
        return self.name

    def run(self, data, state):
        return self.func(data, state)
