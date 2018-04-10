import os.path
from django.test import TestCase
from django.utils import timezone
from django.test import client
from impedans_expert.expert_import.forms import FileParseForm
from impedans_expert.users.models import User
from impedans_expert.expert_upload.models import FileUploadModel, FileType
from impedans_expert.expert.models import Customer, Chamber, Sensor, SensorType

# test the forms

class FileParseFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(name="test", username="test", password="testing1212")
        customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                contact_email="p.s@m.com", user=user)
        # customer = Customer.objects.get(company_name="TestCompany")
        file_type = FileType.objects.create(name="Type", options="Test",
                                            parser_config="/home/luke/Downloads/build.txt",
                                            customer=customer)

        chamber = Chamber.objects.create(chamber_name="Chamber", customer=customer)
        sensor_type = SensorType.objects.create(sensor_type="Octiv")

        sensor = Sensor.objects.create(serial_number="12345", chamber=chamber,
                                       sensor_type=sensor_type)

        file = os.path.realpath("/home/luke/Downloads/build.txt")
        FileUploadModel.objects.create(file=file, _file_size=6, sensor=sensor,
                                       file_type=file_type, chamber=chamber,
                                       name="testfile", owner=user, customer=customer)


    def test_parse_form_file_label(self):
        form = FileParseForm()
        self.assertTrue(form.fields['file'].label=="File: ")

    def test_parse_form_config_label(self):
        form = FileParseForm()
        self.assertTrue(form.fields['config'].label=="Type: ")

    def test_parse_form_file_query(self):
        rf = client.RequestFactory()
        request = rf.get('expert_import:Parse')
        request.user = User.objects.get(username="test")
        form = FileParseForm(request=request)
        files_available = form.fields['file'].queryset
        num_of_files_available = len(list(files_available))
        self.assertEquals(num_of_files_available, 1)

    def test_parse_form_file_configuration_query(self):
        rf = client.RequestFactory()
        request = rf.get('expert_import:Parse')
        request.user = User.objects.get(username="test")
        form = FileParseForm(request=request)
        files_available = form.fields['config'].queryset
        num_of_configurations_available = len(list(files_available))
        self.assertEquals(num_of_configurations_available, 1)

