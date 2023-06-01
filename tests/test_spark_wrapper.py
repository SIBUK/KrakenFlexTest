import unittest
import pyspark
from pyspark.shell import sc
from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, StringType, StructType, StructField

from spark_wrapper import SparkWrapper

class TestSparkWrapperClass(unittest.TestCase):
    def test_spark_wrapper_create_and_get_outages_dataframe_from_json(self):
        spark = SparkSession.builder.master("local[1]") \
            .appName('KrakenFlexTestTests') \
            .getOrCreate()

        t = SparkWrapper(spark)

        test_json = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                     {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                     {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        df = t.create_and_get_outages_dataframe_from_json(test_json)

        self.assertIsInstance(df, pyspark.sql.dataframe.DataFrame)

        # Check that the correct number of columns exist and that they are named correctly
        column_names = df.columns
        self.assertEqual(len(column_names), 3)
        self.assertTrue('begin' in column_names)
        self.assertTrue('end' in column_names)
        self.assertTrue('id' in column_names)

        # Check that the column types are correct
        self.assertIsInstance(df.schema["begin"].dataType, TimestampType)
        self.assertIsInstance(df.schema["end"].dataType, TimestampType)
        self.assertIsInstance(df.schema["id"].dataType, StringType)

        # Check that the 3 rows of data are in the dataframe
        self.assertEqual(df.count(), 3)


    def test_spark_wrapper_filter_out_unwanted_outage_begin_dates(self):
        spark = SparkSession.builder.master("local[1]") \
            .appName('KrakenFlexTestTests') \
            .getOrCreate()

        t = SparkWrapper(spark)

        test_json = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                     {'id': '034426d9-431b-42ba-85f9-74fe892d783a', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                     {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        df = t.create_and_get_outages_dataframe_from_json(test_json)

        filtered_df = t.filter_out_unwanted_outage_begin_dates(df)

        # Check that the first line of data exists in the dataframe as it is exactly equal to '2022-01-01T00:00:00.000Z'
        filter_string = f"id == '{test_json[0]['id']}' and begin == '{test_json[0]['begin']}' and end == '{test_json[0]['end']}'"
        line_df = filtered_df.filter(filter_string)
        self.assertEqual(line_df.count(), 1)

        # Check that the first line of data does NOT exist in the dataframe as it is earlier than '2022-01-01T00:00:00.000Z'
        filter_string = f"id == '{test_json[1]['id']}' and begin == '{test_json[1]['begin']}' and end == '{test_json[1]['end']}'"
        line_df = filtered_df.filter(filter_string)
        self.assertEqual(line_df.count(), 0)

        # Check that the first line of data exists in the dataframe as it is late than '2022-01-01T00:00:00.000Z'
        filter_string = f"id == '{test_json[2]['id']}' and begin == '{test_json[2]['begin']}' and end == '{test_json[2]['end']}'"
        line_df = filtered_df.filter(filter_string)
        self.assertEqual(line_df.count(), 1)


    def test_spark_wrapper_create_and_get_site_data_dataframe_from_json(self):
        spark = SparkSession.builder.master("local[1]") \
            .appName('KrakenFlexTestTests') \
            .getOrCreate()

        t = SparkWrapper(spark)

        test_json = [{'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'},
                     {'id': '70656668-571e-49fa-be2e-099c67d136ab', 'name': 'Battery 3'},
                     {'id': '75e96db4-bba2-4035-8f43-df2cbd3da859', 'name': 'Battery 8'}]

        df = t.create_and_get_site_data_dataframe_from_json(test_json)

        # Test that a dataframe was returned
        self.assertIsInstance(df, pyspark.sql.dataframe.DataFrame)

        # Check that the correct number of columns exist and that they are named correctly
        column_names = df.columns
        self.assertEqual(len(column_names), 2)
        self.assertTrue('id' in column_names)
        self.assertTrue('name' in column_names)

        # Check that the column types are correct
        self.assertIsInstance(df.schema["id"].dataType, StringType)
        self.assertIsInstance(df.schema["name"].dataType, StringType)

        # Check that the 3 rows of data are in the dataframe
        self.assertEqual(df.count(), 3)


    def test_spark_wrapper_join_dataframes(self):
        spark = SparkSession.builder.master("local[1]") \
            .appName('KrakenFlexTestTests') \
            .getOrCreate()

        t = SparkWrapper(spark)

        test_outage_json = [{'id': '00da8493-1780-4945-867e-538d2a77ad7d', 'begin': '2022-01-01T00:00:00.000Z', 'end': '2021-11-14T07:43:52.874Z'},
                            {'id': '11111111-2222-3333-4444-555555555555', 'begin': '2021-01-01T00:00:00.000Z', 'end': '2022-12-15T13:38:16.679Z'},
                            {'id': '03ac36ee-7466-4e4f-8343-20a0f7a46014', 'begin': '2022-08-20T16:41:22.884Z', 'end': '2022-08-30T01:09:20.303Z'}]

        test_outage_df = t.create_and_get_outages_dataframe_from_json(test_outage_json)

        test_site_json = [{'id': '86b5c819-6a6c-4978-8c51-a2d810bb9318', 'name': 'Battery 2'},
                          {'id': '70656668-571e-49fa-be2e-099c67d136ab', 'name': 'Battery 3'},
                          {'id': '11111111-2222-3333-4444-555555555555', 'name': 'Battery 8'}]

        test_site_df = t.create_and_get_site_data_dataframe_from_json(test_site_json)

        final_df = t.join_dataframes(test_site_df, test_outage_df)

        # Test that a dataframe was returned
        self.assertIsInstance(final_df, pyspark.sql.dataframe.DataFrame)

        # Check that the correct number of columns exist and that they are named correctly
        column_names = final_df.columns
        self.assertEqual(len(column_names), 4)
        self.assertTrue('id' in column_names)
        self.assertTrue('name' in column_names)
        self.assertTrue('begin' in column_names)
        self.assertTrue('end' in column_names)

        # Check that the column types are correct
        self.assertIsInstance(final_df.schema["id"].dataType, StringType)
        self.assertIsInstance(final_df.schema["name"].dataType, StringType)
        self.assertIsInstance(final_df.schema["begin"].dataType, TimestampType)
        self.assertIsInstance(final_df.schema["end"].dataType, TimestampType)

        # There should be only 1 matching result
        self.assertEqual(final_df.count(), 1)

        # And it should contain the following data
        filter_string = f"id == '{test_outage_json[1]['id']}' and " \
                f"begin == '{test_outage_json[1]['begin']}' and " \
                f"end == '{test_outage_json[1]['end']}' and " \
                f"name == '{test_site_json[2]['name']}'"
        line_df = final_df.filter(filter_string)
        self.assertEqual(line_df.count(), 1)

