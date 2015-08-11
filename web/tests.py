from __future__ import print_function

import time

from django.test import TestCase
from django.test.client import Client


class PerformanceMainPageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def testLoadTime(self):
        for i in range(1, 40):
            start = time.time()
            self.client.get('/')
            end = time.time()
            load_time = end - start

            log_str = 'MainPage :  %f \n ' % (load_time)
            print(log_str)

            with open('web/performance.log', 'a+') as log_file:
                log_file.write(log_str)
