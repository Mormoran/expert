from django.db import models
from filer.models import File as FilerFile
from impedans_expert.expert.models import (
    Chamber,
    Customer,
    Sensor
)


class FileType(models.Model):
    name = models.CharField(max_length=50, default="Octiv")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    options = models.CharField(max_length=1000)
    parser_config = models.FileField(upload_to='config/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together=(('name', 'customer'),('customer','parser_config'),)


class FileUploadModel(FilerFile):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    file_type = models.ForeignKey(FileType, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    chamber = models.ForeignKey(Chamber, on_delete=models.SET_NULL, null=True)
    parsed = models.BooleanField(default=False)
    # inherited parameters:
    # icon, folder, owner, sha1, filename, original_filename, description, is_public...
    @staticmethod
    def get_absolute_url():
        return reverse('details')

    def __str__(self):
        return self.name


