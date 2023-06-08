import unittest
from unittest.mock import patch, MagicMock
from pyspark.resource import requests
import requests.exceptions
from site_outages import SiteOutages

class TestSiteOutagesClass(unittest.TestCase):
    @patch('web_request.requests')
    def test_post_site_outages_with_valid_site_and_data(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_requests.post.return_value = mock_response

        t = SiteOutages()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        status_code = t.post_site_outages('some-invalid-site', json_payload)

        self.assertEqual(status_code, 200)


    @patch('web_request.requests')
    def test_post_site_outages_with_invalid_data_but_correct_site(self, mock_requests):
        mock_response = MagicMock(status_code=400)
        mock_response.raise_for_status.side_effect = requests.HTTPError('400 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.post.return_value = mock_response

        t = SiteOutages()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('norwich-pear-tree', json_payload)

        self.assertTrue('400 Client Error' in str(context.exception))


    @patch('web_request.requests')
    def test_post_site_outages_with_invalid_site(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Client Error')

        mock_requests.exceptions = requests.exceptions
        mock_requests.post.return_value = mock_response

        t = SiteOutages()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('some-invalid-site', json_payload)

        self.assertTrue('404 Client Error' in str(context.exception))


if __name__ == '__main__':
    unittest.main()

