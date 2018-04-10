from django.test import TestCase
from datetime import datetime

from impedans_expert.expert_algorithms.utils import GetResults, Result
# Create your tests here.

class GetResultsTest(TestCase):

    def setUp(self):
        print("set up")
        self.test_time = datetime.strptime("01/01/17 01:01:01","%d/%m/%y %H:%M:%S")
        self.mock_results = []
        self.mock_results.append(Result(1.24, self.test_time))
        self.mock_json_string = '[{"label": "Results", "x": [0], "y": [1.24]}]'

    def test_format_results(self):
        res = GetResults()
        results = res.format_results(self.mock_results)
        self.assertEquals(sorted(results), sorted(self.mock_json_string))
