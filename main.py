import json
from pyspark.sql import SparkSession
from outages import Outages
from site_info import SiteInfo
from site_outages import SiteOutages
from spark_wrapper import SparkWrapper
import logging

def main():
    logging.basicConfig(level=logging.INFO)

    # Create PySpark instance and add it into the SparkWrapper class
    spark = create_spark_instance('KrakenFlexTest')
    si = SparkWrapper(spark)

    # Fetch Outages data and put it in a dataframe
    outages = Outages()
    outages_json, status_code = outages.get_outages_json()
    outages_df = si.create_and_get_outages_dataframe_from_json(outages_json)
    final_outages_df = si.filter_out_unwanted_outage_begin_dates(outages_df)

    # Fetch Site Info data and put it in a dataframe
    site_info = SiteInfo()
    site_info_json, status_code = site_info.get_site_info_json('norwich-pear-tree')
    final_site_info_df = si.create_and_get_site_data_dataframe_from_json(site_info_json)

    # Join both the dataframe tables and return another dataframe that contains just the columns we need
    final_df = si.join_dataframes(final_site_info_df, final_outages_df)

    # Convert the final dataframe to an array of dicts ready for sending to the POST endpoint
    post_json = final_df.toJSON().map(json.loads).collect()

    # POST the data
    site_outages = SiteOutages()
    status_code = site_outages.post_site_outages('norwich-pear-tree', post_json)
    logging.info("Final Status Code: " + str(status_code))

    success = status_code == 200

    if success:
        print("Task completed successfully!")
    else:
        print("An issue occurred while completing the task.")

    # End spark session
    spark.stop()

    exit(0)

def create_spark_instance(app_name):
    spark_instance = SparkSession.builder.master("local[1]") \
        .appName(app_name) \
        .getOrCreate()
    if spark_instance is None:
        raise Exception("Error creating PySpark instance. Cannot continue.")
    else:
        logging.info(spark_instance)

    return spark_instance


if __name__ == "__main__":
    main()
