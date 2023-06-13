import unittest
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import requests

from web_request import WebRequest


class TestOutagesClass(unittest.TestCase):
    # Test that the outages class is fetching JSON data from its endpoint correctly
    @patch('web_request.requests')
    def test_web_request_get_outages_json_success(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.OK)
        mock_response.json.return_value =  \
            [{'id': 'mock_id_1', 'begin': 'mock_begin_1', 'end': 'mock_end_1'},
             {'id': 'mock_id_2', 'begin': 'mock_begin_2', 'end': 'mock_end_2'}]

        mock_requests.get.return_value = mock_response

        t = WebRequest()
        json_object, status_code = t.get_outages_json()

        # Test that the status code is 200 for success
        self.assertEqual(status_code, HTTPStatus.OK)
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
    def test_web_request_get_outages_json_fail(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.FORBIDDEN)
        mock_response.json.return_value = None

        mock_requests.get.return_value = mock_response

        t = WebRequest()
        json_object, status_code = t.get_outages_json()

        # Test that the status code is 403 for success
        self.assertEqual(status_code, HTTPStatus.FORBIDDEN)
        # Test that is has returned a list
        self.assertEqual(json_object, None)

    @patch('web_request.requests')
    def test_web_request_post_site_outages_with_valid_site_and_data(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.OK)
        mock_requests.post.return_value = mock_response

        t = WebRequest()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        status_code = t.post_site_outages('some-invalid-site', json_payload)

        self.assertEqual(status_code, HTTPStatus.OK)


    @patch('web_request.requests')
    def test_web_request_post_site_outages_with_invalid_data_but_correct_site(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.BAD_REQUEST)
        mock_response.raise_for_status.side_effect = requests.HTTPError('400 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.post.return_value = mock_response

        t = WebRequest()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('norwich-pear-tree', json_payload)

        self.assertTrue('400 Client Error' in str(context.exception))


    @patch('web_request.requests')
    def test_web_request_post_site_outages_with_invalid_site(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.NOT_FOUND)
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.post.return_value = mock_response

        t = WebRequest()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('some-invalid-site', json_payload)

        self.assertTrue('404 Client Error' in str(context.exception))


    @patch('web_request.requests')
    def test_web_request_get_site_info_json_known_good(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.OK)
        mock_response.json.return_value =  \
            {'id': 'norwich-pear-tree', 'name': 'Norwich Pear Tree',
            'devices': [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                        {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'}]}

        mock_requests.get.return_value = mock_response

        t = WebRequest()
        json_object, status_code = t.get_site_info_json('norwich-pear-tree')

        # Test that the status code is 200 for success
        self.assertEqual(status_code, HTTPStatus.OK)
        # Test that is has returned a list
        self.assertIsInstance(json_object, list)
        # Test that the list contains data
        self.assertEqual(json_object[0]['id'], '111183e7-fb90-436b-9951-63392b36bdd2')
        self.assertEqual(json_object[0]['name'], 'Battery 1')
        self.assertEqual(json_object[1]['id'], '86b5c819-6a6c-4978-8c51-a2d810bb9318')
        self.assertEqual(json_object[1]['name'], 'Battery 2')


    @patch('web_request.requests')
    def test_web_request_get_site_info_json_known_bad(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.NOT_FOUND)
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        t = WebRequest()

        with self.assertRaises(Exception) as context:
            t.get_site_info_json('an-invalid-site-name')

        self.assertTrue('404 Client Error' in str(context.exception))


    # Test that the SiteInfo class is fetching JSON data from its endpoint correctly
    @patch('web_request.requests')
    def test_web_request_get_site_info_wrong_site_returned(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.OK)
        mock_response.json.return_value =  \
            {'id': 'wrong-site-name', 'name': 'Norwich Pear Tree',
            'devices': [{'id': '111183e7-fb90-436b-9951-63392b36bdd2', 'name': 'Battery 1'},
                        {'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'}]}

        mock_requests.get.return_value = mock_response

        t = WebRequest()
        with self.assertRaises(Exception) as context:
            t.get_site_info_json('norwich-pear-tree')


    # Test that the Error 500 retries functionality is working correctly during GET requests
    @patch('web_request.requests')
    def test_get_web_request_retries(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_response.raise_for_status.side_effect = requests.HTTPError('500 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        t = WebRequest()

        with self.assertRaises(Exception) as context:
            t.get_site_info_json('an-invalid-site-name')

        self.assertTrue('Retried too many times' in str(context.exception))


    # Test that the Error 500 retries functionality is working correctly during POST requests
    @patch('web_request.requests')
    def test_post_web_request_retries(self, mock_requests):
        mock_response = MagicMock(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        mock_response.raise_for_status.side_effect = requests.HTTPError('500 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.post.return_value = mock_response

        t = WebRequest()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('some-invalid-site', json_payload)

        self.assertTrue('Retried too many times' in str(context.exception))

if __name__ == '__main__':
    unittest.main()

