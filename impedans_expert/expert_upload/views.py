import os
import shutil
import json

from io import StringIO
from os.path import join

from django.core import serializers
from django.conf import settings
from django.forms import formset_factory
from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.generic.edit import CreateView, View
from django.views.generic import ListView

from django_fine_uploader.views import FineUploaderView
from django_fine_uploader.forms import FineUploaderUploadForm
from django_fine_uploader import urls as uploader_urls
from django_fine_uploader.fineuploader import ChunkedFineUploader
from filer.fields.multistorage_file import MultiStorageFileField

from impedans_expert.expert.models import *
from impedans_expert.expert.forms import *
from impedans_expert.users.models import User

from . models import FileType, FileUploadModel as UploadedFile

CHAMBER = None

class file_upload(CreateView):
    model = UploadedFile
    fields = ['file']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = User.objects.get(username=request.user)
        new_file = request.FILES['file']
        new_filename = request.POST.get("filename")
        UploadedFile.objects.create(file=new_file, name=new_file.name, owner=user, attribute='at')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('File_Upload')

class file_list(ListView):
    model = UploadedFile


class FileUpload(CreateView):
    properties_form_set = formset_factory(ChamberPropertiesForm)
    # load the file uploader page -> get the user's chambers and provide the information
    # necessary to create a fineuploader instance for each chamber
    def get(self, request):
        chamber_form = ChamberForm()
        user = User.objects.get(username=request.user)
        properties_formset = self.properties_form_set()
        file_upload_form = UploadedFile(owner=user)
        #file_upload_form.fields = ['file_type', 'sensor']
        return render(request, 'expert_upload/file_upload_form.html',{'chamber_form': chamber_form, 'properties_formset': properties_formset, 'file_upload_form': file_upload_form})

    # handle the uploading of data files from each chamber
    def post(self, request, *args, **kwargs):
        chamber_form = ChamberForm(request.POST)
        properties_formset = self.properties_form_set(request.POST)
        # authenticate user
        if request.user.is_authenticated:
            # create a chamber instance for the user
            if chamber_form.is_valid() and properties_formset.is_valid():
                chamber_name = request.POST['chamber_name']
                current_user = User.objects.get(username=request.user.username)
                customer = Customer.objects.get(user_id=current_user.id)
                chamber = Chamber.objects.create(chamber_name=chamber_name, customer=customer)
                # create the chamber properties entered associated with the new chamber
                for f in properties_formset:
                    p_form = f.cleaned_data
                    property_name = p_form.get('property_name')
                    property_value = p_form.get('property_value')
                    if property_name != None and property_value != None :
                        chamber_property = ChamberProperties.objects.create(property_name=property_name,
                                                                            property_value=property_value, chamber=chamber)
                chamber = serializers.serialize("json", [chamber])
                return JsonResponse(chamber, safe=False)


