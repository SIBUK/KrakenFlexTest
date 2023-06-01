# Kraken Flex Technical Test by Simon Bailey

This is my solution to the Kraken Flex technical test.
The app uses Python 3 and the following two libraries to help achieve the objective of submitting valid data to an endpoint:

* Request - for sending HTTP requests using Python
* PySpark - for data manipulation using Python

There are several classes that I created to help. Here is a brief explanation of them:
* There is a base class called WebRequest. This handles any POST and GET requests
  * The Outages class inherits from WebRequest and deals specifically with fetching the Outages data
  * The SiteInfo class inherits from WebRequest and deals specifically with fetching the Site data
  * The SiteOutages class inherits from WebRequest and deals specifically posting the Outages data
* The SparkWrapper class contains the instance of PySpark and contains functions that perform any data operation
* There is also a folder named Tests that contains all the tests

The application works in the following way:

1. The Outages class fetches the outages in JSON format
2. This JSON then gets passed to a function in the SparkWrapper class which uses spark to convert it to a dataframe containing all the outages data fetched from the outages endpoint
3. This dataframe is then passed to another SparkWrapper function which filters out all the begin dates that start before midnight 2022-01-01 as per the requirements. A new dataframe is created from this.
4. The SiteInfo class then fetches the Site Info in JSON format
5. This JSON then also gets passed to a function in the SparkWrapper class which uses spark to convert it to a dataframe containing all the site data fetched from the sitedata endpoint
6. Both the Outages and Site Data dataframes are then passed to another SparkWrapper function which performs an inner join to get the required data and a final dataframe is created from this
7. The data from the final dataframe is then passed to the SiteOutages class which posts it to the endpoint and confirms that the success status code 200 is received

It is also worth noting that the Bonus Requirement of dealing with the 500 status code has also been completed. In the event of a 500 status code the request will be retried a maximum of 5 times before the app throws an exception (as it cant continue).

### Dependencies

##### Here is a list of the dependencies required by the script:

1. python 3.10.11 - Install from https://www.python.org/downloads/
2. PySpark 3.4.0 - From the root of the project type __*pip install pyspark==3.4.0*__ to install this dependency
3. request  - From the root of the project type __*pip install request*__ to install this dependency

### Running the Application  

After the dependencies above have been installed, the project can be run by typing the following command in the root of the project folder:

* __*python main.py*__

The project can also be loaded into an IDE such as PyCharm and executed by running 'main'. 

### Running the Tests

There is a full suite of tests present for all the classes. Test files are stored in a separate folder called 'tests' inside the project directory. To run the tests type the following command in the terminal inside the project root directory:

__*python -m unittest discover -s tests -t tests*__

### Known Issues

Occasionally when running the app in Windows you may receive this error as the app exits:
###### __*ERROR ShutdownHookManager: Exception while deleting Spark temp dir*__ 
 
This appears to be an issue with the ShutdownHook inside PySpark where it sometimes fails while deleting its own temporary files. It isn't related to anything I've done in my app, and unfortunately there does not appear to be a fix for it currently.
