# Kraken Flex Technical Test by Simon Bailey

This is my solution to the Kraken Flex technical test.
The app uses Python 3 and the following two libraries to help achieve the objective of submitting valid data to an endpoint:

* Request - for sending HTTP requests using Python
* DateUtil - for ISO 8601 date manipulation using Python

There are a few functions and a couple of classes that I created to help. Here is a brief explanation of them:
* There is a class called WebRequest inside the web_request file. This handles any POST and GET requests.
  * There are 2 private functions for handing GET and POST requests
  * There are 3 public functions for calling the site-info, outages and site-outages endpoints
  * There is also another small class with a custom exception defined in this file called RetriesExceededError that is used for when web requests fail after multiple retries
* There are a couple of functions in the data_functions file for manipulating data. They may be small, but putting them here instead of inline has the advantage of making them easily testable and keeps the main function cleaner
* There is also a folder named Tests that contains all the tests

The application works in the following way:

1. The get_outages_json function fetches the outages in JSON format.
2. This JSON is then passed to a function which filters out all the begin dates that start before midnight 2022-01-01 as per the requirements. A new JSON object is created from this and returned.
3. The get_site_info_json function then fetches the Site Info in JSON format.
4. Both the Outages and Site Info JSON objects are then passed to another function which performs a join and creates the final JSON structure for posting to the final endpoint.
5. The data from this resulting JSON object is then posted to the endpoint and confirmation is made that the success status code 200 is received.

It is also worth noting that the Bonus Requirement of dealing with the 500 status code has also been completed. In the event of a 500 status code the request will be retried a maximum of 5 times before the app throws an exception (as it cant continue).

### Dependencies

##### Here is a list of the dependencies required by the script:

1. python >= 3.7 - Install from https://www.python.org/downloads/
2. python-dateutil v2.8.2
3. request v2.31.0

A setup.py file is included. To install the dependencies type the following command in the terminal from the project root directory:
 
__*pip install .*__

### Running the Application  

After the dependencies above have been installed, the project can be run by typing the following command in the root of the project folder:

* __*python main.py*__

The project can also be loaded into an IDE such as PyCharm and executed by running 'main'. 

### Running the Tests

There is a full suite of tests present for all the classes. Test files are stored in a separate folder called 'tests' inside the project directory. To run the tests type the following command in the terminal inside the project root directory:

__*python -m unittest discover -s tests -t tests*__
