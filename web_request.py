import time
import requests
import logging

# Normally we would never include this key in the file, but for the purposes of this test it is safe (and convenient) to do so
API_KEY     = 'EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23'
MAX_RETRIES = 5
KRAKEN_URL  = 'https://api.krakenflex.systems/interview-tests-mock-api/v1/'


# Custom Exception raised when number of retries exceeded
class RetriesExceededError(Exception):
    def __init__(self, message=f"Retried too many times"):
        self.message = message
        super().__init__(self.message)


class WebRequest():
    def __init__(self):
        return

    # Sends a GET requests and retrieves a response
    def __do_get_request_call_and_get_response(self, url):
        response = None
        retries = 0

        headers = {
            'x-api-key': API_KEY,
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }

        while retries < MAX_RETRIES:
            try:
                response = requests.get(
                    url=url,
                    headers=headers
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(type(e))
                logging.error(e)

                # Here we deal with the case of a returned 500 status code and retry the request up to 5 times with a slight pause in between.
                # Other status codes can be added here if need be, but for the purposes of this test just 500 is required
                # and if anything else terrible happens we raise an exception
                if response.status_code in [500]:
                    retries += 1
                    logging.info("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    raise Exception(e)
            else:
                break

        if retries >= MAX_RETRIES:
            raise RetriesExceededError()

        logging.info("WebRequest::_do_get_request_call_and_get_response status code: " + str(response.status_code))
        return response


    # Sends a POST requests and retrieves a response
    def __do_post_request_and_get_response(self, payload, url):
        response = None
        retries = 0

        headers = {
            'x-api-key': API_KEY
        }

        while retries < MAX_RETRIES:
            try:
                response = requests.post(
                    url=url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(type(e))
                logging.error(e)

                # Here we deal with the case of a returned 500 status code and retry the request up to 5 times with a slight pause in between.
                # Other status codes can be added here if need be, but for the purposes of this test just 500 is required
                # and if anything else terrible happens we raise an exception
                if response.status_code in [500]:
                    retries += 1
                    logging.info("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    raise Exception(e)
            else:
                break

        if retries >= MAX_RETRIES:
            raise RetriesExceededError()

        logging.info("WebRequest::_do_post_request_and_get_response status code: " + str(response.status_code))
        return response


    # Send GET request to outages endpoint and return JSON and status code from the response
    def get_outages_json(self):
        url = KRAKEN_URL + 'outages'
        r = self.__do_get_request_call_and_get_response(url)
        status_code = r.status_code
        if status_code == 200:
            json_object = r.json()
            return json_object, status_code
        else:
            return None, status_code


    def get_site_info_json(self, site_name):
        url = KRAKEN_URL + 'site-info/' + site_name
        response = self.__do_get_request_call_and_get_response(url)
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


    def post_site_outages(self, site_name, payload):
        url = KRAKEN_URL + 'site-outages/' + site_name
        outages_url_response = self.__do_post_request_and_get_response(payload, url)

        logging.info(outages_url_response.text)

        return outages_url_response.status_code