class Chunking(ChunkedFineUploader):

    def __init__(self, form, concurrent=True, *args, **kwargs):
        data = form.cleaned_data
        super(ChunkedFineUploader, self).__init__(data, *args, **kwargs)
        data = form.cleaned_data
        self.concurrent = concurrent
        self.total_parts = data.get('qqtotalparts')
        self.part_index = data.get('qqpartindex')
        self.chamber = data.get('chamber')
        self.customer = None
        self.file_size = None
        self.file_name = None
        if self.chamber == None:
            self.chamber = form.data['chamber']
            self.chamber = Chamber.objects.get(id=self.chamber)

    def add_file_parameters(self, chamber, customer, file_name):
        # self.chamber = chamber
        self.customer = customer
        # self.file_size = file_size
        self.file_name = file_name

    def combine_chunks(self):
        """Combine a chunked file into a whole file again. Goes through each part,
        in order, and appends that part's bytes to another destination file.
        Discover where the chunks are stored in settings.CHUNKS_DIR
        Discover where the uploads are saved in settings.UPLOAD_DIR
        """
        # So you can see I'm saving a empty file here. That way I'm able to
        # take advantage of django.core.files.storage.Storage.save (and
        # hopefully any other custom Django storage). In a nutshell the
        # ``final_file`` will get a valid name
        # django.core.files.storage.Storage.get_valid_name
        # and I don't need to create some dirs along the way to open / create
        # my ``final_file`` and write my chunks on it.
        # https://docs.djangoproject.com/en/dev/ref/files/storage/#django.core.files.storage.Storage.save
        # In my experience with, for example, custom AmazonS3 storages, they
        # implement the same behaviour.

        this_file = InMemoryUploadedFile(StringIO(""), 'file', self.file_name, None, StringIO("").tell(), None)
        for i in range(self.total_parts):
            part = join(self.chunks_path, str(i))
            with self.storage.open(part, 'rb') as source:
                this_file.write(source.read().decode('utf-8'))
        shutil.rmtree(self._abs_chunks_path)
        # full_file_path = join(settings.FILES_ROOT, self.real_path)
        if self.file_name.endswith(".dat"):
            file_type = FileType.objects.get(name="Octiv", customer=self.customer)
            fileModel = UploadedFile.objects.create(file=this_file, name=self.file_name, customer=self.customer, \
                                                    chamber=self.chamber, parsed=False, file_type=file_type)
        else:
            fileModel = UploadedFile.objects.create(file=this_file, name=self.file_name, customer=self.customer, \
                                                    chamber=self.chamber, parsed=False)

    def save(self):
        is_file_chunked = isinstance( self.total_parts, int )
        if not is_file_chunked:
            self.total_parts = 1
        if self.chunked:
            chunk = self._save_chunk()
            # If ``concurrent=True`` the method self.is_time_to_combine_chunks
            # cannot return an accurate answer, therefore you must call
            # combine_chunks() manually
            if not self.concurrent and self.is_time_to_combine_chunks:
                self.combine_chunks()
                return self.real_path
            print("2b||!2b")
            return chunk
        else:
            # self.real_path = self.storage.save(self._full_file_path, self.file)
            if self.file_name.endswith(".dat"):
                file_type = FileType.objects.get(name="Octiv", customer=self.customer)
                fileModel = UploadedFile.objects.create(file=self.file, name=self.file_name, customer=self.customer, \
                                                        chamber=self.chamber, parsed=False, file_type=file_type)
            else:
                fileModel = UploadedFile.objects.create(file=self.file, name=self.file_name, customer=self.customer, \
                                                        chamber=self.chamber, parsed=False)
            self.real_path = fileModel.file
            return self.real_path


class Uploader(FineUploaderView) :

    # Based off of https://github.com/douglasmiranda/django-fine-uploader/blob/master/django_fine_uploader/fineuploader.py
    # and https://github.com/douglasmiranda/django-fine-uploader/blob/master/django_fine_uploader/views.py

    form_class_upload = FineUploaderForm
    file_name = None
    #file_size = None
    chamber = None
    customer = None
    total_parts = None
    part_index = None

    def form_invalid(self, form) :
        print("FORM IS INVALID")

    def form_valid(self, form):
        current_user = User.objects.get(username=self.request.user.username)
        self.customer = Customer.objects.get(user_id=current_user.id)
        try:
            self.chamber = form.cleaned_data['chamber']
        except:
            #try:
            #self.chamber = form.data['chamber']
            #self.chamber = Chamber.objects.get(id=self.chamber)
            #except:
            pass

        self.file_name = form.cleaned_data['qqfilename']
        # file = self.request.FILES['qqfile']  # form.cleaned_data['qqfile']
        self.file_size = form.cleaned_data['qqtotalfilesize']
        # file_folder = form.cleaned_data['qquuid']
        # file_dir = os.path.join('uploads', file_folder, file_name)
        # fileModel = UploadedFile.objects.create(file=file, _file_size=self.file_size, name=self.file_name, customer=self.customer, chamber=self.chamber, parsed=False)
        self.process_upload(form)

        return self.make_response({'success': True})

    def process_upload(self, form):
        self.upload = Chunking(form, self.concurrent)
        self.upload.add_file_parameters(self.chamber, self.customer, self.file_name)
        file_path = None
        if self.upload.concurrent and self.chunks_done:
            print("COMBINE_CHUNKS")
            self.upload.combine_chunks()
        else:
            print("SAVING")
            self.upload.save()

