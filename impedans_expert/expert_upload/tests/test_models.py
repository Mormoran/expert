import os.path
import datetime
from django.test import TestCase
from impedans_expert.expert_upload.models import FileUploadModel, FileType
from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer, Chamber, Sensor, SensorType
# test the views

class UploadModelTestCase(TestCase):

    @classmethod
    def setUp(self):
        # do set up
        self.user = User.objects.create(name="Test", username="Test", password="testing1212")
        # user = User.objects.get(name="Test")
        self.customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                                contact_email="p.s@m.com", user=self.user)
        # customer = Customer.objects.get(company_name="TestCompany")
        self.file_type = FileType.objects.create(name="Type", options="Test",
                                                 parser_config="/home/luke/Downloads/build.txt",
                                                 customer=self.customer)

        self.chamber = Chamber.objects.create(chamber_name="Chamber", customer=self.customer)
        self.sensor_type = SensorType.objects.create(sensor_type="Octiv")

        self.sensor = Sensor.objects.create(serial_number="12345", chamber=self.chamber,
                                            sensor_type=self.sensor_type)

        file = os.path.realpath("/home/luke/Downloads/build.txt")
        self.test_file = FileUploadModel.objects.create(file=file, _file_size=6, sensor=self.sensor,
                                                        file_type=self.file_type, chamber=self.chamber,
                                                        name="testfile", owner=self.user,
                                                        customer=self.customer)
    def test_file_name(self):
        # check doc
        self.assertEquals(self.test_file.name, "testfile")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_owner(self):
        # check doc
        self.assertEquals(self.test_file.owner, self.user)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_customer(self):
        # check doc
        self.assertEquals(self.test_file.customer, self.customer)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_chamber(self):
        # check doc
        self.assertEquals(self.test_file.chamber, self.chamber)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_sensor(self):
        # check doc
        self.assertEquals(self.test_file.sensor, self.sensor)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_file_date(self):
        self.assertTrue(isinstance(self.test_file.date, datetime.datetime))

    def test_file_parsed(self):
        self.assertFalse(self.test_file.parsed)

    def test_filetype_name(self):
        self.assertEquals(self.file_type.name, "Type")

    def test_filetype_options(self):
        self.assertEquals(self.file_type.options, "Test")

    def test_filetype_parser_config(self):
        self.assertEquals(self.file_type.parser_config, "/home/luke/Downloads/build.txt")
