from django.conf.urls import url

from . views import *

urlpatterns = [
    url(r'^document/add/$', DocumentUpload.as_view(), name='Document_Upload-add'),
    url(r'^documents/$', documents, name='Documents'),
    url(r'^document/(?P<document_id>[0-9]+)/$', document_download, name='Documentdownload'),
]
