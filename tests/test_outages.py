import unittest
from outages import Outages

class TestOutagesClass(unittest.TestCase):
    # Test that the outages class is fetching JSON data from its endpoint correctly
    def test_get_outages_json(self):
        t = Outages()
        json_object, status_code = t.get_outages_json()

        # Test that the status code is 200 for success
        self.assertEqual(status_code, 200)
        # Test that is has returned a list
        self.assertIsInstance(json_object, list)
        # Test that the list contains data
        self.assertGreater(len(json_object), 0)