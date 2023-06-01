import unittest
from site_info import SiteInfo

class TestSiteInfoClass(unittest.TestCase):
    # Test that the SiteInfo class is fetching JSON data from its endpoint correctly
    def test_get_site_info_json_known_good(self):
        t = SiteInfo()
        json_object, status_code = t.get_site_info_json('norwich-pear-tree')

        # Test that the status code is 200 for success
        self.assertEqual(status_code, 200)
        # Test that is has returned a list
        self.assertIsInstance(json_object, list)
        # Test that the list contains data
        self.assertGreater(len(json_object), 0)


    def test_get_site_info_json_known_bad(self):
        t = SiteInfo()

        with self.assertRaises(Exception) as context:
            t.get_site_info_json('an-invalid-site-name')

        self.assertTrue('404 Client Error' in str(context.exception))
