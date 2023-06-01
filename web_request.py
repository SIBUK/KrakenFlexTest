import time
import requests
import logging

class WebRequest():
    def __init__(self, url_appendix):
        self.URL = 'https://api.krakenflex.systems/interview-tests-mock-api/v1/' + url_appendix
        # Note that the api key would normally be put in a secure store such as an Azure Key Store and never included
        # directly in the app but for the purposes of a test it is safe to put it here
        self.api_key = 'EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23'
        return


    # Sends a GET requests and retrieves a response
    def _do_get_request_call_and_get_response(self):
        response = None
        retries = 5

        headers = {
            'x-api-key': self.api_key,
            'Accept': 'application/json',
            'Content-type': 'application/json',
        }

        while retries > 0:
            try:
                response = requests.get(
                    url=self.URL,
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
                    retries -= 1
                    logging.info("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    raise Exception(e)
            else:
                break

        logging.info("WebRequest::_do_get_request_call_and_get_response status code: " + str(response.status_code))
        return response


    # Sends a POST requests and retrieves a response
    def _do_post_request_and_get_response(self, payload):
        response = None
        retries = 5

        headers = {
            'x-api-key': 'EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23'
        }

        while retries > 0:
            try:
                response = requests.post(
                    url=self.URL,
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
                    retries -= 1
                    logging.info("Retrying...")
                    time.sleep(1)
                    continue
                else:
                    raise Exception(e)
            else:
                break

        logging.info("WebRequest::_do_post_request_and_get_response status code: " + str(response.status_code))
        return response
