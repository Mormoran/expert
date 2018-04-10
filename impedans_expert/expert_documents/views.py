import os
import os.path
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.views.generic.edit import CreateView

from django.contrib.auth.models import User

from impedans_expert.expert.models import *
from impedans_expert.expert_documents.models import DocumentUpload as DocumentUploadModel
from impedans_expert.expert_documents.forms import *


# Create your views here.
def documents(request):
    current_user = User.objects.get(username=request.user.username)
    cust = Customer.objects.get(user_id=current_user.id)

    documents_list = DocumentUploadModel.objects.filter(customer=cust)
    all_documents_objects = []
    for docs in documents_list:
        documents_object = {}
        documents_object['id']=docs.pk
        documents_object['name']=docs.name
        documents_object['report']=docs.report
        all_documents_objects.append(documents_object)

    return JsonResponse(all_documents_objects, safe=False)

# download documents
def document_download(request, document_id) :
    current_user = User.objects.get(username=request.user.username)
    cust = Customer.objects.get(user_id=current_user.id)
    if 0 == 0:
        doc = DocumentUploadModel.objects.get(pk=document_id)
        if doc.customer == cust :
            dir1 = doc.url
            dir_list = dir1.split("/files/")
            file_name = dir_list[1]
            file_dir = os.path.join(settings.FILES_ROOT, file_name)
            file = open(file_dir, 'rb')
            response = HttpResponse(content=file)
            response['Content-Type']= 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename=%s' % (os.path.basename(doc.url))

            return response
        else :
            return Http404
    # except:
    #     return Http404


class DocumentUpload(CreateView) :

    def get(self, request) :
        current_user = User.objects.get(username=request.user.username)
        cust = Customer.objects.get(user_id=current_user.id)
        reports = DocumentUploadModel.objects.filter(report=True, customer=cust)
        documents = DocumentUploadModel.objects.filter(report=False, customer=cust)
        document_form = DocumentForm()
        return render(request, 'expert_documents/document_upload_form.html', {'reports':reports,'documents':documents,'form':document_form})

    def post(self, request, *args, **kwargs) :
        document_form = DocumentForm(request.POST, request.FILES)
        if request.user.is_authenticated:
            if document_form.is_valid():
                path_to_file = request.FILES['path_to_file']
                name = path_to_file.name
                current_user = User.objects.get(username=request.user.username)
                customer = Customer.objects.get(user_id=current_user.id)
                user = request.user
                if user.is_superuser :
                    report = True
                else:
                    report = False
                doc = DocumentUploadModel.objects.create(file=path_to_file, name=name, customer=customer, report=report)
            else:
                print(document_form.errors)
        return redirect('expert_documents:Document_Upload-add')

