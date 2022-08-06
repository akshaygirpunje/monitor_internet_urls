from python_monitor_url import *
import unittest

class TestURL(unittest.TestCase):
    def test_get_url_status(self):
        self.assertAlmostEqual(get_url_status('https://httpstat.us/200'),1)

    def test_get_url_status1(self):
        self.assertAlmostEqual(get_url_status('https://httpstat.us/503'),0)

    def test_get_url_status2(self):
        self.assertAlmostEqual(get_url_status('https://httpstat.us/400'),0)


    def test_get_response(self):
        self.assertGreaterEqual(get_response('https://httpstat.us/200'),0)

    def test_get_response1(self):
        self.assertGreaterEqual(get_response('https://httpstat.us/503'),0)

    def test_get_response2(self):
        self.assertGreaterEqual(get_response('https://httpstat.us/400'),0)
