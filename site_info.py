import logging
from web_request import WebRequest


class SiteInfo(WebRequest):
    def __init__(self):
        WebRequest.__init__(self, 'site-info')
        return

    # Send GET request to site-info endpoint and return JSON and status code from the response
    def get_site_info_json(self, site_name):
        self.URL += '/' + site_name
        response = self._do_get_request_call_and_get_response()
        status_code = response.status_code
        if status_code == 200:
            json_object = response.json()

            id = json_object['id']
            name = json_object['name']
            device_data = json_object['devices']

            if id != site_name:
                raise Exception("SiteInfo::get_site_info_json - Data for site " + site_name + " was requested but site " + id + " was returned instead")

            logging.info("SiteInfo::ingest_site_info - Site name: " + name)
            return device_data, status_code
        else:
            logging.info("SiteInfo::ingest_site_info - Failure to get site data for site name: " + site_name)
            return None, status_code


