from django.db import models
from impedans_expert.users.models import User
from impedans_expert.expert.models import *
from filer.models import File as FilerFile

# Create your models here.

class DocumentUpload(FilerFile):
    # name = models.CharField(max_length=256)
    # path_to_file = models.FileField(upload_to='documents/')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    report = models.BooleanField(default=False)

    def __str__(self):
        return self.name


