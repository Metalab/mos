import os
import sys
import tempfile
import shutil
from io import StringIO

from django.test import TestCase

from ..models import Payment


CSV = u'01.01.2016;"a line";01.01.2016;123,45;EUR;01.01.2016 01:02:03:456;'


class ImportTest(TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_delimiter_is_string(self):
        csv_file = os.path.join(self.tempdir, 'import.csv')
        with open(csv_file, 'w') as outfile:
            outfile.write(CSV)

        try:
            sys.stdout = None
            Payment.objects.import_smallfile(csv_file, '2016-01-02')
        except TypeError as e:
            if e.message == '"delimiter" must be an 1-character string':
                assert False, 'The delimiter argument for csv.reader() is of the wrong type.'
            else:
                raise
        finally:
            sys.stdout = sys.__stdout__
