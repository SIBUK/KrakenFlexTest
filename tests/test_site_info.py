import unittest
from unittest.mock import patch, MagicMock
from pyspark.resource import requests
import requests.exceptions
from site_info import SiteInfo

class TestSiteInfoClass(unittest.TestCase):
    # Test that the SiteInfo class is fetching JSON data from its endpoint correctly
    @patch('web_request.requests')
    def test_get_site_info_json_known_good(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value =  \
            {'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree',
            'devices': [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                        {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'}]}

        mock_requests.get.return_value = mock_response

        t = SiteInfo()
        json_object, status_code = t.get_site_info_json('norwich-pear-tree')

        # Test that the status code is 200 for success
        self.assertEqual(status_code, 200)
        # Test that is has returned a list
        self.assertIsInstance(json_object, list)
        # Test that the list contains data
        self.assertEqual(json_object[0]['id'], '111183e7-fb90-436b-9951-63392b36bdd2')
        self.assertEqual(json_object[0]['name'], 'Battery 1')
        self.assertEqual(json_object[1]['id'], '86b5c819-6a6c-4978-8c51-a2d810bb9318')
        self.assertEqual(json_object[1]['name'], 'Battery 2')


    @patch('web_request.requests')
    def test_get_site_info_json_known_bad(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        t = SiteInfo()

        with self.assertRaises(Exception) as context:
            t.get_site_info_json('an-invalid-site-name')

        self.assertTrue('404 Client Error' in str(context.exception))


    # Test that the SiteInfo class is fetching JSON data from its endpoint correctly
    @patch('web_request.requests')
    def test_get_site_info_wrong_site_returned(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value =  \
            {'id': 'wrong-site-name', 'name': 'Norwich Pear Tree',
            'devices': [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                        {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'}]}

        mock_requests.get.return_value = mock_response

        t = SiteInfo()
        with self.assertRaises(Exception) as context:
            t.get_site_info_json('norwich-pear-tree')



if __name__ == '__main__':
    unittest.main()

