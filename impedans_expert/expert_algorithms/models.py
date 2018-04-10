import uuid

from datetime import datetime
from django.db import models

from impedans_expert.expert.models import Customer, Parameter, Chamber, Step, OwnedModel, Recipe

from impedans_expert.expert_import.models import Run

# Create your models here.

class Algorithm(models.Model):
    algorithm_name          = models.CharField(max_length=50)
    algorithm_src           = models.CharField(max_length=50)
    algorithm_description   = models.CharField(max_length=100)

    def __str__(self):
        return self.algorithm_name

    class Meta:
        unique_together=(('algorithm_name', 'algorithm_src'),)

class StreamAlgorithm(models.Model):
    algorithm_name          = models.CharField(max_length=50, unique=True)
    algorithm_description   = models.CharField(max_length=100)

    def __str__(self):
        return self.algorithm_name

    class Meta:
        unique_together=(('algorithm_name',),)

class AlgorithmRun(models.Model):
    algorithm           = models.ForeignKey(Algorithm)
    customer            = models.ForeignKey(Customer)
    date_time           = models.DateTimeField(auto_now_add=True)
    result_parameter    = models.ForeignKey(Parameter, default=None, blank=True, null=True)

    def __str__(self):
        if self.result_parameter != None:
            run_string = self.algorithm.algorithm_name + ": " + \
                         self.date_time.strftime("%d/%m/%Y %H:%M:%S") + \
                         self.result_parameter.parameter_name
        else:
            run_string = self.algorithm.algorithm_name + ": " + \
                         self.date_time.strftime("%d/%m/%Y %H:%M:%S")

        return run_string

    class Meta:
        unique_together=(('algorithm', 'customer', 'date_time'),)

class AlgorithmRunResult(models.Model):
    run             = models.ForeignKey(Run, default=None, on_delete=models.CASCADE)
    algorithm_run   = models.ForeignKey(AlgorithmRun)
    parameter       = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value           = models.FloatField()

    def __str__(self):
        result_string = self.parameter.parameter_name + ": " + str(self.value)
        return result_string

    class Meta:
        unique_together=(('algorithm_run', 'parameter', 'value'),)


class AlgorithmTimeResult(models.Model):
    algorithm_run   = models.ForeignKey(AlgorithmRun)
    parameter       = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value           = models.FloatField()
    start_time      = models.DateTimeField()
    end_time        = models.DateTimeField()
    chamber         = models.ForeignKey(Chamber, on_delete=models.CASCADE)

    def __str__(self):
        result_string = self.parameter.parameter_name + ": " + str(self.value)
        return result_string

    class Meta:
        unique_together=(('algorithm_run', 'parameter', 'chamber', 'start_time', 'end_time'),)

class AlgorithmState(models.Model):
    algorithm_run   = models.ForeignKey(AlgorithmRun)
    state           = models.TextField()

class AlgorithmSettings(models.Model):
    active                  = models.BooleanField(default=True)
    stream_algorithm        = models.ForeignKey(StreamAlgorithm, on_delete=models.CASCADE)
    configuration_thread    = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    date_time               = models.DateTimeField(default=datetime.now)
    parameter               = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    recipe                  = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    result_name             = models.CharField(max_length=255)
    start                   = models.IntegerField()
    stop                    = models.IntegerField()

    def __str__(self):
        result_string = self.stream_algorithm.algorithm_name + "(" + str(self.start) + "-" + str(self.stop) + ")" + " on (" + str(self.date_time) + ")"
        return result_string

class AlgorithmVariables(models.Model):
    # This is a baseline model.
    active                  = models.BooleanField(default=True)
    algorithm_config_setup  = models.CharField(max_length=500)
    algorithm_configuration = models.CharField(max_length=500)
    algorithm_settings      = models.ForeignKey(AlgorithmSettings, on_delete=models.CASCADE)
    chamber                 = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    date_time               = models.DateTimeField(default=datetime.now)
    ready                   = models.BooleanField(default=False)

    def __str__(self):
        result_string = self.chamber.chamber_name + " on (" + str(self.date_time) + ")"
        return result_string

class GoldenSet(models.Model):
    data    = models.TextField()
    step    = models.ForeignKey(Step)
    chamber = models.ForeignKey(Chamber)

    class Meta:
        unique_together=(('step', 'chamber'),)