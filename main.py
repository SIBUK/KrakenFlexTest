import json
from http import HTTPStatus
from data_functions import filter_out_unwanted_outage_begin_dates, join_data
import logging

from web_request import WebRequest

def main():
    logging.basicConfig(level=logging.INFO)

    # Create class for doing HTTP requests
    req = WebRequest()

    # Fetch Outages data as JSON
    outages_json, status_code = req.get_outages_json()
    final_outages_json = filter_out_unwanted_outage_begin_dates(outages_json)

    # Fetch Site Info data as JSON
    site_info_json, status_code = req.get_site_info_json('norwich-pear-tree')

    # Join both the JSON files
    post_json = join_data(site_info_json, final_outages_json)

    # POST the data
    status_code = req.post_site_outages('norwich-pear-tree', post_json)
    logging.info("Final Status Code: " + str(status_code))

    if status_code == HTTPStatus.OK:
        print("Task completed successfully!")
    else:
        print("An issue occurred while completing the task.")

    exit(0)


if __name__ == "__main__":
    main()
