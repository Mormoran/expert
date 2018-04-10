from django.conf.urls import url

from django.contrib.auth.decorators import login_required

from . views import *

urlpatterns = [
    url(r'^fileupload/$', login_required(file_upload.as_view()), name='File_Upload'),
    url(r'^filelist/$', login_required(file_list.as_view()), name='File_List'),

    url(r'^file/add/$', login_required(FileUpload.as_view()), name='File_Upload-add'),
    url(r'^file/uploader/$', login_required(Uploader.as_view()), name='Uploader-add'),
]

