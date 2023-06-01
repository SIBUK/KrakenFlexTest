import sys
import unittest
import pyspark
from main import *

class TestMainFunctions(unittest.TestCase):
    # Test that the create_spark_instance function in main returns a valid spark object
    def test_create_spark_instance(self):
        spark = create_spark_instance('KrakenFlexTestTest')

        self.assertIsInstance(spark, pyspark.sql.session.SparkSession)
