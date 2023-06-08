import unittest
from unittest.mock import patch, MagicMock
from outages import Outages

class TestOutagesClass(unittest.TestCase):
    # Test that the outages class is fetching JSON data from its endpoint correctly
    @patch('web_request.requests')
    def test_get_outages_json_success(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value =  \
            [{'id': 'mock_id_1', 'begin': 'mock_begin_1', 'end': 'mock_end_1'},
             {'id': 'mock_id_2', 'begin': 'mock_begin_2', 'end': 'mock_end_2'}]

        mock_requests.get.return_value = mock_response

        t = Outages()
        json_object, status_code = t.get_outages_json()

        # Test that the status code is 200 for success
        self.assertEqual(status_code, 200)
        # Test that is has returned a list
        self.assertIsInstance(json_object, list)
        # Test that the list contains the correct data
        self.assertEqual(json_object[0]['id'], 'mock_id_1')
        self.assertEqual(json_object[0]['begin'], 'mock_begin_1')
        self.assertEqual(json_object[0]['end'], 'mock_end_1')
        self.assertEqual(json_object[1]['id'], 'mock_id_2')
        self.assertEqual(json_object[1]['begin'], 'mock_begin_2')
        self.assertEqual(json_object[1]['end'], 'mock_end_2')


    @patch('web_request.requests')
    def test_get_outages_json_fail(self, mock_requests):
        mock_response = MagicMock(status_code=403)
        mock_response.json.return_value = None

        mock_requests.get.return_value = mock_response

        t = Outages()
        json_object, status_code = t.get_outages_json()

        # Test that the status code is 403 for success
        self.assertEqual(status_code, 403)
        # Test that is has returned a list
        self.assertEqual(json_object, None)


if __name__ == '__main__':
    unittest.main()

