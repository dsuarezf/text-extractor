"""Test suite for text-extractor"""

import sys
import unittest

sys.path.insert(0, 'main/python')  # Execute test from project's root directory

from extractor_server import app


class TestTextExtractor(unittest.TestCase):
    """Test suite to test the text extractor"""

    def setUp(self):
        """Set up the test suite"""
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_health_check(self):
        """Test for health check method"""
        result = self.app.get('/v1/health')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'UP')

    def tearDown(self):
        """Tearing down test suite"""


if __name__ == '__main__':
    unittest.main()
