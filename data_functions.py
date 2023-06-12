import logging
from dateutil import parser

# Minimum outages begin date to use
MINIMUM_BEGIN_TIME = '2022-01-01T00:00:00.000Z'

# Filter out begin dates before MINIMUM_BEGIN_TIME
def filter_out_unwanted_outage_begin_dates(outages_json):
    logging.info("filter_out_unwanted_outage_begin_dates: filtering begin dates")

    new_list = []
    begin_time = parser.parse(MINIMUM_BEGIN_TIME)
    for line in outages_json:
        if parser.parse(line['begin']) >= begin_time:
            new_list.append(line)

    logging.info("filter_out_unwanted_outage_begin_dates: filtering begin dates completed")

    return new_list



# Join both the site data and outages data and create the JSON we need for the final POST, then return it
def join_data(site_info, outages):
    logging.info("join_data: joining site data and outages dataf")

    joined_data = []
    for site in site_info:
        for outage in outages:
            if outage['id'] == site['id']:
                new_line = {'id': outage['id'], 'name': site['name'], 'begin': outage['begin'], 'end': outage['end']}
                joined_data.append(new_line)

    logging.info("join_data: site data and outages data joining complete")

    return joined_data
