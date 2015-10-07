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
        self.failUnlessRaises(ConnectionError, self.w.get_temp())


if __name__ == '__main__':
    unittest.main()