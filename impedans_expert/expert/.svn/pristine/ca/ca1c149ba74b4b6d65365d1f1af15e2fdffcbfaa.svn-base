# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from django.core.urlresolvers import reverse
from impedans_expert.users.models import User
# from impedans_expert.expert_import.models import (
#     Run,
#     RunProperty
# )

class Customer(models.Model):
    company_name    = models.CharField(max_length=100)
    contact_name    = models.CharField(max_length=100)
    contact_email   = models.CharField(max_length=100)
    user            = models.ForeignKey(User)

    @staticmethod
    def get_absolute_url():
        return reverse('details')

    def __str__(self):
        return self.company_name + ', ' + self.contact_name + ' (' + self.contact_email + ')'

    class Meta:
        unique_together=(('contact_email','user'),)

class OwnedModel(models.Model):
    owner = models.ForeignKey(User)

    class Meta:
        abstract = True

class Chamber(models.Model):
    chamber_name    = models.CharField(max_length=100)
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE)

    @staticmethod
    def get_absolute_url():
        return reverse('details')

    def __str__(self):
        return self.chamber_name

    def __key(self):
        return self.chamber_name, self.customer.id

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('chamber_name', 'customer'),)

class ChamberProperty(models.Model):
    chamber         = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    property_name   = models.CharField(max_length=50)
    property_value  = models.CharField(max_length=100)
    user_defined    = models.BooleanField(default=True)

    def __str__(self):
        return self.property_name + ' = ' + self.property_value

    def __key(self):
        return self.chamber, self.property_name

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('property_name','property_value', 'chamber'),)


class Marker(models.Model):
    time            = models.DateTimeField()
    chamber         = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    marker_name     = models.CharField(max_length=20)
    marker_string   = models.CharField(max_length=50)

    def __str__(self):
        return str(self.time) + ': ' + self.marker_name + ' = ' + self.marker_string

    def __key(self):
        return self.chamber, self.time, self.marker_name

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('time','marker_name', 'chamber'),)


class Recipe(models.Model):
    name        = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    customer    = models.ForeignKey(Customer)

    def __str__(self):
        return str(self.name)

    class Meta:
        unique_together=(('name','customer'),)
    
class RecipeProperties(models.Model):
    recipe          = models.ForeignKey(Recipe)
    property_name   = models.CharField(max_length=255)
    property_value  = models.CharField(max_length=255)

    def __str__(self):
        return str(self.property_name)

    class Meta:
        unique_together=(('recipe','property_name'),)

class Step(models.Model):
    recipe      = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_number = models.IntegerField()    # models.IntegerRangeField()

    def __str__(self):
        return str(self.recipe.name + " Step: " + str(self.step_number))

    class Meta:
        unique_together=(('recipe','step_number'),)


class SensorType(models.Model):
    sensor_type = models.CharField(max_length=256)

    def __str__(self):
        return self.sensor_type

    class Meta:
        unique_together=(('sensor_type'),)


class Sensor(models.Model):
    active          = models.BooleanField(default=True)
    chamber         = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    name            = models.CharField(max_length=50, null=False, blank=True)
    serial_number   = models.CharField(max_length=50)
    sensor_type     = models.ForeignKey(SensorType)

    @staticmethod
    def get_absolute_url():
        return reverse('sensor_list')

    def __str__(self):
        return self.serial_number + ' : ' + str(self.chamber_id)

    def __key(self):
        return self.chamber.id, self.serial_number

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('serial_number','chamber'),)


class Parameter(models.Model):
    parameter_name          = models.CharField(max_length=50)
    parameter_type          = models.CharField(max_length=30, default='double')
    parameter_unit          = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.parameter_name


class SensorParameter(models.Model):
    sensor                  = models.ForeignKey(Sensor)
    parameter               = models.ForeignKey(Parameter)
    parameter_name_userdef  = models.CharField(max_length=100, blank=False, default="Parameter")
    live_value              = models.FloatField(null=True)

    # def save(self, *args, **kwargs):
    #     default_string = str(self.sensor.name + " - " + self.parameter.parameter_name)
    #     self.parameter_name_userdef = default_string
    #     super(SensorParameter, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sensor.name) + ' - ' + str(self.parameter)

    def __key(self):
        return self.sensor.id, self.parameter.id

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())

    class Meta:
        unique_together=(('sensor','parameter'),)


class Data(models.Model):
    time                = models.DateTimeField(db_index=True)
    sensor_parameter    = models.ForeignKey(SensorParameter, on_delete=models.CASCADE)
    parameter_value     = models.FloatField()

    def __str__(self):
        return str(self.time) + ' : ' + self.sensor_parameter.parameter_name_userdef + ' = ' + str(self.parameter_value)

    def __key(self):
        return self.time, self.sensor_parameter

    def __eq__(self, y):
        return isinstance(y, self.__class__) and self.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())