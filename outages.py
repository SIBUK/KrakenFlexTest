from web_request import WebRequest

class Outages(WebRequest):
    def __init__(self):
        WebRequest.__init__(self, 'outages')
        return

    # Send GET request to outages endpoint and return JSON and status code from the response
    def get_outages_json(self):
        r = self._do_get_request_call_and_get_response()
        status_code = r.status_code
        if status_code == 200:
            json_object = r.json()
            return json_object, status_code
        else:
            return None, status_code


