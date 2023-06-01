import unittest
from site_outages import SiteOutages

class TestSiteOutagesClass(unittest.TestCase):
    def test_post_site_outages_with_wrong_data_but_correct_site(self):
        t = SiteOutages()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('norwich-pear-tree', json_payload)

        self.assertTrue('400 Client Error' in str(context.exception))



    def test_post_site_outages_with_invalid_site(self):
        t = SiteOutages()

        json_payload = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                        {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                        {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        with self.assertRaises(Exception) as context:
            t.post_site_outages('some-invalid-site', json_payload)

        self.assertTrue('404 Client Error' in str(context.exception))

