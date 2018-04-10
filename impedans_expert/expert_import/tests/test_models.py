import os.path
from django.test import TestCase
from impedans_expert.expert_upload.models import FileUploadModel, FileType
from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer, Chamber, Sensor, SensorType
# test the views

class ImportModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # do set up
        user = User.objects.create(name="Test", username="Test", password="testing1212")
        # user = User.objects.get(name="Test")
        customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                contact_email="p.s@m.com", user=user)
        # customer = Customer.objects.get(company_name="TestCompany")
        file_type = FileType.objects.create(name="Type", options="Test",
                                            parser_config="/home/luke/Downloads/build.txt",
                                            customer=customer)

        chamber = Chamber.objects.create(chamber_name="Chamber", customer=customer
        )
        sensor_type = SensorType.objects.create(sensor_type="Octiv")

        sensor = Sensor.objects.create(serial_number="12345", chamber=chamber,
                                       sensor_type=sensor_type)

        file = os.path.realpath("/home/luke/Downloads/build.txt")
        FileUploadModel.objects.create(file=file, _file_size=6, sensor=sensor,
                                       file_type=file_type, chamber=chamber,
                                       name="testfile", owner=user, customer=customer)

        # def setUp(self):
        # do set up per method
        #    print("set up done")
    """
    def test_file_name(self):
        # check doc
        test_file = FileUploadModel.objects.get(name="testfile")
        self.assertEquals(test_file.name, "testfile")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_owner(self):
        # check doc
        test_file = FileUploadModel.objects.get(name="testfile")
        user = User.objects.get(name="Test")
        self.assertEquals(test_file.owner, user)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_customer(self):
        # check doc
        test_file = FileUploadModel.objects.get(name="testfile")
        customer = Customer.objects.get(company_name="TestCompany")
        self.assertEquals(test_file.customer, customer)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_chamber(self):
        # check doc
        test_file = FileUploadModel.objects.get(name="testfile")
        chamber = Chamber.objects.get(chamber_name="Chamber")
        self.assertEquals(test_file.chamber, chamber)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_sensor_tye(self):
        # check doc
        sensor = Sensor.objects.get(serial_number="12345")
        sensor_type = SensorType.objects.get(sensor_type="Octiv")
        self.assertEquals(sensor.sensor_type, sensor_type)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_sensor(self):
        # check doc
        test_file = FileUploadModel.objects.get(name="testfile")
        sensor = Sensor.objects.get(serial_number="12345")
        self.assertEquals(test_file.sensor, sensor)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail
    """
