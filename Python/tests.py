import unittest
from readers import *


class TestReaders(unittest.TestCase):

    def setUp(self):
        self.reader_id = "web"
        self.w = WebReader(self.reader_id)

    def tearDown(self):
        del self.w

    def test_WebReaderReads(self):
        reading = self.w.get_temp()

    def test_WebReaderError(self):
        self.w.root = "http://nothinghereatall.imsure"
        # How do I know all the exceptions that could be raised?
        self.assertRaises(Exception, self.w.get_temp)

    def test_WebReaderDict(self):
        """
        A Reading from get_temp should return a dict containing:
            'temp'      - a number
            'id'        - a string
            'datetime'  - a string
        """
        reading = self.w.get_temp()
        self.assertTrue(isinstance(reading['temp'], float))
        self.assertTrue(isinstance(reading['id'], str))
        self.assertTrue(isinstance(reading['datetime'], str))


if __name__ == '__main__':
    unittest.main()