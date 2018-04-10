import json
import numpy
from django.test import TestCase

from impedans_expert.expert_algorithms.algorithms.standard_deviation import *
from impedans_expert.expert_algorithms.models import *


class Test_Standard_Deviation(TestCase):

    def setUp(self):
        self.test_data = [[1,2,3,4,5,6,7,8]]
        self.answer = 2.4494897427831779

    def test_std(self):
        results = do_standard_deviation(self.test_data, [])
        self.assertEquals(results[0][0], self.answer)
