import time
import datetime

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

            log_str = 'MainPage :  %f \n ' %(load_time)
            print log_str

            log_file = open('web/performance.log', 'a+')
            log_file.write(log_str)
            log_file.close()
