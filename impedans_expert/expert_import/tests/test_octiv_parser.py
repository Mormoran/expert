
from django.test import TestCase
from datetime import datetime

from impedans_expert.expert_import.octiv_parser import OctivParser
from impedans_expert.expert.models import Customer, Chamber, Sensor, Data, SensorType, Parameter
from impedans_expert.users.models import User
from impedans_expert.expert_import.models import Runs
from impedans_expert.expert_upload.models import FileUploadModel, FileType


class OctivParserTest(TestCase):

    def setUp(self):
        self.array = ["1;2;3;4;5","3;4;5;6;7","1;2;3;4;5"]
        self.array_result = [["1","2","3","4","5"],["3","4","5","6","7"],["1","2","3","4","5"]]
        self.parser = OctivParser()

        user = User.objects.create(name="test", username="test", password="testing1212")
        self.customer = Customer.objects.create(contact_name="test", company_name="", \
                                           contact_email="test@mail.com", user=user)
        self.chamber = Chamber.objects.create(chamber_name="chamber 1", customer=self.customer)
        octiv = SensorType.objects.create(sensor_type="Octiv")
        self.sensor = Sensor.objects.create(serial_number="12321", chamber=self.chamber, sensor_type=octiv)

        self.file = FileUploadModel.objects.create(customer=self.customer, chamber=self.chamber)

        self.chamber_name = "chamber 1"
        self.serial_number = "12321"

        self.params = ["Voltage","Current"]
        self.pulse_position = "None"
        self.test_parameter = Parameter.objects.create(parameter_name="Voltage", parameter_position="None", \
                                 parameter_type="double")
        self.test_parameter_ids = [self.test_parameter.id]
        # "0.123" = time offset - (not a parameter variable)
        self.test_row_values = ["0.123", "23.2"]
        self.data_timestamp = datetime.strptime("01/01/17 01:01:02","%d/%m/%y %H:%M:%S")


    def test_create_data_array(self):
        results = self.parser.create_data_array(self.array)
        self.assertEquals(results, self.array_result)


    def test_get_chamber(self):
        chamber = self.parser.get_chamber(self.chamber_name, self.customer)
        self.assertEquals(chamber.chamber_name, self.chamber_name)


    def test_get_sensor(self):
        sensor = self.parser.get_sensor(self.serial_number, self.chamber)
        self.assertEquals(sensor.serial_number, self.serial_number)


    def test_get_parameters(self):
        test_param_data = []
        test_param_ids = []

        parameters = self.parser.get_parameters(self.params, self.pulse_position, \
                                                test_param_data, test_param_ids)

        parameter_exists = False
        if self.test_parameter.id in test_param_ids:
            parameter_exists = True

        # get_or_create returns a tuple (object, created) object = Parameter object, created a boolean
        # where True = created, False = got
        parameter = Parameter.objects.get_or_create(parameter_name="Current", parameter_position="None", \
                                        parameter_type="double")

        param_data_populated = False
        for param_data in test_param_data:
            if param_data.name == self.params[0]:
                param_data_populated = True

        # if parameter[1] is False it was got from the database, therefore it was created in the function
        # if parameter[1] is True get_or_create created it, indicating a the test has failed
        self.assertFalse(parameter[1])
        self.assertTrue(param_data_populated)
        self.assertEquals(test_param_data[0].position, self.pulse_position)
        self.assertTrue(parameter_exists)


    def test_create_runs(self):
        all_runs = []
        start_of_run = None
        end_of_run = None
        self.parser.create_runs(start_of_run, end_of_run, self.chamber, self.file, all_runs)
        runs_created = False
        if len(all_runs) > 0:
            runs_created = True
        self.assertFalse(runs_created)

        start_of_run = datetime.strptime("01/01/17 01:01:01","%d/%m/%y %H:%M:%S")
        end_of_run = datetime.strptime("01/01/17 01:02:01","%d/%m/%y %H:%M:%S")
        self.parser.create_runs(start_of_run, end_of_run, self.chamber, self.file, all_runs)

        runs_created = False
        if len(all_runs) > 0:
            runs_created = True
        self.assertTrue(runs_created)


    def test_create_row_data(self):
        all_data = []
        self.parser.create_row_data(self.test_parameter_ids, self.test_row_values, self.sensor, self.data_timestamp, all_data)

        self.assertEquals(float(self.test_row_values[1]), all_data[0].parameter_value)
