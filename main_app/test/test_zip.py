import os
from pathlib import Path
from unittest import TestCase
from main_app.util.zip import BgsZipfile

class TestZipFile(TestCase):
    file: BgsZipfile

    def setUp(self):
        self.file = BgsZipfile()

    def tearDown(self):
        self.file.close()

    def test_open_file(self):
        file = self.file

        file.open(str(Path(__file__).parent.resolve()) + "/files/ziptest.zip")

        self.assertEqual(len(file.files), 4)

