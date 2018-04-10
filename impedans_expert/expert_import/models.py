from django.db import models
from filer.models import File as FilerFile

from impedans_expert.expert.models import (
    Chamber,
    Recipe,
    OwnedModel
)

from impedans_expert.expert.models import (
    Chamber,
    Parameter
)

from impedans_expert.expert_upload.models import (
    FileType,
    FileUploadModel
)

# from impedans_expert.expert_algorithms.models import AlgorithmConfiguration

class Run(models.Model):
    start_time      = models.DateTimeField(db_index=True)
    end_time        = models.DateTimeField(db_index=True)
    chamber         = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    recipe          = models.ForeignKey(Recipe, default=None, blank=True, null=True)    

    def __str__(self):
        return "Start: " + str(self.start_time) + ' (Duration: ' + str(self.end_time - self.start_time) + ')'

    def __key(self):
        return self.chamber, self.start_time,  self.end_time

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('start_time', 'end_time', 'chamber'),)

class RunParameter(models.Model):
    parameter               = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    chamber                 = models.ForeignKey(Chamber)
    param_name_user_defined = models.BooleanField(default=True)

    def __str__(self):
        return self.parameter.parameter_name + " in chamber: " + self.chamber.chamber_name

    def __key(self):
        return self.parameter, self.chamber

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('parameter','chamber'),)

class RunProperty(models.Model):
    run             = models.ForeignKey(Run)
    property_name   = models.CharField(max_length=20)
    property_value  = models.CharField(max_length=50)
    user_defined    = models.BooleanField(default=True)

    def __str__(self):
        return self.property_name + ': ' + self.property_value

    def __key(self):
        return self.run, self.property_name

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('property_name','run'),)

class RunValue(models.Model):
    run                     = models.ForeignKey(Run, on_delete=models.CASCADE)
    run_parameter           = models.ForeignKey(RunParameter, on_delete=models.CASCADE)
    # configuration           = models.ForeignKey(RunValueConfiguration, null=True)
    value                   = models.IntegerField()
    user_defined            = models.BooleanField(default=True)

    def __str__(self):
        return str(self.run_parameter.parameter.parameter_name) + " - Value: " + str(self.value)

    def __key(self):
        return self.run, self.value

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('run','run_parameter'),)

class RunValueConfiguration(models.Model):
    algorithm_string = models.CharField(max_length=255)

    def __str__(self):
        return self.algorithm_string