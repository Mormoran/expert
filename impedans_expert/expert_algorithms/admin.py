from django.contrib import admin

from . models import (
	Algorithm,
	AlgorithmRun,
	AlgorithmRunResult,
	AlgorithmState,
	AlgorithmSettings,
	AlgorithmTimeResult,
	AlgorithmVariables,
	GoldenSet,
	StreamAlgorithm
)

# Register your models here.
# admin.site.register(Algorithm)
# admin.site.register(AlgorithmRun)
# admin.site.register(AlgorithmRunResults)
# admin.site.register(AlgorithmTimeResults)
# admin.site.register(AlgorithmState)
# admin.site.register(GoldenSet)
# admin.site.register(AlgorithmConfiguration)


@admin.register(Algorithm)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm_name',
			'algorithm_src',
			'algorithm_description',
            'id'
		)

@admin.register(AlgorithmRun)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm',
			'customer',
			'date_time',
            'result_parameter',
            'id'
		)
		list_select_related = (
            'algorithm',
            'customer',
            'result_parameter',
        )

@admin.register(AlgorithmRunResult)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'run',
			'algorithm_run',
			'parameter',
            'value',
            'id'
		)
		list_select_related = (
            'run',
			'algorithm_run',
			'parameter',
        )

@admin.register(AlgorithmState)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm_run',
            'id'
		)
		list_select_related = (
			'algorithm_run',
        )

@admin.register(AlgorithmSettings)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'stream_algorithm',
			'parameter',
            'date_time',
			'recipe',
			'active',
			'start',
			'stop'
		)
		list_select_related = (
			'stream_algorithm',
			'parameter',
            'recipe',
        )

@admin.register(AlgorithmTimeResult)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm_run',
			'parameter',
            'value',
            'start_time',
            'end_time',
            'chamber',
            'id'
		)
		list_select_related = (
			'algorithm_run',
        )

@admin.register(AlgorithmVariables)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm_settings',
			'chamber',
            'date_time',
            'active',
            'ready',
            'id'
		)
		list_select_related = (
			'algorithm_settings',
            'chamber',
        )

@admin.register(GoldenSet)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'chamber',
			'step',
            'id'
		)
		list_select_related = (
			'chamber',
            'step',
        )

@admin.register(StreamAlgorithm)
class ProductAdmin(admin.ModelAdmin):
		list_display = (
			'algorithm_name',
			'algorithm_description',
            'id'
		)