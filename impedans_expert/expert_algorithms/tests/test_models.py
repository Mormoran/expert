from datetime import datetime

from django.test import TestCase

from impedans_expert.expert_algorithms.models import Algorithm, AlgorithmRun, \
                         AlgorithmRunResults, AlgorithmTimeResults, \
                         AlgorithmState
from impedans_expert.expert_import.models import Runs
from impedans_expert.users.models import User
from impedans_expert.expert.models import Customer, Chamber, Parameter
# test the views

class AlgorithmTestCase(TestCase):

    def setUp(self):
        self.algorithm = Algorithm.objects.create(algorithm_name="Algorithm",
                                                  algorithm_src="///",
                                                  algorithm_description="Testing")


    def test_algorithm_name(self):
        self.assertEquals(self.algorithm.algorithm_name, "Algorithm")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_algorithm_source(self):
        self.assertEquals(self.algorithm.algorithm_src, "///")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_algorithm_description(self):
        self.assertEquals(self.algorithm.algorithm_description, "Testing")
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail


class AlgorithmRunTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test", username="Test", password="testing1212")
        self.customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                                contact_email="p.s@m.com", user=self.user)

        self.algorithm = Algorithm.objects.create(algorithm_name="Algorithm",
                                                  algorithm_src="///",
                                                  algorithm_description="Testing")

        self.algorithm_run = AlgorithmRun.objects.create(algorithm=self.algorithm,
                                                         customer=self.customer)

    def test_algorithm_run_algorithm(self):
        self.assertEquals(self.algorithm_run.algorithm, self.algorithm)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_algorithm_run_customer(self):
        self.assertEquals(self.algorithm_run.customer, self.customer)
        # AssertTrue, AssertFalse, AssertEqual define test pass/fail

    def test_algorithm_run_date(self):
        self.assertTrue(isinstance(self.algorithm_run.date_time, datetime))


class AlgorithmTimeResultsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(name="Test", username="Test", password="testing1212")
        self.customer = Customer.objects.create(company_name="TestCompany", contact_name="person",
                                                contact_email="p.s@m.com", user=self.user)

        self.algorithm = Algorithm.objects.create(algorithm_name="Algorithm",
                                                  algorithm_src="///",
                                                  algorithm_description="Testing")

        self.algorithm_run = AlgorithmRun.objects.create(algorithm=self.algorithm,
                                                         customer=self.customer)

        self.chamber = Chamber.objects.create(chamber_name="Chamber", customer=self.customer)

        self.parameter = Parameter.objects.create(parameter_name="parameter")

        self.time_result = AlgorithmTimeResults(algorithm_run=self.algorithm_run,
                                                parameter=self.parameter,
                                                value=1,
                                                start_time=datetime.now(),
                                                end_time=datetime.now(),
                                                chamber=self.chamber)

    def test_algorithm_time_result_algorithm_run(self):
        self.assertEquals(self.time_result.algorithm_run, self.algorithm_run)

    def test_algorithm_time_result_parameter(self):
        self.assertEquals(self.time_result.parameter, self.parameter)

    def test_algorithm_time_result_value(self):
        self.assertEquals(self.time_result.value, 1)

    def test_algorithm_time_result_chamber(self):
        self.assertEquals(self.time_result.chamber, self.chamber)

    def test_algorithm_time_result_start_time(self):
        self.assertTrue(isinstance(self.time_result.start_time, datetime))

    def test_algorithm_time_result_end_time(self):
        self.assertTrue(isinstance(self.time_result.end_time, datetime))
