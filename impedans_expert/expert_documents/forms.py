from django import forms
from django.forms import ModelForm, CharField
from impedans_expert.expert_documents.models import DocumentUpload


class DocumentForm(ModelForm):
    path_to_file = forms.FileField(required=True)
    class Meta:
        model = DocumentUpload
        fields = ['path_to_file']

