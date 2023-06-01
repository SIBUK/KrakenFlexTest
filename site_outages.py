import logging
from web_request import WebRequest

# Send POST request to site-outages endpoint and the status code from the response
class SiteOutages(WebRequest):
    def __init__(self):
        WebRequest.__init__(self, 'site-outages')
        return

    def post_site_outages(self, site_name, payload):
        self.URL += '/' + site_name
        outages_url_response = self._do_post_request_and_get_response(payload)

        logging.info(outages_url_response.text)

        return outages_url_response.status_code
