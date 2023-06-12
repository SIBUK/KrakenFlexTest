import unittest

from data_functions import filter_out_unwanted_outage_begin_dates, join_data

class TestDataFunction(unittest.TestCase):

    def test_data_function_filter_out_unwanted_outage_begin_dates(self):
        test_json = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                     {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                     {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        filtered_json = filter_out_unwanted_outage_begin_dates(test_json)

        # Check that the first line of data does exist in the json, as it is exactly equal to '2022-01-01T00:00:00.000Z'
        exists = False
        for line in filtered_json:
            if line['id'] == '00da8493-1780-4945-867e-538d2a77ad7d':
                exists = True
        self.assertTrue(exists)

        # Check that the second line of data does NOT exist in the json as it is earlier than '2022-01-01T00:00:00.000Z'
        exists = False
        for line in filtered_json:
            if line['id'] == '034426d9-431b-42ba-85f9-74fe892d783a':
                exists = True
        self.assertFalse(exists)

        # Check that the third line of data exists in the json as it is later than '2022-01-01T00:00:00.000Z'
        exists = False
        for line in filtered_json:
            if line['id'] == '03ac36ee-7466-4e4f-8343-20a0f7a46014':
                exists = True
        self.assertTrue(exists)


    def test_data_functions_join_data(self):
        test_outage_json = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                            {'id': '11111111-2222-3333-4444-555555555555', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                            {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        test_site_json = [{'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'},
                          {'id': '70656668-571e-49fa-be2e-099c67d136ab', 'name': 'Battery 3'},
                          {'id': '11111111-2222-3333-4444-555555555555', 'name': 'Battery 8'}]

        final_json = join_data(test_site_json, test_outage_json)

        # There should be only 1 matching result
        self.assertEqual(len(final_json), 1)

        # Check that the correct number of columns exist and that they are named correctly
        row = final_json[0]
        self.assertEqual(len(row), 4)
        self.assertTrue('id' in row)
        self.assertTrue('name' in row)
        self.assertTrue('begin' in row)
        self.assertTrue('end' in row)

        # Check that the data contained in the returned json is correct
        self.assertEqual(row['id'], test_outage_json[1]['id'])
        self.assertEqual(row['begin'], test_outage_json[1]['begin'])
        self.assertEqual(row['end'], test_outage_json[1]['end'])
        self.assertEqual(row['name'], test_site_json[2]['name'])



