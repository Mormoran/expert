# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
	Customer,
	Chamber,
	ChamberProperty,
	SensorType,
	Sensor,
	Data,
	Marker,
	Parameter,
	Recipe,
	RecipeProperties,
	Step,
	SensorParameter
)

# admin.site.register(Customer)
#admin.site.register(Chamber)
# admin.site.register(ChamberProperties)
# admin.site.register(Runs)
# admin.site.register(RunProperties)
admin.site.register(SensorType)
# admin.site.register(Sensor)
# admin.site.register(Data)
admin.site.register(Marker)
# admin.site.register(Parameter)
# admin.site.register(Recipe)
admin.site.register(Step)
# admin.site.register(Algorithm)
# admin.site.register(AlgorithmResults)
# admin.site.register(FileUploadModel)
# admin.site.register(FileType)
# admin.site.register(DocumentUpload)


# class ChamberPropertiesInline(admin.TabularInline):
# 	model = ChamberProperties
# 	extra = 3

# class ChamberAdmin(admin.ModelAdmin):
# 	inlines = [ChamberPropertiesInline]

# admin.site.register(Chamber, ChamberAdmin)
# Register your models here.

@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'company_name',
			'contact_name',
			'user'
		)
		list_select_related = (
					'user',
				)

@admin.register(Chamber)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'chamber_name',
			'customer'
		)
		list_select_related = (
			'customer',
		)

@admin.register(ChamberProperty)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'chamber',
			'property_name',
			'property_value',
			'user_defined'
		)
		list_select_related = (
			'chamber',
		)

@admin.register(Data)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'id',
			'time',
			'sensor_parameter',
			'parameter_value'
		)
		list_select_related = (
			'sensor_parameter',
		)

@admin.register(Parameter)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'parameter_name',
			'id'
		)

@admin.register(Recipe)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'name',
			'customer',
			'id'
		)
		list_select_related = (
			'customer',
		)

@admin.register(RecipeProperties)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'recipe',
			'property_name',
			'property_value',
			'id'
		)
		list_select_related = (
			'recipe',
		)

@admin.register(Sensor)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'name',
			'chamber',
			'sensor_type',
			'serial_number',
			'id'
		)
		list_select_related = (
			'chamber',
			'sensor_type',
		)

@admin.register(SensorParameter)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'parameter_name_userdef',
			'parameter',
			'sensor',
			'live_value',
			'id'
		)
		list_select_related = (
			'parameter',
			'sensor',
		)