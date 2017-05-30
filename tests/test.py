import unittest

from test_database_connection import DataBaseTestCases
from test_event_parser import EventParserTestCases
from test_pageview_parser import PageViewParserTestCases
from test_s3 import S3TestCases

if __name__ == '__main__':
    unittest.main()
