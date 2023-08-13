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

        self.assertTrue(file.is_open())
        self.assertEqual(len(file.files), 4)

    def test_close_file(self):
        file = self.file
        file.open(str(Path(__file__).parent.resolve()) + "/files/ziptest.zip")

        self.assertTrue(file.is_open())
        self.assertTrue(len(file.files) > 0)
        self.assertTrue(file.file is not None)

        file.close()

        self.assertEqual(file.file, None)
        self.assertEqual(len(file.files), 0)
        self.assertTrue(not file.is_open())
