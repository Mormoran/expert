from django.contrib import admin

from . models import FileUploadModel, FileType

# Register your models here.
admin.site.register(FileUploadModel)
admin.site.register(FileType)



