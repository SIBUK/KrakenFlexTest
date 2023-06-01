from pyspark.shell import sc
from pyspark.sql import SparkSession
import logging
from pyspark.sql.types import StructType, StructField, TimestampType, StringType

# This flag can be set to True which will output some of the contents of the dataframe files to aid with debugging if need be
DEBUG = False

class SparkWrapper():
    def __init__(self, spark_instance):
        self.spark = spark_instance
        return


    # Create and return the dataframe that contains the outages data
    def create_and_get_outages_dataframe_from_json(self, json_object):
        logging.info("SparkWrapper::create_and_get_outages_dataframe_from_json: creating outages dataframe")
        outages_schema = StructType(fields=[
            StructField("begin", TimestampType(), False),
            StructField("end", TimestampType(), False),
            StructField("id", StringType(), False)
        ])

        df = self.spark.read.schema(outages_schema).json(sc.parallelize([json_object]), multiLine=True)
        logging.info("SparkWrapper::create_and_get_outages_dataframe_from_json: outages dataframe created")
        self.__show_dataframe(df)

        return df


    # Filter out begin dates before '2022-01-01T00:00:00.000Z' (minor optimisation doing this first before the join)
    def filter_out_unwanted_outage_begin_dates(self, df):
        logging.info("SparkWrapper::filter_out_unwanted_outage_begin_dates: filtering begin dates")
        final_outages_df = df.filter("begin >= '2022-01-01T00:00:00.000Z'").orderBy("begin", ascending=True)
        logging.info("SparkWrapper::filter_out_unwanted_outage_begin_dates: filtering begin dates completed")

        self.__show_dataframe(final_outages_df)

        return final_outages_df


    # Create and return the dataframe that contains the site data
    def create_and_get_site_data_dataframe_from_json(self, json_object):
        logging.info("SparkWrapper::create_and_get_site_data_dataframe_from_json: creating site data dataframe")
        site_info_schema = StructType(fields=[
            StructField("id", StringType(), False),
            StructField("name", StringType(), False)
        ])

        site_info_df = self.spark.read.schema(site_info_schema).json(sc.parallelize([json_object]), multiLine=True)
        logging.info("SparkWrapper::create_and_get_site_data_dataframe_from_json: site data dataframe created")

        self.__show_dataframe(site_info_df)

        return site_info_df


    # Join both the site data and outages dataframe tables and select just the columns we need for the final POST
    # then return  anew dataframe containing this info
    def join_dataframes(self, site_info_df, outages_df):
        logging.info("SparkWrapper::join_dataframes: joining site data and outages dataframes")

        final_df = site_info_df.join(outages_df, site_info_df.id == outages_df.id, "inner") \
            .select(site_info_df.id, site_info_df.name, outages_df.begin, outages_df.end) \
            .orderBy('name', ascending=True)

        logging.info("SparkWrapper::join_dataframes: site data and outages dataframes joining complete")

        self.__show_dataframe(final_df)

        return final_df


    def __show_dataframe(self, df):
        if DEBUG == True:
            df.show(truncate=False)
