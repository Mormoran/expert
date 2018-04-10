from django.contrib import admin

from . models import (
    Run,
    RunParameter,
    RunProperty,
    RunValue
)

# Register your models here.
admin.site.register(Run)
admin.site.register(RunParameter)
admin.site.register(RunProperty)
admin.site.register(RunValue)